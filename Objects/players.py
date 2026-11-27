PLAYER_0 = 0
PLAYER_1 = 1
PLAYER_2 = 2
PLAYER_3 = 3
PLAYER_4 = 4
PLAYER_5 = 5


class Player:
    def __init__(self, player_id):
        self.name = "Inactive"
        self.player_id = player_id
        self.num_cards = 0
players = []


# Initialises players array data
def load_players():

    players.append(Player(PLAYER_0))
    players.append(Player(PLAYER_1))
    players.append(Player(PLAYER_2))
    players.append(Player(PLAYER_3))
    players.append(Player(PLAYER_4))
    players.append(Player(PLAYER_5))

# Validates an input to determine if it is within the boundaries of the players array
def is_valid_player_id(input):
    return 0 <= input < len(players)