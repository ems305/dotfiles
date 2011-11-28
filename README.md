Dotfiles
========

Configuration files to get my system the way I like it.

Installation
------------

    git clone git://github.com/taylorsmith/dotfiles.git ~/.dotfiles
    rake install

A note on SSH
-------------

I've ignored `ssh/config` in the spirit of privacy. Assuming you want one, run the following:

    mkdir ~/.dotfiles/ssh
    touch ~/.dotfiles/ssh/config
    ln -s ~/.dotfiles/ssh/config ~/.ssh/config
