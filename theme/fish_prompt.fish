set segment_separator \uE0B0

set error_section_open  \uE0B3
set error_section_close \uE0B1

set _prompt_time white
set _prompt_user green
set _prompt_path cyan

function _format_duration
  set -l duration $argv[1]

  #Select format depending on whether there are minutes, seconds, or just ms

  if test -z "$duration"
    #Special case of no duration
    echo -n '0'
  else if test $duration -eq 0
    #No duration
    echo -n '0'
  else if test $duration -lt 100
    #Milliseconds
    printf '%dms' $duration
  else if test $duration -lt 60000
    #Display seconds, w/ milliseconds as fraction of a second
    set -l seconds (math $duration / 1000)
    set -l milliseconds (math $duration '%' 1000)
    printf '%d.%03d' $seconds $milliseconds
  else
    #Display minutes:seconds, w/ milliseconds as fraction of a second
    set -l minutes (math $duration / 60000)
    set duration (math $duration '%' 60000)
    set -l seconds (math $duration / 1000)
    set -l milliseconds (math $duration '%' 1000)
    printf '%d:%02d.%03d' $minutes $seconds $milliseconds
  end
end

function start_segment -a bg_color fg_color
    set_color --background $bg_color
    set_color $fg_color
end

function end_segment -a bg_color fg_color next_color
    set_color --dim $bg_color
    set_color --background $next_color
    echo -n "$segment_separator "
end

function fish_prompt --description 'Write out the prompt'
    set -l last_status $status

    if test -n "$CMD_DURATION"
        set duration_str (_format_duration $CMD_DURATION)
    end

    start_segment $_prompt_time black

    set -l current_time (date "+%H:%M:%S")
    # Just calculate this once, to save a few cycles when displaying the prompt
    if not set -q __fish_prompt_hostname
        set -g __fish_prompt_hostname (hostname)
    end

    #Current time and, if present, last command exec time
    echo -n "[$current_time] "
    if test -n "$duration_str"
        printf '(%s)' $duration_str
    end
    set_color --background $fish_color_user
    end_segment $_prompt_time black $_prompt_user
    start_segment $_prompt_user black

    #User@host
    echo -n "$USER"
    echo -n "@"
    echo -n "$__fish_prompt_hostname"
    end_segment $_prompt_user black $_prompt_path
    start_segment $_prompt_path black

    # PWD
    echo -n (prompt_pwd)
    set_color normal
    set_color $_prompt_path
    echo -n "$segment_separator "

    #Status if last command failed
    if not test $last_status -eq 0
		set_color $fish_color_error
        echo -n "$error_section_open$last_status$error_section_close "
    end

    set_color normal
end
