import re
import urllib3
from urllib.parse import quote
from urllib.parse import quote_plus

# TODO Prozkoumat jestli se to nebude hodit.
#from urllib import urlopen
#import nltk

## TOTO je modul pro parsovani nazvu karet ve stazenem balicku.
## Bude pouzit jak pro flask web app, tak pro desktop / CLI appku.

# variable accessible as modulename.variable
somevariable = 42


def strip_initial_digits(card_name):
    modified_name = re.sub("^([0-9]{1,3} )?", "", card_name)
    return modified_name


def strip_set_and_ending_num(card_name):
    modified_name = re.sub("(\s*$)?( \([0-9a-zA-Z]{1,6}\))?( [0-9]{1,5})?$", "", card_name)
    return modified_name


def strip_end_of_line_chars(card_name):
    modified_name = re.sub(r"\n", "", card_name)
    return modified_name


def comment_detected(card_name):
    match = re.search("^\s*#", card_name)
    if match is None:
        return False
    else:
        return True


def encode_card_name_as_url(card_name):
    # https://www.w3schools.com/tags/ref_urlencode.ASP
    card_name = re.sub(r"'", "´", card_name) # additional char exchange for cernyrytir
    urlencoded = quote(card_name, encoding="cp1250")
    # return urlencoded.replace("%C2%B4", "%B4")
    return urlencoded


def encode_card_name_as_url_plus(card_name):
    urlencoded = quote_plus(card_name, encoding="utf-8")
    return urlencoded


def clean_cardname(card):
    '''
    in: '3 Aether Tunnel (A3E0) 123\n'
    out: 'Aether Tunnel'
    '''
    processed_card = card
    processed_card = strip_initial_digits(processed_card)
    processed_card = strip_set_and_ending_num(processed_card)
    processed_card = strip_end_of_line_chars(processed_card)
    return processed_card


# def encode_cardname_for_web(card, target_web)
#     encoded = ""
#     if target_web == "cernyrytir":
#         encoded = encode_card_name_as_url(card)
#     else: #najada, rishada, blacklotus
#         encoded = encode_card_name_as_url_plus(card)
#     return encoded


def process_deck(deckfile, target_web):
    urls = []

    fdeck = open(deckfile, "r")
    for line in fdeck:
        if comment_detected(line):
            continue

        cleaned_card_name = clean_cardname(line)

        card_url = ""
        if target_web == "cernyrytir":
            encoded = encode_card_name_as_url(cleaned_card_name)
            card_url = f"http://cernyrytir.cz/index.php3?akce=3&searchtype=card&searchname={encoded}"

        elif target_web == "najada":
            encoded = encode_card_name_as_url_plus(cleaned_card_name)
            card_url = f"https://www.najada.cz/cz/kusovky-mtg/?Anchor=EShopSearchArticles&RedirUrl=https%3A%2F%2Fwww.najada.cz%2F&Search={encoded}&Sender=Submit&MagicCardSet=-1#"

        elif target_web == "blacklotus":
            encoded = encode_card_name_as_url_plus(cleaned_card_name)
            card_url = f"https://www.blacklotus.cz/vyhledavani/?string={encoded}"
            # echo -e '\e]8;;https://www.blacklotus.cz/vyhledavani/?string='$najadamodified'\a'$cardname'\e]8;;\a'
            pass

        elif target_web == "rishada":
            encoded = encode_card_name_as_url_plus(cleaned_card_name)
            card_url = f"https://rishada.cz/hledani?fulltext={encoded}"
            # echo -e '\e]8;;https://rishada.cz/hledani?fulltext='$najadamodified'\a'$cardname'\e]8;;\a'

        else: #mysticshop
            pass

        urls.append((cleaned_card_name, card_url))
        print((cleaned_card_name, card_url))
    fdeck.close()
    return urls

