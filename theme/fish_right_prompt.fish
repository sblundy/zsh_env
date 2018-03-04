function fish_right_prompt -d 'Write out the right prompt'
	set -l git_prompt (__fish_git_prompt "%s")

	if test -n "$git_prompt"
		echo -n "$git_prompt"
	end
end
