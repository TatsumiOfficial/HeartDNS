#!/bin/bash

heartkeyword() {
    curl=$(curl -s "https://heartdns.com/API/keyword.php?s=$1" | jq -r '.domain[] | .[]')
    if [[ $curl == '' ]]; then
        echo -e "Failed Get Domain $keyword"
    else
        echo -e "Success Get Domain $keyword"
        echo "$curl" >> domain-result.txt
    fi
}

read -p "Enter your filename: " filename


if [[ ! -f $filename ]]; then
    echo "File not found: $filename"
    exit 1
fi

while read -r keyword; do
    heartkeyword "$keyword"
done < "$filename"
