# Configuration
# ===========================================================================

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

# Readline Settings
bind "set completion-ignore-case on"
