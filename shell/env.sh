# Environment Variables
# =============================================================================

export EDITOR="vi"
export CLICOLOR=1

export PATH="/usr/local/sbin:$PATH"
export PATH="/usr/local/Cellar/ruby/1.9.2-p290/bin:$PATH"
export PATH="/usr/local/bin:$PATH"
export PATH="/Users/taylor/.dotfiles/bin:$PATH"

export NODE_PATH="/usr/local/lib/node_modules"

export ENVIRONMENT="development"

export LOLCOMMITS_DEVICE="Display iSight"

source ~/.dotfiles-private/shell/env.sh

[[ -s $HOME/.tmuxinator/scripts/tmuxinator ]] && source $HOME/.tmuxinator/scripts/tmuxinator
