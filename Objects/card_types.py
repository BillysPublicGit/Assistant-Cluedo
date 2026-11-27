CARD_TYPE_CHARACTER = 0
CARD_TYPE_WEAPON = 1
CARD_TYPE_ROOM = 2


class CardType:
    def __init__(self, name, card_type_id, num):
        self.name = name
        self.card_type_id = card_type_id
        self.num = num
card_types = []


# Initialises card_types array data
def load_card_types():

    card_types.append(CardType("Character", CARD_TYPE_CHARACTER, 6))
    card_types.append(CardType("Weapon", CARD_TYPE_WEAPON, 6))
    card_types.append(CardType("Room", CARD_TYPE_ROOM, 9))

# Validates an input to determine if it is within the boundaries of the card_types array
def is_valid_card_type_id(input):
    return 0 <= input < len(card_types)