git_prompt_info() {
  ref=$(git symbolic-ref HEAD 2> /dev/null)
  if [[ -n $ref ]]; then
    echo " %{$reset_color%}[%{$fg[green]%}${ref#refs/heads/}%{$reset_color%}]"
  fi
}

autoload -U colors
colors

export CLICOLOR=1
# export PS1='$(git_prompt_info)[${SSH_CONNECTION+"%{$fg_bold[green]%}%n@%m:"}%{$fg_bold[blue]%}%~%{$reset_color%}] '
export PS1='%{$fg[blue]%}%c$(git_prompt_info) %{$FG[240]%}$ %{$reset_color%}'

# ZSH_THEME_GIT_PROMPT_PREFIX=" %{$FG[002]%}["
# ZSH_THEME_GIT_PROMPT_SUFFIX="%{$reset_color%}"
# ZSH_THEME_GIT_PROMPT_DIRTY=" %{$fg[red]%}±%{$FG[002]%}]%{$reset_color%}"
# ZSH_THEME_GIT_PROMPT_CLEAN="%{$FG[002]%}]"
