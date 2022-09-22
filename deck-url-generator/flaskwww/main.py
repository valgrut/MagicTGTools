from mtgsdk import Card

# https://github.com/MagicTheGathering/mtg-sdk-python

# search by set and subtype
cards = Card.where(set='ktk').where(subtype='warrior,human').all()
for card in cards:
    print(card.name, " ", card.colors)

# partial name search
cards = Card.where(name='fox').where(subtype='fox').all()
for card in cards:
    print(card.name, " ", card.colors)
