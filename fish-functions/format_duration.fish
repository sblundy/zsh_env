function format_duration
  set -l duration $argv[1]


  #Select format depending on whether there are minutes, seconds, or just ms

  if test -z "$duration"
    #Special case of no duration
    echo -n '0'
  else if test $duration -eq 0
    #No duration
    echo -n '0'
  else if test $duration -lt 100
    #Milliseconds
    printf '%dms' $duration
  else if test $duration -lt 60000
    #Display seconds, w/ milliseconds as fraction of a second
    set -l seconds (math $duration / 1000)
    set -l milliseconds (math $duration '%' 1000)
    printf '%d.%03d' $seconds $milliseconds
  else
    set -l minutes (math $duration / 60000)
    set duration (math $duration '%' 60000)
    set -l seconds (math $duration / 1000)
    set -l milliseconds (math $duration '%' 1000)
    printf '%d:%02d.%03d' $minutes $seconds $milliseconds
  end
end
