# General Purpose
# =============================================================================

alias ls='ls -lh'                                             # Default listings to the long version with unit suffixes
alias la='ls -la'                                             # Include directory entries whose names begin with a dot
alias ..='cd ..'                                              # Go up one directory
alias cdd='cd -'                                              # Go to previous directory
alias db='cd ~/Dropbox'                                       # Dropbox shortcut
alias dev='cd ~/Dropbox/dev'                                  # Dev shortcut
alias cwd='pwd | pbcopy'                                      # Copy working directory path
alias ip='dig +short myip.opendns.com @resolver1.opendns.com' # Get external IP address
alias iplocal='ipconfig getifaddr en1'                        # Internal IP address
alias ips='ip && iplocal'                                     # Output external and internal IP addresses


# Overrides
# =============================================================================

alias grep='grep --color'                                     # Default grep to show colors


# Apache
# =============================================================================

alias hosts='$EDITOR /private/etc/hosts'                      # Open hosts file in your editor
alias vhosts='$EDITOR /private/etc/apache2/virtualhosts'      # Open virtualhosts file in your editor
alias restart='sudo /usr/sbin/apachectl restart'              # Restart Apache


# Web Browsers
# =============================================================================

alias c='open -a /Applications/Google\ Chrome.app'            # Open Chrome
alias f='open -a /Applications/Firefox.app'                   # Open Firefox
alias s='open -a /Applications/Safari.app'                    # Open Safari


# Heroku
# =============================================================================

alias h='heroku'                                              # Heroku is hard to type, man
alias hl='h logs --tail'                                      # Tail heroku logs
alias hr='h restart'                                          # Restart heroku processes
alias hc='h run console'                                      # Initiate heroku console


# Git
# =============================================================================

alias g='git'                                                 # 1 letter is better than 3
alias gd='git diff'                                           # Diff shortcut
alias gc='git commit'                                         # Commit shortcut
alias gca='git commit -a'                                     # Stage all tracked and modified files
alias gco='git checkout'                                      # Checkout shortcut
alias gb='git branch'                                         # Branch shortcut
alias gs='git status -sb'                                     # Simple git status view
alias gitfix='rm -f .git/index && git reset'                  # Fixes corrupted git index
alias repos='ssh git@gitarchive info'                         # Display all gitarchive repos
alias killsvn='find . -type d -name .svn | xargs rm -rf'      # Remove all .svn folders
