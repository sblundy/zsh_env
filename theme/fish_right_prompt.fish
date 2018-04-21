set -q _prompt_gopath_color
                or set _prompt_gopath_color magenta

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

    if test -n "$GOPATH"
        echo -n ' '
        switch $PWD
        case "$GOPATH"
            set_color --bold $_prompt_gopath_color
            echo -n  '.'
        case "$GOPATH*"
            set -l TMP_DIR "$PWD"
            set -l GOPATH_MSG ""
            while test $TMP_DIR != $GOPATH
                set TMP_DIR (dirname $TMP_DIR)
                set GOPATH_MSG "../$GOPATH_MSG"
            end
            set_color --bold $_prompt_gopath_color
            echo -n "$GOPATH_MSG"
        case "*"
            set_color $_prompt_gopath_color
            echo -n \uE0B2
            set_color black
            set_color --background $_prompt_gopath_color
            set realhome ~
            set -l tmp_gopath (string replace -r '^'"$realhome"'($|/)' '~$1' $GOPATH)
            set -q gopath_dir_length
                or set -l gopath_dir_length 1
            string replace -ar '(\.?[^/]{'"$gopath_dir_length"'})[^/]*/' '$1/' "$tmp_gopath"
        end

        set_color normal
    end
end
