# Copyright (C) 2011 Fog Creek Software.  All rights reserved.
#
# To enable the "kiln" extension put these lines in your ~/.hgrc:
#  [extensions]
#  kiln = /path/to/kiln.py
#
# For help on the usage of "hg kiln" use:
#  hg help kiln
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

'''provides command-line support for working with Kiln

This extension allows you to directly open up the Kiln page for your
repository, including the annotation, file view, outgoing, and other
pages.  Additionally, it will attempt to guess which remote Kiln
repository you wish push to and pull from based on its related repositories.

This extension will also notify you when a Kiln server you access has an
updated version of the Kiln Client and Tools available.
To disable the check for a version 'X.Y.Z' and all lower versions, add the
following line in the [kiln] section of your hgrc:
    ignoreversion = X.Y.Z
'''
import os
import re
import urllib
import urllib2
import sys

from cookielib import MozillaCookieJar
from hashlib import md5
from mercurial import commands, demandimport, extensions, hg, httprepo, \
        localrepo, match, util
from mercurial import ui as hgui
from mercurial import url as hgurl
from mercurial.error import RepoError
from mercurial.i18n import _
from mercurial.node import nullrev

try:
    from mercurial import scmutil
except ImportError:
    pass

demandimport.disable()
try:
    import json
except ImportError:
    sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '_custom'))
    import json

try:
    import webbrowser
    def browse(url):
        webbrowser.open(escape_reserved(url))
except ImportError:
    if os.name == 'nt':
        import win32api
        def browse(url):
            win32api.ShellExecute(0, 'open', escape_reserved(url), None, None, 0)
demandimport.enable()

_did_version_check = False

class APIError(Exception):
    def __init__(self, obj):
        '''takes a json object for debugging

        Inspect self.errors to see the API errors thrown.
        '''
        self.errors = []
        for error in obj['errors']:
            data = error['codeError'], error['sError']
            self.errors.append('%s: %s' % data)

    def __str__(self):
        return '\n'.join(self.errors)

def urljoin(*components):
    url = components[0]
    for next in components[1:]:
        if not url.endswith('/'):
            url += '/'
        if next.startswith('/'):
            next = next[1:]
        url += next
    return url

def _baseurl(ui, path):
    remote = hg.repository(ui, path)
    try:
        # Mercurial >= 1.9
        url = util.removeauth(remote.url())
    except AttributeError:
        # Mercurial <= 1.8
        url = hgurl.removeauth(remote.url())
    if url.lower().find('/kiln/') > 0 or url.lower().find('kilnhg.com/') > 0:
        return url
    else:
        return None

def escape_reserved(path):
    reserved = re.compile(
               r'^(((com[1-9]|lpt[1-9]|con|prn|aux)(\..*)?)|web\.config' +
               r'|clock\$|app_data|app_code|app_browsers' +
               r'|app_globalresources|app_localresources|app_themes' +
               r'|app_webreferences|bin|.*\.(cs|vb)html?)$', re.IGNORECASE)
    p = path.split('?')
    path = p[0]
    query = '?' + p[1] if len(p) > 1 else ''
    return '/'.join('$' + part + '$'
                    if reserved.match(part) or part.startswith('$') or part.endswith('$')
                    else part
                    for part in path.split('/')) + query

def normalize_name(s):
    return s.lower().replace(' ', '-')

def call_api(ui, baseurl, urlsuffix, params, post=False):
    '''returns the json object for the url and the data dictionary

    Uses HTTP POST if the post parameter is True and HTTP GET
    otherwise. Raises APIError on API errors.
    '''
    url = baseurl + urlsuffix
    data = urllib.urlencode(params, doseq=True)
    try:
        if post:
            fd = urllib2.urlopen(url, data)
        else:
            fd = urllib2.urlopen(url + '?' + data)
        obj = json.load(fd)
    except Exception:
        raise util.Abort(_('Path guessing requires Fog Creek Kiln 2.0.  If you'
                           ' are running Kiln 2.0 and continue to experience'
                           ' problems, please contact Fog Creek Software.'))

    if isinstance(obj, dict) and 'errors' in obj:
        if 'token' in params and obj['errors'][0]['codeError'] == 'InvalidToken':
            token = login(ui, baseurl)
            add_kilnapi_token(ui, baseurl, token)
            params['token'] = token
            return call_api(ui, baseurl, urlsuffix, params, post)
        raise APIError(obj)
    return obj

