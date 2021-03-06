#! /usr/bin/env bash

##########################################################################
# Title      :  deck-url-translator.sh
# Author     :  Jiri Peska
# Date       :  16.02.2021
# Category   :  URL generator, web, magic the gathering
# Repository :  https://github.com/valgrut/MagicTGTools
##########################################################################
# Description
# 	Script that prints direct urls to cards from list.
# 	Script is able to download list of cards by deck ID from mtggoldfish and generate urls for cernyrytir.cz
#
# 	Script expects following columnt format:
# 		| Num | CardName |
#
# Usage
#
##########################################################################

set -euo pipefail

# TODO Pridat testy dle testovacich karet. Pridat do testovacich karet karty v noven formatu. generovani pro najadu a rytire.
# TODO u najady je problem ze odkaz je klikatelny pouze po znaky ' nebo ( nebo )
# TODO list cards that could not be found and where search failed or was unsuccesful
# TODO add option that activates direct transformation from deckid and print of urls
# TODO add option print prices and availability in given store by parsing html code from curl.
# TODO add option to compare prices and availability in stores

# TODO TODO: Pridat sumu ceny - budu muset naparsovat vsechny karty a zjistit nejlevnejsi verzi a tu zahrnout do vypoctu.

# Najada:
# https://stackoverflow.com/questions/296536/how-to-urlencode-data-for-curl-command
# https://www.w3schools.com/tags/ref_urlencode.ASP
# URL encoding:
#  '"' = %22
#  ''' = %27
#######################################################################################

function show_help
{
    echo "Usage:"
    echo "	deck-url-transformator.sh [-h|--help] [-d|--deck-id| DECK_ID] [-w|--web cernyrytir|najada] [-f|--deck-file FILE] [-o|--open]"
}

# Function that encodes card name into url-valid form
function urlencode_card_name
{
    echo "$1" | sed -e 's/^[ \t]*//' | tr -d '\n' | jq -sRr @uri
}

# Functions modifying the url for "cernytyrir" search
function modify_card_url_for_cernyrytir
{
    # mapping
    # array=( "s/%C2%B4/%B4/g" )
    # or
    # array["%C2%B4"] = "%B4"
    # for mapping in array:
    #   echo $1 | sed "s/$mapping/array[$mapping]/g"
    echo "$1" | sed "s/%C2%B4/%B4/g" | sed "s/'/%B4/g" | sed "s/(/%28/g" | sed "s/)/%29/g" | sed "s/\?/%3F/g" | sed "s/!/%21/g"
}

function modify_card_url_for_najada
{
    echo "$1" | sed "s/%20/+/g"
}

# Function that checks format of given line of processed list.
function check_format
{
    if echo "$1" | awk '{print $0}' | grep -E -v '^[0-9]+'; then
        return 1
    fi

    # Ok, contains number at first columnt
    return 0
}

# Detect new format of deck list (from tappedout or mtggoldfish)
function contains_edition
{
    if echo "$1" | awk '{print $0}' | grep -q -E -v '\( [a-zA-Z0-9]{2,7}\)?( [0-9]{1,4})?$'; then
        # string does not contain edition and number
        return 0
    fi
    return 1
}

function strip_edition
{
    echo "$1" | sed -r 's/ \([a-zA-Z0-9]{3,7}\) ?[0-9]{0,4}//'
}

function detect_comment_line
{
    # If Not a comment
    if echo "$1" | awk '{print $0}' | grep -q -E -v '^#'; then
        return 0
    fi

    # Comment detected
    return 1
}

