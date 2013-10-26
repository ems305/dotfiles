all: clean build

clean:
	rm -rf ~/.ackrc
	rm -rf ~/.aliases
	rm -rf ~/.bash_profile
	rm -rf ~/.bashrc
	rm -rf ~/.env
	rm -rf ~/.gemrc
	rm -rf ~/.gitconfig
	rm -rf ~/.gitignore
	rm -rf ~/.guardrc
	rm -rf ~/.hushlogin
	rm -rf ~/.inputrc
	rm -rf ~/.profile
	rm -rf ~/.railsrc
	rm -rf ~/.tmux.conf
	rm -rf ~/.vim
	rm -rf ~/.vimrc
	rm -rf ~/.zlogin
	rm -rf ~/.zsh
	rm -rf ~/.zshenv
	rm -rf ~/.zshrc

build:
	ln -s $(CURDIR)/ackrc ~/.ackrc
	ln -s $(CURDIR)/aliases ~/.aliases
	ln -s $(CURDIR)/bash_profile ~/.bash_profile
	ln -s $(CURDIR)/bashrc ~/.bashrc
	ln -s $(CURDIR)/env ~/.env
	ln -s $(CURDIR)/gemrc ~/.gemrc
	ln -s $(CURDIR)/gitconfig ~/.gitconfig
	ln -s $(CURDIR)/gitignore ~/.gitignore
	ln -s $(CURDIR)/guardrc ~/.guardrc
	ln -s $(CURDIR)/hushlogin ~/.hushlogin
	ln -s $(CURDIR)/inputrc ~/.inputrc
	ln -s $(CURDIR)/profile ~/.profile
	ln -s $(CURDIR)/railsrc ~/.railsrc
	ln -s $(CURDIR)/tmux.conf ~/.tmux.conf
	ln -s $(CURDIR)/vim ~/.vim
	ln -s $(CURDIR)/vimrc ~/.vimrc
	ln -s $(CURDIR)/zlogin ~/.zlogin
	ln -s $(CURDIR)/zsh ~/.zsh
	ln -s $(CURDIR)/zshenv ~/.zshenv
	ln -s $(CURDIR)/zshrc ~/.zshrc

