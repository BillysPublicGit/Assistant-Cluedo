from Objects.players import *
from Objects.card_types import *


CARD_REVEREND_GREEN = 0
CARD_COLONEL_MUSTARD = 1
CARD_MRS_PEACOCK = 2
CARD_PROFESSOR_PLUM = 3
CARD_MISS_SCARLETT = 4
CARD_MRS_WHITE = 5
CARD_CANDLESTICK = 6
CARD_DAGGER = 7
CARD_LEAD_PIPE = 8
CARD_REVOLVER = 9
CARD_ROPE = 10
CARD_SPANNER = 11
CARD_BALLROOM = 12
CARD_BILLIARD_ROOM = 13
CARD_CONSERVATORY = 14
CARD_DINING_ROOM = 15
CARD_HALL = 16
CARD_KITCHEN = 17
CARD_LIBRARY = 18
CARD_LOUNGE = 19
CARD_STUDY = 20

MAX_CARD_NAME_LENG = 15


class Card:
    def __init__(self, name, card_id, card_type_id):
        self.name = name
        self.card_id = card_id
        self.card_type_id = card_type_id
cards = []


# Initialises cards array data
def load_cards():

    cards.append(Card("Reverend Green", CARD_REVEREND_GREEN, CARD_TYPE_CHARACTER))
    cards.append(Card("Colonel Mustard", CARD_COLONEL_MUSTARD, CARD_TYPE_CHARACTER))
    cards.append(Card("Mrs Peacock", CARD_MRS_PEACOCK, CARD_TYPE_CHARACTER))
    cards.append(Card("Professor Plum", CARD_PROFESSOR_PLUM, CARD_TYPE_CHARACTER))
    cards.append(Card("Miss Scarlett", CARD_MISS_SCARLETT, CARD_TYPE_CHARACTER))
    cards.append(Card("Mrs White", CARD_MRS_WHITE, CARD_TYPE_CHARACTER))
    cards.append(Card("Candlestick", CARD_CANDLESTICK, CARD_TYPE_WEAPON))
    cards.append(Card("Dagger", CARD_DAGGER, CARD_TYPE_WEAPON))
    cards.append(Card("Lead Pipe", CARD_LEAD_PIPE, CARD_TYPE_WEAPON))
    cards.append(Card("Revolver", CARD_REVOLVER, CARD_TYPE_WEAPON))
    cards.append(Card("Rope", CARD_ROPE, CARD_TYPE_WEAPON))
    cards.append(Card("Spanner", CARD_SPANNER, CARD_TYPE_WEAPON))
    cards.append(Card("Ballroom", CARD_BALLROOM, CARD_TYPE_ROOM))
    cards.append(Card("Billiard Room", CARD_BILLIARD_ROOM, CARD_TYPE_ROOM))
    cards.append(Card("Conservatory", CARD_CONSERVATORY, CARD_TYPE_ROOM))
    cards.append(Card("Dining Room", CARD_DINING_ROOM, CARD_TYPE_ROOM))
    cards.append(Card("Hall", CARD_HALL, CARD_TYPE_ROOM))
    cards.append(Card("Kitchen", CARD_KITCHEN, CARD_TYPE_ROOM))
    cards.append(Card("Library", CARD_LIBRARY, CARD_TYPE_ROOM))
    cards.append(Card("Lounge", CARD_LOUNGE, CARD_TYPE_ROOM))
    cards.append(Card("Study", CARD_STUDY, CARD_TYPE_ROOM))

# Validates an input to determine if it is within the boundaries of the cards array
def is_valid_card_id(input):
    return 0 <= input < len(cards)