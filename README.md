# MagicTGTools
Tools for Magic the Gathering related tasks.

Chces-li si koupit commander deck nakupem jednotlivych karet, tak v nejakem stadiu musis kazdou kartu zadat do vyhledavani na prislusnem obchodu. Coz pro desitky karet muze byt docela nudna prace. Tento skript ti umozni ze seznamu karet, ktery ziskas na webech jako tappedout nebo mtggoldfish, vygenerovat seznam url, na ktere pak staci jen ctrl+klik-nout a rovnou se ocitnes na strance karty.

Skript vygeneruje odkazy pro vsechny karty v seznamu.

## deck-url-transformator.sh
Tento skript prevede vstupni list karet na url adresy pro obchody cernyrytir.cz nebo najada.cz

Priklad vstupniho souboru 'deck.txt':
```
1 Auramancer's Guise
1 Authority of the Consuls
1 Baird, Steward of Argive
1 Beastmaster's Magemark
1 Benevolent Unicorn
1 Blazing Archon
1 Capashen Unicorn
1 Cartouche of Knowledge
1 Cartouche of Strength
1 Chamber of Manipulation
1 Circle of Protection: Artifacts
1 Circle of Protection: Black
```

Skript vygeneruje z tohoto seznamu seznam url pomoci:
```
deck-url-transformator.sh -f deck.txt
```

Vystup pro **cernyrytir**:
```
http://cernyrytir.cz/index.php3?akce=3&searchtype=card&searchname=Auramancer%B4s%20Guise
http://cernyrytir.cz/index.php3?akce=3&searchtype=card&searchname=Authority%20of%20the%20Consuls
http://cernyrytir.cz/index.php3?akce=3&searchtype=card&searchname=Baird%2C%20Steward%20of%20Argive
http://cernyrytir.cz/index.php3?akce=3&searchtype=card&searchname=Beastmaster%B4s%20Magemark
http://cernyrytir.cz/index.php3?akce=3&searchtype=card&searchname=Benevolent%20Unicorn
http://cernyrytir.cz/index.php3?akce=3&searchtype=card&searchname=Blazing%20Archon
http://cernyrytir.cz/index.php3?akce=3&searchtype=card&searchname=Capashen%20Unicorn
http://cernyrytir.cz/index.php3?akce=3&searchtype=card&searchname=Cartouche%20of%20Knowledge
http://cernyrytir.cz/index.php3?akce=3&searchtype=card&searchname=Cartouche%20of%20Strength
http://cernyrytir.cz/index.php3?akce=3&searchtype=card&searchname=Chamber%20of%20Manipulation
http://cernyrytir.cz/index.php3?akce=3&searchtype=card&searchname=Circle%20of%20Protection%3A%20Artifacts
http://cernyrytir.cz/index.php3?akce=3&searchtype=card&searchname=Circle%20of%20Protection%3A%20Black
```

