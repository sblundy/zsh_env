if test -z "$PLANS_HOME"
    set -l ORG_PWD (pwd)
    set PLANS_HOME (cd (dirname (status --current-filename)); and pwd)
    cd $ORG_PWD
end

if test -z "$PLANS_DIR"
    set PLANS_DIR "$HOME/plans"
end

function plan --description='Daily planning util'
    set -l action $argv[1]

    if test -z "$action"
        set action 'current'
    end

    set -l filename_basename (date '+%Y-%m-%d')
    set -l filename "$PLANS_DIR/$filename_basename.plan"

    switch $action
        case create
            set -l default_file_name "Default"
            if set -q argv[2]
                set default_file_name $argv[2]
            else if not test -e "$PLANS_DIR/Default.plan"
                touch $filename
                return 0
            end

            set -l default_file "$PLANS_DIR/$default_file_name.plan"
            if not test -e "$default_file"
                echo "Error: $default_file does not exist" 1>&2
                return 1
            else
                cp "$default_file" $filename
            end
        case set replan rm
            if not test -e "$filename"
                echo "Today's plan hasn't been initialized" 1>&2
                return 1
            end
            cp $filename "$filename.bk"
            command python3 "$PLANS_HOME/plan.py" $filename $action $argv[2..-1]
            command python3 "$PLANS_HOME/plan.py" $filename current
        case '*'
            if not test -e "$filename"
                echo "Today's plan hasn't been initialized" 1>&2
                return 1
            end
            test 1 -lt (count $argv)
            and set -l CMD_ARGS $filename $action $argv[2..-1]
            or set -l CMD_ARGS $filename $action
            command python3 "$PLANS_HOME/plan.py" $CMD_ARGS
    end
end

function __plan_needs_command
    set -l cmd (commandline -opc)

    if test $cmd[-1] = 'plan'
        return 0
    else
        return 1
    end
end

function __plan_using_command
    set -l name $argv[1]
    set -l cmd (commandline -opc)

    if test $cmd[2] = $name
        return 0
    else
        return 1
    end
end

function __plan_available_templates -d "description"
    for plan_file in (ls $PLANS_DIR/*.plan)
        if basename "$plan_file" | grep -q -v -E '20[[:digit:]]{2}-[01][[:digit:]]-[0123][[:digit:]].plan'
            string replace '.plan' '' (basename "$plan_file")
        end
    end
end

complete -f -c plan
complete -f -c plan -n '__plan_needs_command' -a 'create'
complete -f -c plan -n '__plan_using_command create' -a '(__plan_available_templates)'

complete -f -c plan -n '__plan_needs_command' -a 'current'
complete -f -c plan -n '__plan_needs_command' -a 'list'
complete -f -c plan -n '__plan_needs_command' -a 'replan'
complete -f -c plan -n '__plan_needs_command' -a 'set'
complete -f -c plan -n '__plan_needs_command' -a 'rm'
