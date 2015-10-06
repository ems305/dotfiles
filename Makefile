all: clean build create

clean:
	rm -rf ~/.aliases
	rm -rf ~/.bash_profile
	rm -rf ~/.bashrc
	rm -rf ~/.editorconfig
	rm -rf ~/.env
	rm -rf ~/.gemrc
	rm -rf ~/.gitconfig
	rm -rf ~/.githelpers
	rm -rf ~/.gitignore
	rm -rf ~/.hushlogin
	rm -rf ~/.profile
	rm -rf ~/.zsh
	rm -rf ~/.zshenv
	rm -rf ~/.zshrc

build:
	ln -s $(CURDIR)/aliases ~/.aliases
	ln -s $(CURDIR)/bash_profile ~/.bash_profile
	ln -s $(CURDIR)/bashrc ~/.bashrc
	ln -s $(CURDIR)/editorconfig ~/.editorconfig
	ln -s $(CURDIR)/env ~/.env
	ln -s $(CURDIR)/gemrc ~/.gemrc
	ln -s $(CURDIR)/gitconfig ~/.gitconfig
	ln -s $(CURDIR)/githelpers ~/.githelpers
	ln -s $(CURDIR)/gitignore ~/.gitignore
	ln -s $(CURDIR)/hushlogin ~/.hushlogin
	ln -s $(CURDIR)/profile ~/.profile
	ln -s $(CURDIR)/zsh ~/.zsh
	ln -s $(CURDIR)/zshenv ~/.zshenv
	ln -s $(CURDIR)/zshrc ~/.zshrc

create:
	mkdir -p ~/Development/Web
	mkdir -p ~/Development/iOS
	mkdir -p ~/Development/Android
	mkdir -p ~/Development/MultiPlatform