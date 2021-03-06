#@IgnoreInspection AddShebangLine
# Dependencies
#   antigen
#   functions/prompt_vcs_setup in function path
antigen bundle zsh-users/zsh-syntax-highlighting

setopt promptsubst
setopt extendedglob
setopt appendhistory
setopt sharehistory
setopt nomatch
setopt notify

autoload -U promptinit
promptinit
prompt vcs

antigen apply

