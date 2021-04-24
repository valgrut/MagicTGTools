#! /usr/bin/env bash

# test output url for all shops and compare them with reviewed reference output urls.

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

shops=( 'cernyrytir' 'najada' 'rishada' 'magicshop' 'blacklotus')
for shop in ${shops[@]}; do
    ../deck-url-translator.sh -f testdecks/test_deck.txt -w $shop > $shop-output.txt
    diff_out=$(diff $shop-output.txt $shop-ref-output.txt)
    rc=$?
    
    if [[ $rc == 0 ]]; then
        echo -e "${GREEN}PASS${NC} ($rc) $shop"
    else
        echo -e "${RED}FAIL${NC} ($rc) $shop"
    fi
    
    rm "$shop-output.txt"
done
