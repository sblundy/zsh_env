function fish_right_prompt -d 'Write out the right prompt'

	if not set -q fish_color_vcs_branch
		set -g fish_color_vcs_branch yellow
	end

	set -l git_prompt (__fish_git_prompt "%s")

	if test -n "$git_prompt"
		set_color $fish_color_vcs_branch
		echo -n '♈ '
		set_color normal
		echo -n "$git_prompt"
	end
#	set_color normal
end
