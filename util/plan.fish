if test -z "$PLANS_HOME"
    set -l ORG_PWD (pwd)
    set PLANS_HOME (cd (dirname (status --current-filename)); and pwd)
    cd $ORG_PWD
end

function plan --description='Daily planning util'
    set -l action $argv[1]
    set -l plans_dir "$HOME/plans"

    if test -z "$action"
        set action 'current'
    end

    set -l filename_basename (date '+%Y-%m-%d')
    set -l filename "$plans_dir/$filename_basename.plan"

    switch $action
    case create
        if test -e "$plans_dir/Default.plan"
            cp "$plans_dir/Default.plan" $filename
        else
            touch $filename
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
        test 1 -lt (count $argv); and set -l CMD_ARGS $filename $action $argv[2..-1]; or set -l CMD_ARGS $filename $action
        echo $CMD_ARGS
        command python3 "$PLANS_HOME/plan.py" $CMD_ARGS
    end
end