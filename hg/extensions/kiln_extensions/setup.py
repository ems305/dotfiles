import compileall
import os
import win32api
import zipfile

folders = ['bfiles', '_custom']
extensions = ['.py']
excludes = ['\\setup.py']

def compile_extensions():
    compileall.compile_dir(os.path.dirname(__file__), force=1)

def check_item(item):
    for exclude in excludes:
        if item[1].endswith(exclude):
            return False
    if item[1] in folders:
        return True
    for extension in extensions:
        if item[1].endswith(extension):
            return True
    return False

def list_files(dir_root, zip_root):
    subdirs = []
    items = []
    for item in os.listdir(dir_root):
        path = os.path.join(dir_root, item)
        zip_path = os.path.join(zip_root, item)
        if os.path.isfile(path):
            items.append([path, zip_path])
        else:
            subdirs.append([path, zip_path])
    for subdir in subdirs:
        items.extend(list_files(subdir[0], subdir[1]))
    return [f for f in items if check_item(f)]

def build_release():
    compile_extensions()
    dir = os.path.dirname(__file__)
    absdir = os.path.abspath(dir)
    files = list_files(absdir, '.')

    print 'Creating ZIP archive...'
    zip = zipfile.ZipFile(absdir + '\kiln_extensions.zip', 'w')
    for file in files:
        zip.write(file[0], file[1])
    zip.close()
    print 'Success!'

if __name__ == '__main__':
    build_release()
