# Powerlevel10k instant prompt (keep at the very top)
if [[ -r "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh" ]]; then
  source "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh"
fi

export ZSH="$HOME/.oh-my-zsh"

ZSH_THEME="powerlevel10k/powerlevel10k"

ENABLE_CORRECTION="true"
COMPLETION_WAITING_DOTS="true"
HIST_STAMPS="dd.mm.yyyy"

plugins=(
    git
    zsh-autosuggestions
    zsh-syntax-highlighting
    sudo
    history
    colored-man-pages
    command-not-found
    extract
)

source $ZSH/oh-my-zsh.sh

export EDITOR='nvim'
export VISUAL='nvim'
export LANG=en_US.UTF-8
export PATH="$HOME/.local/bin:$HOME/bin:$PATH"

alias v="nvim"
alias c="clear"
alias ls="ls --color=auto"
alias ll="ls -lah --color=auto"
alias la="ls -A --color=auto"
alias grep="grep --color=auto"
alias ..="cd .."
alias ...="cd ../.."
alias gs="git status"
alias gc="git commit"
alias gp="git push"
alias gl="git log --oneline --graph --decorate"

# Powerlevel10k config
[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh
