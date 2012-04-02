# Configuration
# ===========================================================================

if [ -f ~/.dotfiles/git/git-completion.bash ]; then
  source ~/.dotfiles/git/git-completion.bash
fi

environment() {
  if [[ $(pwd | grep /Volumes/Active-Projects/Developer-Environments/Taylor-Smith 2> /dev/null) ]];
  then
    echo "↓ "
  elif [[ $(pwd | grep /Volumes/Active-Projects/Websites 2> /dev/null) ]];
  then
    echo "↑ "
  fi
}

format_vcprompt() {
  vcprompt -f " [%n:%b%m%u]"
}

PS1='$(environment)\W$(format_vcprompt) \$ '
# PS1='\W$(__git_ps1 " [%s]") \$ '
# PS1='\W \$ '

# Readline Settings
bind "set completion-ignore-case on"