def login(ui, url):
    ui.write(_('realm: %s\n') % url)
    user = ui.prompt('username:')
    pw = ui.getpass()

    token = call_api(ui, url, 'Api/1.0/Auth/Login', dict(sUser=user, sPassword=pw))

    if token:
        return token
    raise util.Abort(_('authorization failed'))

def get_domain(url):
    temp = url[url.find('://') + len('://'):]
    domain = temp[:temp.find('/')]
    port = None
    if ':' in domain:
        domain, port = domain.split(':', 1)
    if '.' not in domain:
        domain += '.local'

    return domain

def _get_path(path):
    if os.name == 'nt':
        ret = os.path.expanduser('~\\_' + path)
    else:
        ret = os.path.expanduser('~/.' + path)
    # Cygwin's Python does not always expanduser() properly...
    if re.match(r'^[A-Za-z]:', ret) is not None and re.match(r'[A-Za-z]:\\', ret) is None:
        ret = re.sub(r'([A-Za-z]):', r'\1:\\', ret)
    return ret

def _upgradecheck(ui, repo):
    global _did_version_check
    if _did_version_check or not ui.configbool('kiln', 'autoupdate', True):
        return
    _did_version_check = True
    _upgrade(ui, repo)

def _upgrade(ui, repo):
    ext_dir = os.path.dirname(os.path.abspath(__file__))
    ui.debug('kiln: checking for extensions upgrade for %s\n' % ext_dir)

    try:
        r = localrepo.localrepository(hgui.ui(), ext_dir)
    except RepoError:
        commands.init(hgui.ui(), dest=ext_dir)
        r = localrepo.localrepository(hgui.ui(), ext_dir)

    r.ui.setconfig('kiln', 'autoupdate', False)
    r.ui.pushbuffer()
    try:
        source = 'https://developers.kilnhg.com/Repo/Kiln/Group/Kiln-Extensions'
        if commands.incoming(r.ui, r, bundle=None, force=False, source=source) != 0:
            # no incoming changesets, or an error. Don't try to upgrade.
            ui.debug('kiln: no extensions upgrade available\n')
            return
        ui.write(_('updating Kiln Extensions at %s... ') % ext_dir)
        # pull and update return falsy values on success
        if commands.pull(r.ui, r, source=source) or commands.update(r.ui, r, clean=True):
            url = urljoin(repo.url()[:repo.url().lower().index('/repo')], 'Tools')
            ui.write(_('unable to update\nvisit %s to download the newest extensions\n') % url)
        else:
            ui.write(_('complete\n'))
    except Exception, e:
        ui.debug(_('kiln: error updating Kiln Extensions: %s\n') % e)

def is_dest_a_path(ui, dest):
    paths = ui.configitems('paths')
    for pathname, path in paths:
        if pathname == dest:
            return True
    return False

def is_dest_a_scheme(ui, dest):
    destscheme = dest[:dest.find('://')]
    if destscheme:
        for scheme in hg.schemes:
            if destscheme == scheme:
                return True
    return False

def create_match_list(matchlist):
    ret = ''
    for m in matchlist:
        ret += '    ' + m + '\n'
    return ret

def get_username(url):
    url = re.sub(r'https?://', '', url)
    url = re.sub(r'/.*', '', url)
    if '@' in url:
        # There should be some login info
        # rfind in case it's an email address
        username = url[:url.rfind('@')]
        if ':' in username:
            username = url[:url.find(':')]
        return username
    # Didn't find anything...
    return ''

def get_dest(ui):
    from mercurial.dispatch import _parse
    try:
        cmd_info = _parse(ui, sys.argv[1:])
        cmd = cmd_info[0]
        dest = cmd_info[2]
        if dest:
            dest = dest[0]
        elif cmd in ['outgoing', 'push']:
            dest = 'default-push'
        else:
            dest = 'default'
    except:
        dest = 'default'
    return ui.expandpath(dest)

