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
    case '*'
        if test $action = 'set' or test $action = 'replan'
            cp $filename "$filename.bk"
        end
        command python3 "$PLANS_HOME/plan.py" $filename $action $argv[2..-1]
    end
end