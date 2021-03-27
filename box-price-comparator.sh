#! /usr/bin/env bash

##########################################################################
# Title      :  box-price-comparator.sh
# Author     :  Valgrut
# Date       :  25.03.2021
# Category   :  web scrapping, magic the gathering
##########################################################################
# Description
# 	Script goes through various online shops and parses the price of given booster boxes.
# 	
# Usage
#   ./deck-price-comparator.sh -k "spiral"  
##########################################################################

function show_help
{
    #TODO
	echo "Usage:"
	echo "	deck-url-transformator.sh [-h] [--deck-id DECK_ID] [--web cernyrytir|najada] [--deck-file FILE]"
}

function get_info_about_card_cernyrytir
{
	card_url="$1"
	card_name="$2"
	web_curl=$(curl -s "$card_url")
	#price=$(echo "$web_curl" | grep -F -A 20 ">$card_name</font>" | grep -o -E "bolder;\">8&nbsp;K<" | grep -o -E '[0-9]+')
	price=0
	availability=$(echo "$web_curl" | grep -F -A 20 ">$card_name</font>" | grep -o -E "[0-9]+\&nbsp;ks" | grep -o -E '[0-9]+')
	echo "$card_name, ks: $availability, price: $price Kc"
}

# A POSIX variable
OPTIND=1  # Reset in case getopts has been used previously in the shell.

# Initialize our own variables:
search_key="" #i.e. "remastered"
target_web="cernyrytir"
verbose=0
product="box|display" #default

#while getopts "h?dwf:" opt; do
while [[ "$#" -gt 0 ]]; do
	case $1 in
		-h|--help)
			show_help
			exit 0
			;;
		-k|--key)  search_key="$2"; shift
			;;
		# -p|--product)  product="$2"; shift
			# ;;
		*) echo "Unknown parameter passed: $1"; exit 1
			;;
	esac
	shift
done
# echo $card_list_file $deck_id $target_web


########
# box
# web cena dostupnost
# ===================
# abc 1444 3
# xtx ?    ?

declare -A web_prices

najada_url="https://www.najada.cz/cz/eshop/ostatni-zbozi/?Type=4#"
veselydrak_url="https://www.vesely-drak.cz/produkty/booster-box/"
blacklotus_url="https://www.blacklotus.cz/draft-booster-box--time-spiral-remastered/"
kalel_url="https://store.kal-el.cz/subdom/store/mtg/booster-box"
cernyrytir_url="https://www.cernyrytir.cz/index.php3?akce=100&sekce=mtg&podsekce=display"
rishada_url="https://www.rishada.cz/mtg/displaye"
fantasyobchod_url="https://www.fantasyobchod.cz/magic-the-gathering-booster-boxy"

function parse_najada
{
	web_curl=$(curl -s $najada_url)
    price=$(echo "$web_curl" | grep -E -A 20 "$search_key" | grep -E -A 20 "$product" | grep -E '<span class="price"><span class="v">' | grep -o -E "[0-9]+ ?[0-9]+")
    web_prices["najada.cz"]="$price"
}

function parse_veselydrak
{
	web_curl=$(curl -s $veselydrak_url)
    price=$(echo "$web_curl" | grep -E -A 10 "$search_key" | grep -E -A 10 "$product" | grep -E '<span class="price">' | grep -o -E "[0-9]+ ?[0-9]+")
    web_prices["vesely-drak.cz"]="$price"
}

function parse_blacklotus
{
	web_curl=$(curl -s $blacklotus_url)
    price=$(echo "$web_curl" | grep -E "priceWithVat\":" | grep -o -E "[0-9]+")
    web_prices["blacklotus.cz"]="$price"
}

function parse_kal_el
{
	web_curl=$(curl -s $kalel_url)
    price=$(echo "$web_curl" | grep -E -A 10 "$search_key" | grep -E -A 10 "$product" | grep -E -A 1 '<div class="price">' | grep -E -o "[0-9]+ [0-9]+")
    if [[ price -eq "" ]]; then
        price="none"
    fi
    web_prices["kal-el.cz"]="$price"
}

function parse_cernyrytir
{
	web_curl=$(curl -s $cernyrytir_url)
    price=$(echo "$web_curl" | grep -E -a -i -m 1 -A 5 "$search_key" | grep -E -i -a -A 5 "$product" | grep -a -E -o '[0-9]+.?[0-9]*.?K' | grep -a -E -o "[0-9]+")
    web_prices["cernyrytir.cz"]="$price"
}

function parse_rishada
{
	web_curl=$(curl -s $rishada_url)
    price=$(echo "$web_curl" | grep -E -A 3 "$search_key" | grep -E -A 3 "$product" | grep -E -o -A 1 '<div class="item-price">.{10}'  | grep -E -o "[0-9]+ ?[0-9]+")
    web_prices["rishada.cz"]="$price"
}

function parse_fantasyobchod
{
	web_curl=$(curl -s $fantasyobchod_url)
    price=$(echo "$web_curl" | grep -E -A 20 "$search_key" | grep -E -A 20 "$product" | grep -o -P ".{0,8}<span class='currency-right'"  | grep -E -o "[0-9]+ ?[0-9]+")
    web_prices["fantasyobchod.cz"]="$price"
}


echo "Searching for '$product' and key '$search_key'."
echo "Web    | price"
echo "----------------"
parse_najada
parse_veselydrak
parse_blacklotus
parse_kal_el
parse_cernyrytir
parse_rishada
parse_fantasyobchod

for key in "${!web_prices[@]}"; do
    echo "$key | ${web_prices[$key]} Kc"
done