def check_kilnapi_token(ui, url):
    tokenpath = _get_path('hgkiln')

    if (not os.path.exists(tokenpath)) or os.path.isdir(tokenpath):
        return ''

    domain = get_domain(url)
    userhash = md5(get_username(get_dest(ui))).hexdigest()

    fp = open(tokenpath, 'r')
    ret = ""
    for line in fp:
        try:
            d, u, t = line.split(' ')
        except:
            raise util.Abort(_('Authentication file %s is malformed.') % tokenpath)
        if d == domain and u == userhash:
            # Get rid of that newline character...
            ret = t[:-1]

    fp.close()
    return ret

def add_kilnapi_token(ui, url, fbToken):
    if not fbToken:
        return
    tokenpath = _get_path('hgkiln')
    if os.path.isdir(tokenpath):
        raise util.Abort(_('Authentication file %s exists, but is a directory.') % tokenpath)

    domain = get_domain(url)
    userhash = md5(get_username(get_dest(ui))).hexdigest()

    fp = open(tokenpath, 'a')
    fp.write(domain + ' ' + userhash + ' ' + fbToken + '\n')
    fp.close()

def delete_kilnapi_tokens():
    # deletes the hgkiln file
    tokenpath = _get_path('hgkiln')
    if os.path.exists(tokenpath) and not os.path.isdir(tokenpath):
        os.remove(tokenpath)

def check_kilnauth_token(ui, url):
    cookiepath = _get_path('hgcookies')
    if (not os.path.exists(cookiepath)) or (not os.path.isdir(cookiepath)):
        return ''
    cookiepath = os.path.join(cookiepath, md5(get_username(get_dest(ui))).hexdigest())

    try:
        if not os.path.exists(cookiepath):
            return ''
        cj = MozillaCookieJar(cookiepath)
    except IOError, e:
        return ''

    domain = get_domain(url)

    cj.load(ignore_discard=True, ignore_expires=True)
    for cookie in cj:
        if domain == cookie.domain:
            if cookie.name == 'fbToken':
                return cookie.value

def remember_path(ui, repo, path, value):
    '''appends the path to the working copy's hgrc and backs up the original'''

    paths = dict(ui.configitems('paths'))
    # This should never happen.
    if path in paths: return
    # ConfigParser only cares about these three characters.
    if re.search(r'[:=\s]', path): return

    try:
        audit_path = scmutil.pathauditor(repo.root)
    except ImportError:
        audit_path = getattr(repo.opener, 'audit_path', util.path_auditor(repo.root))

    audit_path('hgrc')
    audit_path('hgrc.backup')
    base = repo.opener.base
    util.copyfile(os.path.join(base, 'hgrc'),
                  os.path.join(base, 'hgrc.backup'))
    ui.setconfig('paths', path, value)

    try:
        fp = repo.opener('hgrc', 'a', text=True)
        # Mercurial assumes Unix newlines by default and so do we.
        fp.write('\n[paths]\n%s = %s\n' % (path, value))
        fp.close()
    except IOError, e:
        return

def unremember_path(ui, repo):
    '''restores the working copy's hgrc'''

    try:
        audit_path = scmutil.pathauditor(repo.root)
    except ImportError:
        audit_path = getattr(repo.opener, 'audit_path', util.path_auditor(repo.root))

    audit_path('hgrc')
    audit_path('hgrc.backup')
    base = repo.opener.base
    if os.path.exists(os.path.join(base, 'hgrc')):
        util.copyfile(os.path.join(base, 'hgrc.backup'),
                      os.path.join(base, 'hgrc'))

