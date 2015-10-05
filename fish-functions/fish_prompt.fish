function fish_prompt --description 'Write out the prompt'
	set -l last_status $status

	if test -n "$CMD_DURATION"
		set duration_str (format_duration $CMD_DURATION)
	end

	set -l current_time (date "+%H:%M:%S")
	# Just calculate this once, to save a few cycles when displaying the prompt
	if not set -q __fish_prompt_hostname
		set -g __fish_prompt_hostname (hostname)
	end

	#Current time and, if present, last command exec time
	echo -n "[$current_time] "
	if test -n "$duration_str"
		printf '(%s) ' $duration_str
	end

	#User@host
  set_color $fish_color_user
	echo -n "$USER"
  set_color normal
	echo -n "@"
	set_color $fish_color_host
	echo -n "$__fish_prompt_hostname "
	set_color normal

	# PWD
	set_color $fish_color_cwd
	echo -n (prompt_pwd)
	set_color normal

	#Status if last command failed
	if not test $last_status -eq 0
		set_color $fish_color_error
		echo -n " [$last_status]"
		set_color normal
	end

	echo -n " > "
end
