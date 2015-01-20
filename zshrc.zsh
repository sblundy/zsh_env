#@IgnoreInspection AddShebangLine
# Dependencies
#   antigen
#   functions/prompt_vcs_setup in function path
antigen bundle zsh-users/zsh-syntax-highlighting

autoload -U promptinit
promptinit
prompt vcs