def guess_kilnpath(orig, ui, repo, dest=None, **opts):
    if not dest:
        return orig(ui, repo, **opts)

    if os.path.exists(dest) or is_dest_a_path(ui, dest) or is_dest_a_scheme(ui, dest):
        return orig(ui, repo, dest, **opts)
    else:
        targets = get_targets(repo);
        matches = []
        prefixmatches = []

        for target in targets:
            url = '%s/%s/%s/%s' % (target[0], target[1], target[2], target[3])
            ndest = normalize_name(dest)
            ntarget = [normalize_name(t) for t in target[1:4]]
            aliases = [normalize_name(s) for s in target[4]]

            if ndest.count('/') == 0 and \
                (ntarget[0] == ndest or \
                ntarget[1] == ndest or \
                ntarget[2] == ndest or \
                ndest in aliases):
                matches.append(url)
            elif ndest.count('/') == 1 and \
                '/'.join(ntarget[0:2]) == ndest or \
                '/'.join(ntarget[1:3]) == ndest:
                matches.append(url)
            elif ndest.count('/') == 2 and \
                '/'.join(ntarget[0:3]) == ndest:
                matches.append(url)

            if (ntarget[0].startswith(ndest) or \
                ntarget[1].startswith(ndest) or \
                ntarget[2].startswith(ndest) or \
                '/'.join(ntarget[0:2]).startswith(ndest) or \
                '/'.join(ntarget[1:3]).startswith(ndest) or \
                '/'.join(ntarget[0:3]).startswith(ndest)):
                prefixmatches.append(url)

        if len(matches) == 0:
            if len(prefixmatches) == 0:
                # if there are no matches at all, let's just let mercurial handle it.
                return orig(ui, repo, dest, **opts)
            else:
                urllist = create_match_list(prefixmatches)
                raise util.Abort(_('%s did not exactly match any part of the repository slug:\n\n%s') % (dest, urllist))
        elif len(matches) > 1:
            urllist = create_match_list(matches)
            raise util.Abort(_('%s matches more than one Kiln repository:\n\n%s') % (dest, urllist))

        # Unique match -- perform the operation
        try:
            remember_path(ui, repo, dest, matches[0])
            return orig(ui, repo, matches[0], **opts)
        finally:
            unremember_path(ui, repo)

def get_tails(repo):
    tails = []
    for rev in xrange(repo['tip'].rev() + 1):
        ctx = repo[rev]
        if ctx.p1().rev() == nullrev and ctx.p2().rev() == nullrev:
            tails.append(ctx.hex())
    if not len(tails):
        raise util.Abort(_('Path guessing is only enabled for non-empty repositories.'))
    return tails

def get_targets(repo):
    targets = []
    kilnschemes = repo.ui.configitems('kiln_scheme')
    for scheme in kilnschemes:
        url = scheme[1]
        if url.lower().find('/kiln/') != -1:
            baseurl = url[:url.lower().find('/kiln/') + len("/kiln/")]
        elif url.lower().find('kilnhg.com/') != -1:
            baseurl = url[:url.lower().find('kilnhg.com/') + len("kilnhg.com/")]
        else:
            continue

        tails = get_tails(repo)

        token = check_kilnapi_token(repo.ui, baseurl)
        if not token:
            token = check_kilnauth_token(repo.ui, baseurl)
            add_kilnapi_token(repo.ui, baseurl, token)
        if not token:
            token = login(repo.ui, baseurl)
            add_kilnapi_token(repo.ui, baseurl, token)

        # We have an token at this point
        params = dict(revTails=tails, token=token)
        related_repos = call_api(repo.ui, baseurl, 'Api/1.0/Repo/Related', params)
        targets.extend([[url,
                         related_repo['sProjectSlug'],
                         related_repo['sGroupSlug'],
                         related_repo['sSlug'],
                         related_repo.get('rgAliases', [])] for related_repo in related_repos])
    return targets

def display_targets(repo):
    targets = get_targets(repo)
    repo.ui.write(_('The following Kiln targets are available for this repository:\n\n'))
    for target in targets:
        if target[4]:
            alias_text = _(' (alias%s: %s)') % ('es' if len(target[4]) > 1 else '', ', '.join(target[4]))
        else:
            alias_text = ''
        repo.ui.write('    %s/%s/%s/%s%s\n' % (target[0], target[1], target[2], target[3], alias_text))

def dummy_command(ui, repo, dest=None, **opts):
    '''dummy command to pass to guess_path() for hg kiln

    Returns the repository URL if dest has been successfully path
    guessed, None otherwise.
    '''
    return opts['path'] != dest and dest or None

