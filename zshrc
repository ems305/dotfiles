if which rbenv > /dev/null; then eval "$(rbenv init -)"; fi

fpath=(~/.zsh/completion $fpath)

autoload -U compinit
compinit -C

for function in ~/.zsh/functions/*; do
  source $function
done

set -o emacs

bindkey "^Y" accept-and-hold
bindkey "^N" insert-last-word
bindkey -s "^T" "^Asudo ^E"

setopt auto_cd
setopt prompt_subst
setopt histignoredups
setopt autopushd
setopt pushdminus
setopt pushdsilent
setopt pushdtohome
setopt correct
setopt correct_all
setopt extended_glob
setopt interactivecomments

unsetopt correct_all

export PS1='[${SSH_CONNECTION+"%n@%m:"}%~] '
export HISTSIZE=4096
export DIRSTACKSIZE=10

zstyle ':completion:*' matcher-list 'm:{a-z}={A-Z}'

[[ -s "${HOME}/.aliases" ]] && source "${HOME}/.aliases"
