" Boot up pathogen
call pathogen#infect()
call pathogen#helptags()

" Map my leader key
let mapleader=","

" Pick a theme
color ir_black
syntax on

" Set all the things
set nocompatible
set hidden
set t_Co=256
set background=dark
set guifont=Inconsolata-g:h11
set notimeout
set ttimeout
set timeoutlen=50
set showtabline=2
set number
set numberwidth=5
set ruler
set hlsearch
set showmatch
set nowrap
set tabstop=2
set shiftwidth=2
set softtabstop=2
set expandtab
set smartindent
set autoindent " Copy indent from last line when starting new line.
set cursorline " Highlight current line
set vb
set ignorecase smartcase
set infercase
set cmdheight=2
set clipboard=unnamed
set winwidth=80
set list
set listchars=tab:▸\ ,eol:¬
set guioptions-=T
set guioptions-=r
set go-=L
set backupdir=~/.vim-tmp,~/.tmp,~/tmp,/var/tmp,/tmp
set directory=~/.vim-tmp,~/.tmp,~/tmp,/var/tmp,/tmp
set colorcolumn=80
set wildignore+=*/node_modules/**,*/bower_components/**
highlight ColorColumn guibg=#202020

filetype plugin on
filetype plugin indent on

" Set syntax for weird files
autocmd BufNewFile,BufRead *.master set filetype=html
autocmd BufNewFile,BufRead *.cshtml set filetype=html
autocmd BufNewFile,BufRead *.rabl set filetype=ruby

" Strip trailing whitespace
map <leader>w :call StripTrailingWhitespaces()<cr>

map <leader>t :CommandT<cr>

" Flush CommandT cache
map <leader>f :CommandTFlush<cr>\|:CommandT<cr>
map <leader>ga :CommandT assets<cr>
map <leader>gs :CommandT assets/stylesheets<cr>
map <leader>gj :CommandT assets/javascripts<cr>
map <leader>gv :CommandT Views<cr>

map <leader>gc :CommandT app/controllers<cr>
map <leader>gm :CommandT app/models<cr>
map <leader>gv :CommandT app/views<cr>
map <leader>gr :CommandT spec<cr>

map <Leader>r :call RunCurrentSpecFile()<CR>
map <Leader>s :call RunAllSpecs()<CR>
let g:rspec_command = "compiler rspec | set makeprg=zeus | Make rspec {spec}"

" Toggle git gutter
map <leader>g :ToggleGitGutter<cr>

" Toggle comments quickly
map <leader>c \\\<cr>

" Hash rocket
imap <c-l> <space>=><space>

" Strip trailing whitespace before save
autocmd BufWritePre * call StripTrailingWhitespaces()

" Move around splits with <c-hjkl>
nnoremap <c-j> <c-w>j
nnoremap <c-k> <c-w>k
nnoremap <c-h> <c-w>h
nnoremap <c-l> <c-w>l

nnoremap <Space> @q

" Switch between buffers
nnoremap <leader><leader> <c-^>

" Insert new lines without entering insert mode
map <c-S-Enter> O<Esc>
map <c-Enter> o<Esc>

" Hit return to remove search highlighting
function! MapCR()
  nnoremap <cr> :nohlsearch<cr>
endfunction
call MapCR()

" Multipurpose tab key
function! InsertTabWrapper()
  let col = col('.') - 1
  if !col || getline('.')[col - 1] !~ '\k'
    return "\<tab>"
  else
    return "\<c-p>"
  endif
endfunction
inoremap <tab> <c-r>=InsertTabWrapper()<cr>
inoremap <s-tab> <c-n>

" Highlight EOL whitespace, http://vim.wikia.com/wiki/Highlight_unwanted_spaces
highlight ExtraWhitespace ctermbg=darkred guibg=#ff0000
highlight clear SignColumn

autocmd ColorScheme * highlight ExtraWhitespace ctermbg=red guibg=red
autocmd BufWinEnter * match ExtraWhitespace /\s\+$/
autocmd InsertLeave * match ExtraWhitespace /\s\+$/
autocmd InsertEnter * match ExtraWhitespace /\s\+\%#\@<!$/

" Strip trailing whitespace
function! StripTrailingWhitespaces()
  let l = line(".")
  let c = col(".")
  %s/\s\+$//e
  call cursor(l, c)
endfunction

cnoremap %% <C-R>=expand('%:h').'/'<cr>
map <leader>v :!open %%<cr><cr>