def kiln(ui, repo, *pats, **opts):
    '''show the relevant page of the repository in Kiln

    This command allows you to navigate straight the Kiln page for a
    repository, including directly to settings, file annotation, and
    file & changeset viewing.

    Typing "hg kiln" by itself will take you directly to the
    repository history in kiln.  Specify any other options to override
    this default. The --rev, --annotate, --file, and --filehistory options
    can be used together.

    To display a list of valid targets, type hg kiln --targets.  To
    push or pull from one of these targets, use any unique identifier
    from this list as the parameter to the push/pull command.
    '''

    try:
        url = _baseurl(ui, ui.expandpath(opts['path'] or 'default', opts['path'] or 'default-push'))
    except RepoError:
        url = guess_kilnpath(dummy_command, ui, repo, dest=opts['path'], **opts)
        if not url:
            raise

    if not url:
        raise util.Abort(_('this does not appear to be a Kiln-hosted repository\n'))
    default = True

    def files(key):
        allpaths = []
        for f in opts[key]:
            paths = [path for path in repo['.'].manifest().iterkeys() if re.search(match._globre(f) + '$', path)]
            paths = [re.sub(r'^\.kbf', '', path) for path in paths]
            if not paths:
                ui.warn(_('cannot find %s') % f)
            allpaths += paths
        return allpaths

    if opts['rev']:
        default = False
        for ctx in (repo[rev] for rev in opts['rev']):
            browse(urljoin(url, 'History', ctx.hex()))

    if opts['annotate']:
        default = False
        for f in files('annotate'):
            browse(urljoin(url, 'File', f) + '?view=annotate')
    if opts['file']:
        default = False
        for f in files('file'):
            browse(urljoin(url, 'File', f))
    if opts['filehistory']:
        default = False
        for f in files('filehistory'):
            browse(urljoin(url, 'FileHistory', f) + '?rev=tip')

    if opts['outgoing']:
        default = False
        browse(urljoin(url, 'Outgoing'))
    if opts['settings']:
        default = False
        browse(urljoin(url, 'Settings'))

    if opts['targets']:
        default = False
        display_targets(repo)
    if opts['logout']:
        default = False
        delete_kilnapi_tokens()

    if default or opts['changes']:
        browse(url)

def uisetup(ui):
    extensions.wrapcommand(commands.table, 'outgoing', guess_kilnpath)
    extensions.wrapcommand(commands.table, 'push', guess_kilnpath)
    extensions.wrapcommand(commands.table, 'pull', guess_kilnpath)
    extensions.wrapcommand(commands.table, 'incoming', guess_kilnpath)

def reposetup(ui, repo):
    if issubclass(repo.__class__, httprepo.httprepository):
        _upgradecheck(ui, repo)

def extsetup(ui):
    try:
        g = extensions.find('gestalt')
        extensions.wrapcommand(g.cmdtable, 'overview', guess_kilnpath)
        extensions.wrapcommand(g.cmdtable, 'advice', guess_kilnpath)
        extensions.wrapcommand(g.cmdtable, 'next', guess_kilnpath)
    except KeyError:
        pass

    try:
        f = extensions.find('fetch')
        extensions.wrapcommand(f.cmdtable, 'fetch', guess_kilnpath)
    except KeyError:
        pass

cmdtable = {
    'kiln':
        (kiln,
         [('a', 'annotate', [], _('annotate the file provided')),
          ('c', 'changes', None, _('view the history of this repository; this is the default')),
          ('f', 'file', [], _('view the file contents')),
          ('l', 'filehistory', [], _('view the history of the file')),
          ('o', 'outgoing', None, _('view the repository\'s outgoing tab')),
          ('s', 'settings', None, _('view the repository\'s settings tab')),
          ('p', 'path', '', _('select which Kiln branch of the repository to use')),
          ('r', 'rev', [], _('view the specified changeset in Kiln')),
          ('t', 'targets', None, _('view the repository\'s targets')),
          ('', 'logout', None, _('log out of Kiln sessions'))],
         _('hg kiln [-p url] [-r rev|-a file|-f file|-c|-o|-s|-t|--logout]'))
    }