# Function that generates urls for given website from list of cards in provided file
function process_deck
{
    input="$1" #deck file with card list

    if [[ $export_as_html == 1 ]]; then
        start_html "$input"
    fi

    LINE_CNT=1
    if [ -f "$input" ]; then
        while IFS= read -r line
        do
            # Skip lines that start with #
            if ! detect_comment_line $line; then
                continue
            fi

            if ! check_format $line; then
                echo "Error: First word on line $LINE_CNT is not numeric. ($line)"
                continue
            fi

            cardname="$(echo $line | sed 's/^[0-9]* //g')"

            # Check if card version and edition is at the end
            if contains_edition "$cardname"; then
                # Remove edition and number from card name
                cardname=$(strip_edition "$cardname")
            fi

            # cernyrytir
            encoded=$(urlencode_card_name "$cardname")
            if [[ $target_web == "cernyrytir" ]]; then
                modified=$(modify_card_url_for_cernyrytir "$encoded")
                card_url="http://cernyrytir.cz/index.php3?akce=3&searchtype=card&searchname=$modified"
                if [[ $show_info -eq 1 ]]; then
                    get_info_about_card_cernyrytir "$card_url" "$cardname"
                else
                    if [[ $open_in_browser == 0 ]]; then
                        if [[ $print_url == 1 ]]; then
                            #echo "${card_url: : -3}" #remove last 3 characters
                            echo "$card_url"
                        else
                            echo -e '\e]8;;http://cernyrytir.cz/index.php3?akce=3&searchtype=card&searchname='$modified'\a'$cardname'\e]8;;\a'
                        fi
                        if [[ $export_as_html == 1 ]]; then
                            insert_html_card_link "$input" "$cardname" "$card_url"
                        fi
                    else
                        firefox -new-tab "$card_url"
                    fi
                fi
            fi

            # najada
            if [[ $target_web == "najada" ]]; then
                najadamodified=$(modify_card_url_for_najada "$encoded")
                if [[ $open_in_browser == 0 ]]; then
                    if [[ $print_url == 1 ]]; then
                        echo "https://www.najada.cz/cz/kusovky-mtg/?Anchor=EShopSearchArticles&RedirUrl=https%3A%2F%2Fwww.najada.cz%2F&Search=$najadamodified&Sender=Submit&MagicCardSet=-1#"
                    else
                        echo -e '\e]8;;https://www.najada.cz/cz/kusovky-mtg/?Anchor=EShopSearchArticles&RedirUrl=https%3A%2F%2Fwww.najada.cz%2F&Search='$najadamodified'&Sender=Submit&MagicCardSet=-1#"\a'$cardname'\e]8;;\a'
                    fi
                    if [[ $export_as_html == 1 ]]; then
                        insert_html_card_link "$input" "$cardname" "$card_url"
                    fi
                else
                    firefox -new-tab "https://www.najada.cz/cz/kusovky-mtg/?Anchor=EShopSearchArticles&RedirUrl=https%3A%2F%2Fwww.najada.cz%2F&Search=$najadamodified&Sender=Submit&MagicCardSet=-1#"
                fi
            fi

            # black lotus
            if [[ $target_web == "blacklotus" ]]; then
                najadamodified=$(modify_card_url_for_najada "$encoded")
                if [[ $open_in_browser == 0 ]]; then
                    if [[ $print_url == 1 ]]; then
                        echo "https://www.blacklotus.cz/vyhledavani/?string=$najadamodified"
                    else
                        echo -e '\e]8;;https://www.blacklotus.cz/vyhledavani/?string='$najadamodified'\a'$cardname'\e]8;;\a'
                    fi
                    if [[ $export_as_html == 1 ]]; then
                        insert_html_card_link "$input" "$cardname" "$card_url"
                    fi
                fi
            fi

            # rishada
            if [[ $target_web == "rishada" ]]; then
                najadamodified=$(modify_card_url_for_najada "$encoded")
                if [[ $open_in_browser == 0 ]]; then
                    if [[ $print_url == 1 ]]; then
                        echo "https://rishada.cz/hledani?fulltext=$najadamodified"
                    else
                        echo -e '\e]8;;https://rishada.cz/hledani?fulltext='$najadamodified'\a'$cardname'\e]8;;\a'
                    fi
                    if [[ $export_as_html == 1 ]]; then
                        insert_html_card_link "$input" "$cardname" "$card_url"
                    fi
                fi
            fi

            # mysticshop.cz
            # TODO

            (( LINE_CNT++ ))

        done < "$input"

    else
        echo "Error: File $input does not exist."
    fi

    if [[ $export_as_html == 1 ]]; then
        end_html "$input"
    fi
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

function generate_urls
{
    deck="$1"

    # If file has been created in windows, file is formatted differently.
    # Convert file into unix format to get rid of ^M (ctrl+m) at the end of a line
    # https://www.suse.com/support/kb/doc/?id=000018317
    dos2unix -q "$deck"
    process_deck "$deck"
}

function start_html
{
    # gen html and body tags
    deck_name="$1"
    touch "$deck_name.html"
    # Note: Quoting "END" will cause variables and commands to not expand
    cat <<- END > "$deck_name.html"
<html>
<head>
<title>$deck_name</title>
</head>
<body>
<h3>$deck_name</h3>
<ul>
END
}

function end_html
{
    deck_name="$1"
    cat <<- END >> "$deck_name.html"
</ul>
</body>
</html>
END
}

function insert_html_card_link
{
    html_file="$1.html"
    card_name="$2"
    card_link="$3"
    echo "<li><a href='$card_link'>$card_name</a></li>" >> "$html_file"
}


# A POSIX variable
OPTIND=1  # Reset in case getopts has been used previously in the shell.

# Initialize our own variables:
card_list_file=""
deck_id=""
target_web="cernyrytir" #Default
show_info=0
verbose=0
open_in_browser=0
print_url=0
DEBUG=0
export_as_html=0

# https://stackoverflow.com/questions/192249/how-do-i-parse-command-line-arguments-in-bash
while [[ "$#" -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        -d|--deck_id)  deck_id="$2"; shift
            ;;
        -D|--DEBUG)  DEBUG=1;
            ;;
        -w|--web)  target_web="$2"; shift
            ;;
        -e|--html)  export_as_html="1";
            ;;
        -u|--url)  print_url="1";
            ;;
        -f|--file)  card_list_file="$2"; shift
            ;;
        -i|--info)  show_info=1; shift
            ;;
        -o|--open)  open_in_browser=1; shift
            ;;
        *) echo "Unknown parameter passed: $1"; exit 1
            ;;
    esac
    shift
done

# Input is local file with card list
if [[ -f "$card_list_file" && $deck_id -eq "" ]]; then
    generate_urls "$card_list_file"
    exit 0
else
    echo "Soubor $card_list_file nebyl nalezen."
    exit 1
fi

# Download deck (card list) from mtggoldfish.com by deck ID
# If provided param is number (deck ID from mtggoldfish.com)
if echo "$deck_id" | grep -qE '^[0-9]+$'; then
    # echo "Downloading card list of deck $deck_id"
    # Save card list into file
    curl https://www.mtggoldfish.com/deck/download/$deck_id | tee $deck_id.txt

    generate_urls "$deck_id.txt"

    exit 0
else
    echo "Error: Wrong format of deck ID. Only numbers allowed."
    exit 1
fi

