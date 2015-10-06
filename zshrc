set -o emacs

# Change Dirs without 'cd'
setopt auto_cd

# Consolidate Dupes
setopt histignoredups

# Disable AutoCorrect
unsetopt correct_all

# Uncomment to change how many often would you like to wait before auto-updates occur? (in days)
export UPDATE_ZSH_DAYS=1

# Uncomment following line if you want to disable colors in ls
# DISABLE_LS_COLORS="true"

# Uncomment following line if you want to disable autosetting terminal title.
# DISABLE_AUTO_TITLE="true"

# Uncomment following line if you want red dots to be displayed while waiting for completion
COMPLETION_WAITING_DOTS="true"

plugins=(git)

ZSH=$HOME/.oh-my-zsh
ZSH_THEME="robbyrussell"
#ZSH_THEME="agnoster"

source $ZSH/oh-my-zsh.sh

[[ -s "${HOME}/.aliases" ]] && source "${HOME}/.aliases"
### Added by the Heroku Toolbelt
export PATH="/usr/local/heroku/bin:$PATH"
