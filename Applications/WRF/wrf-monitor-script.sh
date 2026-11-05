#!/bin/bash
# this is a monitoring script to be run with wrf that periodically (per PERIOD) reads the wrf logs
# and estimates how much time the full simulation will take.
# make sure to redirect wrf output to a logfile and set the file path properly. 

# these are just estimates, don't trust them too much. 

JOB_NAME="WRF: Polar vortex simulation"
PERIOD=1
INPUT=~/spack-v1/spack/opt/spack/linux-sapphirerapids/wrf-4.7.1-tq5cmx47ctjvfofvivcwqmgray6uv7ya/test/em_real/namelist.input
FILE=~/spack-v1/spack/opt/spack/linux-sapphirerapids/wrf-4.7.1-tq5cmx47ctjvfofvivcwqmgray6uv7ya/test/em_real/logfile.txt
MINS_SINCE_START=104 # how many minutes ago it started (use htop to look at the longest running process)
WRFSTART=$(($(date +%s) - (MINS_SINCE_START * 60)))


nl_get() {
    awk -F= -v key="$1" '
        $1 ~ "^[ \t]*" key "[ \t]*$" {
            split($2, a, ",")
            gsub(/[ \t]/, "", a[1])
            print a[1]
            exit
        }' "$INPUT"
}

cleanup() {
	tput cnorm
	exit 0
}

trap cleanup INT TERM EXIT

start_year=$(nl_get start_year)
start_month=$(nl_get start_month)
start_day=$(nl_get start_day)
start_hour=$(nl_get start_hour)

end_year=$(nl_get end_year)
end_month=$(nl_get end_month)
end_day=$(nl_get end_day)
end_hour=$(nl_get end_hour)

printf -v start_time '%04d-%02d-%02d_%02d:%02d:%02d' \
    "$((10#$start_year))" "$((10#$start_month))" "$((10#$start_day))" \
    "$((10#$start_hour))" "00" "00"

printf -v end_time '%04d-%02d-%02d_%02d:%02d:%02d' \
    "$((10#$end_year))" "$((10#$end_month))" "$((10#$end_day))" \
    "$((10#$end_hour))" "00" "00"

echo "start: $start_time"
echo "end:   $end_time"

to_epoch() { date -d "${1/_/ }" +%s; }

start_epoch=$(to_epoch "$start_time")
end_epoch=$(to_epoch "$end_time")

model_total=$((end_epoch - start_epoch))

re='time ([^ ]+) on domain +([0-9]+): +([0-9.]+) elapsed'

tput sc
tput civis

while true; do
    line=$(tail -n 500 "$FILE" | grep 'Timing for main' | tail -n 1)
    tput clear
    if [[ $line =~ $re ]]; then
        timestamp=${BASH_REMATCH[1]}
        domain=${BASH_REMATCH[2]}

        now_epoch=$(to_epoch "$timestamp")
        model_elapsed=$((now_epoch - start_epoch))
        rhs=$((end_epoch - start_epoch))
        pct=$(((100 * model_elapsed) / rhs))
            echo "timestamp=$timestamp domain=$domain, progress: $pct%"
    fi

    right_now=$(date +%s)
    elapsed_time=$((right_now - WRFSTART)) # wall time that has passed
    mult=$(echo "scale=4; 100 / $pct" | bc)
    projected_time=$(echo "scale=4; ($elapsed_time * $mult) / 60" | bc)

    remaining_time=$(( elapsed_time * (model_total - model_elapsed) / model_elapsed )) # in seconds, how much time to we project to be left
    finish_epoch=$((right_now + remaining_time))
    
    if [ "$remaining_time" -le 0 ]; then 
		exit 0 
	fi

    tput setab 4
    echo $JOB_NAME
    tput sgr0

    echo "Elapsed: $(($elapsed_time / 60 )) minutes"
    echo "Projected total time: $(( (elapsed_time + remaining_time) / 60 )) minutes"
    echo "Time remaining: $(( remaining_time / 60)) minutes" 
    tput bold
    echo "Projected finish at $(date -d @"$finish_epoch" '+%Y-%m-%d %H:%M:%S')"

    tput sgr0
    sleep $PERIOD
done