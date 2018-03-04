function fish_right_prompt -d 'Write out the right prompt'
    if vcs.present
        if set -l vcs_name (vcs.name)
            set_color --bold green
            switch $vcs_name
                case git
                    echo '⎇ '
                case svn
                    echo 's '
                case hg
                    echo '☿ '
            end
        end
        if set -l dirty (vcs.dirty)
            set_color --bold red
            echo "± "
        end
        set -l branch_name (vcs.branch)
        set_color --bold yellow
        echo "$branch_name"
        set_color normal
    end
end
