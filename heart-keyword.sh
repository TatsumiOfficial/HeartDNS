#!/bin/bash

heartkeyword() {
    curl=$(curl -s "https://heartdns.com/API/keyword.php?s=$1" | jq -r '.domain[] | .[]')
    if [[ $curl == '' ]]; then
        echo -e "Failed Get Domain $1"
    else
        echo -e "Success Get Domain $1"
        echo "$curl" >> domain-result.txt
    fi
}

read -p "Select Your List : " listo;

IFS=$'\r\n' GLOBIGNORE='*' command eval 'list=($(cat $listo))'
for (( i = 0; i < "${#list[@]}"; i++ )); do
    AMPAS="${list[$i]}"
    IFS='' read -r -a array <<< "$AMPAS"
    target=${array[0]}
    heartkeyword ${target} &
done
wait
