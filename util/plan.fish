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

    set -l filename (__plan_current_file)

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
            command python3 "$PLANS_HOME/plan.py" $filename current
        case import
            cp $filename "$filename.bk"
            for event in (icalBuddy -ea -npn -nc -iep 'datetime,title' -b '' -ps "|\t|" eventsToday)
                set -l event_props (string split \x09 $event)
                command python3 "$PLANS_HOME/plan.py" $filename set $event_props[2] $event_props[1]
            end
            command python3 "$PLANS_HOME/plan.py" $filename current
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

function __plan_current_file
    set -l filename_basename (date '+%Y-%m-%d')
    echo "$PLANS_DIR/$filename_basename.plan"
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

function __plan_available_templates
    for plan_file in (ls $PLANS_DIR/*.plan)
        if basename "$plan_file" | grep -q -v -E '20[[:digit:]]{2}-[01][[:digit:]]-[0123][[:digit:]].plan'
            string replace '.plan' '' (basename "$plan_file")
        end
    end
end

function __plan_all_versions
    set -l max_version 0
    set -l filename (__plan_current_file)
    while read -la line
        set -l tabs_only (echo "$line" | sed 's/[^\t]//g')
        set -l line_len (string length "$tabs_only")
        if test $line_len -gt $max_version
            set max_version $line_len
        end
    end < "$filename"
    seq $max_version
end

complete -f -c plan
complete -f -c plan -n '__plan_needs_command' -a 'create'
complete -f -c plan -n '__plan_using_command create' -a '(__plan_available_templates)'

complete -f -c plan -n '__plan_needs_command' -a 'import'
complete -f -c plan -n '__plan_needs_command' -a 'current'
complete -f -c plan -n '__plan_needs_command' -a 'list'
complete -f -c plan -n '__plan_using_command list' -a '(__plan_all_versions)'

complete -f -c plan -n '__plan_needs_command' -a 'replan'
complete -f -c plan -n '__plan_needs_command' -a 'set'
complete -f -c plan -n '__plan_needs_command' -a 'rm'
