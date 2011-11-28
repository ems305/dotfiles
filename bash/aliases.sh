# Aliases
# ===========================================================================

# Changing Directories
alias ..='cd ..'
alias cdd='cd -'

# Nice file listings
alias ls='ls -lh'
alias la='ls -la'

# Commonly accessed directories
alias db='cd ~/Dropbox'

# Apache
alias hosts='mate /private/etc/hosts'
alias virtualhosts='mate /private/etc/apache2/virtualhosts'
alias restart='sudo /usr/sbin/apachectl restart'

# Web Browsers
alias c='open -a /Applications/Google\ Chrome.app'
alias f='open -a /Applications/Firefox.app'
alias s='open -a /Applications/Safari.app'

# Override defaults
alias grep='grep --color'


alias cwd='pwd | pbcopy'



# Functions
# ===========================================================================

# Connect to the development server
dev1 () {
  if [ ! -d "/Volumes/Active-Projects/Developer-Environments/Taylor-Smith/" ]; then
    echo "Connecting ..."
    osascript -e "try" -e "mount volume \"smb://taylor.smith@192.168.5.21/Active-Projects\"" -e "end try"
  fi
}

# Browse to dev folder, connect if necessary
dev () {
  dev1
  cd '/Volumes/Active-Projects/Developer-Environments/Taylor-Smith/'
}

# Browse to websites folder, connect if necessary
web () {
  dev1
  cd '/Volumes/Active-Projects/Websites/'
}

# Make a new directory and browse to it
mcd () {
  mkdir "$@" && cd "$@"
}

# Make a new directoy and delete it. For the luls.
mrm () {
  mkdir "$@" && rm -r "$@"
}

# Fixes caching issues you may run into in Umbraco
flush () {
  touch web.config
  rm App_Data/umbraco.config
}

show_colors () {
	T='gYw'   # The test text

	echo -e "\n                 40m     41m     42m     43m\
	     44m     45m     46m     47m";

	for FGs in '    m' '   1m' '  30m' '1;30m' '  31m' '1;31m' '  32m' \
	           '1;32m' '  33m' '1;33m' '  34m' '1;34m' '  35m' '1;35m' \
	           '  36m' '1;36m' '  37m' '1;37m';
	  do FG=${FGs// /}
	  echo -en " $FGs \033[$FG  $T  "
	  for BG in 40m 41m 42m 43m 44m 45m 46m 47m;
	    do echo -en "$EINS \033[$FG\033[$BG  $T  \033[0m";
	  done
	  echo;
	done
	echo
}

function randompass () {
  password=`cat /dev/urandom | env LC_CTYPE=C tr -cd 'a-z0-9' | head -c $1`
  echo $password
}

function make_gifs () {
  for file in *.jpg ; do mv $file `echo $file | sed 's/\(.*\.\)jpg/\1gif/'` ; done
}

function move_gifs () {
  for fname in *.gif
  do
    password=`cat /dev/urandom | env LC_CTYPE=C tr -cd 'a-z0-9' | head -c 5`
    mv "$fname" $password.gif
  done
}

function lipsum () {
  if [ -z "$1" ]
  then
    curl --silent "http://loripsum.net/api/10/medium/" | pbcopy
    echo "Copied 10 paragraphs of dummy text"
  else
    curl --silent "http://loripsum.net/api/$1/medium/" | pbcopy
    echo "Copied $1 paragraphs of dummy text"
  fi
}



alias glog="git log --graph --pretty=format:'%Cred%h%Creset %an: %s - %Creset %C(yellow)%d%Creset %Cgreen(%cr)%Creset' --abbrev-commit --date=relative"
alias gp='git push origin HEAD'
alias gd='git diff'
alias gc='git commit'
alias gca='git commit -a'
alias gco='git checkout'
alias gb='git branch'
alias gs='git status -sb'
alias grm="git status | grep deleted | awk '{print \$3}' | xargs git rm"
