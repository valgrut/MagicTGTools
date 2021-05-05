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
    modified_name = re.sub("( \([0-9a-zA-Z]{1,6}\))?( [0-9]{1,5})?$", "", card_name)
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
    urlencoded = quote(card_name, encoding="cp1250")
    # return urlencoded.replace("%C2%B4", "%B4")
    return urlencoded


def encode_card_name_as_url_plus(card_name):
    urlencoded = quote_plus(card_name, encoding="utf-8")
    return urlencoded

####################################################

deck = open("deck.txt", "r")
for card in deck:
    if comment_detected(card):
        continue
    card = strip_initial_digits(card)
    card = strip_set_and_ending_num(card)
    card = strip_end_of_line_chars(card)
    cr_card = encode_card_name_as_url(card)
    others_card = encode_card_name_as_url_plus(card)
    # print(f"'{card}'")
    # print(f"http://cernyrytir.cz/index.php3?akce=3&searchtype=card&searchname={cr_card}")
    
    # print(f"'{others_card}'")
    print(f"https://www.najada.cz/cz/kusovky-mtg/?Anchor=EShopSearchArticles&RedirUrl=https%3A%2F%2Fwww.najada.cz%2F&Search={others_card}&Sender=Submit&MagicCardSet=-1#")
