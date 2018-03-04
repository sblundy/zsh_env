function fish_right_prompt -d 'Write out the right prompt'
    if vcs.present
        if set -l dirty (vcs.dirty)
            set_color --bold red
            echo -n "± "
        end
        if set -l vcs_name (vcs.name)
            set_color --bold green
            switch $vcs_name
                case git
                    # TODO find better symbol
                    echo -n 'ɤ '
                case svn
                    echo -n 's '
                case hg
                    echo -n '☿ '
            end
        end

        set -l vcs_status (vcs.status)
        switch "$vcs_status"
            case ahead
                set_color --bold yellow
                echo -n '↑ '
            case behind
                set_color --bold yellow
                echo -n '↓ '
            case diverged
                set_color --bold yellow
                echo -n '⇅ '
            case detached
                set_color --bold red
                echo -n '╳ '
            case clean
                set_color green
                echo -n '✓ '
        end
        set -l branch_name (vcs.branch)
        set_color --bold yellow
        echo -n "($branch_name)"
        set_color normal
    end
end