Vystup pro **najada**:
```
https://www.najada.cz/cz/kusovky-mtg/?Anchor=EShopSearchArticles&RedirUrl=https%3A%2F%2Fwww.najada.cz%2F&Search=Auramancer's+Guise&Sender=Submit&MagicCardSet=-1#
https://www.najada.cz/cz/kusovky-mtg/?Anchor=EShopSearchArticles&RedirUrl=https%3A%2F%2Fwww.najada.cz%2F&Search=Authority+of+the+Consuls&Sender=Submit&MagicCardSet=-1#
https://www.najada.cz/cz/kusovky-mtg/?Anchor=EShopSearchArticles&RedirUrl=https%3A%2F%2Fwww.najada.cz%2F&Search=Baird%2C+Steward+of+Argive&Sender=Submit&MagicCardSet=-1#
https://www.najada.cz/cz/kusovky-mtg/?Anchor=EShopSearchArticles&RedirUrl=https%3A%2F%2Fwww.najada.cz%2F&Search=Beastmaster's+Magemark&Sender=Submit&MagicCardSet=-1#
https://www.najada.cz/cz/kusovky-mtg/?Anchor=EShopSearchArticles&RedirUrl=https%3A%2F%2Fwww.najada.cz%2F&Search=Benevolent+Unicorn&Sender=Submit&MagicCardSet=-1#
https://www.najada.cz/cz/kusovky-mtg/?Anchor=EShopSearchArticles&RedirUrl=https%3A%2F%2Fwww.najada.cz%2F&Search=Blazing+Archon&Sender=Submit&MagicCardSet=-1#
https://www.najada.cz/cz/kusovky-mtg/?Anchor=EShopSearchArticles&RedirUrl=https%3A%2F%2Fwww.najada.cz%2F&Search=Capashen+Unicorn&Sender=Submit&MagicCardSet=-1#
https://www.najada.cz/cz/kusovky-mtg/?Anchor=EShopSearchArticles&RedirUrl=https%3A%2F%2Fwww.najada.cz%2F&Search=Cartouche+of+Knowledge&Sender=Submit&MagicCardSet=-1#
https://www.najada.cz/cz/kusovky-mtg/?Anchor=EShopSearchArticles&RedirUrl=https%3A%2F%2Fwww.najada.cz%2F&Search=Cartouche+of+Strength&Sender=Submit&MagicCardSet=-1#
https://www.najada.cz/cz/kusovky-mtg/?Anchor=EShopSearchArticles&RedirUrl=https%3A%2F%2Fwww.najada.cz%2F&Search=Chamber+of+Manipulation&Sender=Submit&MagicCardSet=-1#
https://www.najada.cz/cz/kusovky-mtg/?Anchor=EShopSearchArticles&RedirUrl=https%3A%2F%2Fwww.najada.cz%2F&Search=Circle+of+Protection%3A+Artifacts&Sender=Submit&MagicCardSet=-1#
https://www.najada.cz/cz/kusovky-mtg/?Anchor=EShopSearchArticles&RedirUrl=https%3A%2F%2Fwww.najada.cz%2F&Search=Circle+of+Protection%3A+Black&Sender=Submit&MagicCardSet=-1#
```

## Proc skript pouzit?

Chcete-li si koupit napriklad karty z commander decku, ktery si stahnete z netu, tak zadavat jednotlive karty je dost otrocina.

Tomuto skriptu predate stazeny seznam karet. Skript akceptuje nasledujici format radku souboru.
```
<pocet> <nazev_karty>
1 Cartouche of Knowledge
3 Swamp

<pocet> <nazev_karty> (edice) [nejake_cislo]
1 Sandstone Oracle (CMR) 336
1 Scourglass (ALA)
```
a ten vygeneruje seznam url, na ktere pak staci v terminalu jen klikat jeden po druhem pomoci 'ctrl+L click'.

Tento vystupni list lze take presmerovat do souboru a pouzit ho pozdeji.


## Kde ziskat list karet v tomto formatu?
List karet ve zminenem formatu lze napriklad exportovanim na **mtggoldfish** nebo na **tappedout**. Takovy seznam pak bude perfektne pouzitelny pro tento nastroj.

Note: Dalsi stranky/formaty nez vyse zminene nebyly odzkouseny. Obecne ale pokud seznam splnuje format, url by to melo bez problemu vygenerovat.


## Priklady pouziti
```
deck-url-transformator.sh [-h|--help] [-d|--deck-id DECK_ID] [-w|--web cernyrytir|najada] [-f|--deck-file FILE] [-o|--open]"

# Vypise help a ukonci skript
./deck-url-transformator.sh -h

# **Zakladni pouziti - vygeneruje seznam url dle karet ze souboru pro obchod cernyrytir**
./deck-url-transformator.sh -f my_commander_deck.txt

# Stahne a vygeneruje url pro deck podle ID z https://www.mtggoldfish.com/deck/download/3909719
./deck-url-transformator.sh -d 3909719

# Vygeneruje URL karet ze souboru my_commander_deck.txt pro server najada **[pro najadu to jeste nema vychytane mouchy]**
./deck-url-transformator.sh -w najada -f my_commander_deck.txt

# Vygeneruje URL karet ze souboru a rovnou se url pokusi otevrit v prohlizeci firefox [zatim jen experimentalni]
./deck-url-transformator.sh -w cernyrytir -f my_commander_deck.txt -o
```

## Planovana rozsireni
- pro zadane obchody porovnat ceny jednotlivych karet v zadanem seznamu

