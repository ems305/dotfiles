Dotfiles
========

Configuration files to get my system the way I like it.

Installation
------------

    git clone git://github.com/taylorsmith/dotfiles.git ~/.dotfiles
    ln -s ~/.dotfiles/bash_profile ~/.bash_profile
    ln -s ~/.dotfiles/bashrc ~/.bashrc
    ln -s ~/.dotfiles/gitconfig ~/.gitconfig
    ln -s ~/.dotfiles/hgrc ~/.hgrc

A note on SSH
-------------

I've ignored `ssh/config` in the spirit of privacy. Assuming you want one, run the following:

    mkdir ~/.dotfiles/ssh
    touch ~/.dotfiles/ssh/config
    ln -s ~/.dotfiles/ssh/config ~/.ssh/config
