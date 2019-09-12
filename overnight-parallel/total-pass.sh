# count the total number of tests passed and total number of instructions executed

find . -name 'log.txt' | xargs cat | grep pass | awk '{t+=$2; i+=$4}END{print t, i}'
