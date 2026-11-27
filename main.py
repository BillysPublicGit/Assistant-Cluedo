from Objects.players import *
from Objects.card_types import *
from Objects.cards import *
from Objects.suspicions import *
from Objects.triples import *


COLOUR_RESET = "\033[0m"
COLOUR_RED = "\033[91m"
COLOUR_GREEN = "\033[92m"
COLOUR_YELLOW = "\033[93m"
COLOUR_BLUE = "\033[94m"
COLOUR_PURPLE = "\033[95m"
COLOUR_CYAN = "\033[96m"
COLOUR_WHITE = "\033[97m"

RETURN_TO_MENU = 99
RETURN_TEXT = str(RETURN_TO_MENU) + " - Return to main menu"


# Prints a string without the newline similar to C
def printf(text: str) -> None:
    print(text, end="")

# Prints a string with corresponding new lines
def print_lines(text: str, count: int = 3) -> None:
    print(text, end="\n" * count)

# Reads and validates an integer input
def read_int(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print_lines("Invalid input. Please enter a valid integer.")

# Reads and validates a Yes/No input
def read_yn(prompt: str) -> bool:
    while True:
        choice = input(f"{prompt}\n1 - Yes\n2 - No\n").strip().lower()
        if choice in ("1", "y", "yes"):
            return True
        if choice in ("2", "n", "no"):
            return False
        print_lines("Please enter 1/2 or Y/N.")

# Reads and validates a string input
def read_str(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print_lines("Invalid input. Please enter a valid string.")

# Prints the value of a single grid square
def print_grid_value(grid_value):
    grid_colour = COLOUR_RESET
    grid_char = ' '
    if (grid_value == 0):
        grid_colour = COLOUR_RED
        grid_char = 'N'
    elif (grid_value == 1):
        grid_colour = COLOUR_GREEN
        grid_char = 'Y'
    printf(grid_colour + grid_char + COLOUR_RESET)

# Prints row of |=== ... ===|
def print_border_row(num_players):
    printf("|")
    for i in range(0,MAX_CARD_NAME_LENG + 6 + 4*num_players):
        printf("=")
    print("|")

# Prints the grid
def print_grid(num_players, grid):
    print_border_row(num_players)
    printf("|            Card")
    for i in range(0, num_players):
        printf(" | " + players[i].name[0])
    print(" | C |")
    print_border_row(num_players)
    for i in range(0,len(cards)):
        printf("| ")
        for j in range(0,MAX_CARD_NAME_LENG-len(cards[i].name)):
            printf(" ")
        printf(cards[i].name)
        for j in range(0,num_players+1):
            printf(" | " )
            print_grid_value(grid[j][i])
        print(" |")
        print_border_row(num_players)
    printf("|       Num Cards")
    for i in range(0,num_players):
        printf(" | " + str(players[i].num_cards))
    print(" | " + str(3) + " |")
    print_border_row(num_players)

def describe_fulfilment(suspicion_fulfilee_id, shown_card_id):
    if suspicion_fulfilee_id < 0:
        return "Suspicion unfulfilled"
    text = "Fulfilled by " + players[suspicion_fulfilee_id].name
    if shown_card_id >= 0:
        text += " (" + cards[shown_card_id].name + ")"
    return text

# Prints all suspicions
def print_suspicions():
    for suspicion in suspicions:
        fulfil_text = describe_fulfilment(suspicion.fulfilee_player_id, suspicion.shown_card_id)
        print(str(suspicion.suspicion_id) + " - " + players[suspicion.suspicious_player_id].name + ": " + cards[suspicion.character_card_id].name + ", " + cards[suspicion.weapon_card_id].name + " & " + cards[suspicion.room_card_id].name + " - " + fulfil_text)

# Prints all triples
def print_triples():
    for triple in triples:
        suspicion = suspicions[triple.linked_suspicion_id]
        fulfil_text = describe_fulfilment(suspicion.fulfilee_player_id, suspicion.shown_card_id)
        if triple.resolved:
            printf(COLOUR_GREEN + "Resolved:   " + COLOUR_RESET)
        else:
            printf(COLOUR_RED + "Unresolved: " + COLOUR_RESET)
        print(str(suspicion.suspicion_id) + " - " + players[suspicion.suspicious_player_id].name + ": " + cards[suspicion.character_card_id].name + ", " + cards[suspicion.weapon_card_id].name + " & " + cards[suspicion.room_card_id].name + " - " + fulfil_text)

# Checks triples to see if they can populate the grid
def check_triples(num_players, grid):
    for triple in triples:
        if (triple.resolved == 0):

            suspicion = suspicions[triple.linked_suspicion_id]
            fulfilee_player_id = suspicion.fulfilee_player_id

            # The three cards involved in the suspicion
            card_ids = [
                suspicion.character_card_id,
                suspicion.weapon_card_id,
                suspicion.room_card_id
            ]

            possible_card_ids = [card_id for card_id in card_ids if grid[fulfilee_player_id][card_id] != 0]

            if not possible_card_ids:
                print(COLOUR_RED + f"Conflict: suspicion {suspicion.suspicion_id} cannot have been fulfilled" + COLOUR_RESET)
            elif any(grid[fulfilee_player_id][card_id] == 1 for card_id in card_ids):
                triple.resolved = 1
            elif len(possible_card_ids) == 1:

                # Mark resolved before changing the grid.
                # set_grid_value() calls check_triples().
                triple.resolved = 1
                set_grid_value(fulfilee_player_id, possible_card_ids[0], 1, num_players, grid)

# Sets the value of a square on the grid and calculates other squares based on updated info
def set_grid_value(x_index,y_index, value, num_players, grid):

    current_value = grid[x_index][y_index]

    if current_value != 2:
        if current_value != value:
            print(COLOUR_RED + f"Conflict: {players[x_index].name} - {cards[y_index].name}, {current_value} -> {value}" + COLOUR_RESET)
        return

    if ((current_value == 2) and (value in {0,1})):
        grid[x_index][y_index] = value
        if value == 1:
            if x_index < num_players:
                for i in range(num_players):
                    if i != x_index:
                        set_grid_value(i, y_index, 0, num_players, grid)
                set_grid_value(num_players, y_index, 0, num_players, grid)
            else:
                for i in range(num_players):
                    set_grid_value(i, y_index, 0, num_players, grid)
                for j, card in enumerate(cards):
                    if (j != y_index and card.card_type_id == cards[y_index].card_type_id):
                        set_grid_value(num_players, j, 0, num_players, grid)
        if (value == 0):
            candidates = [i for i in range(num_players + 1) if grid[i][y_index] != 0]
            if len(candidates) == 1:
                set_grid_value(candidates[0], y_index, 1, num_players, grid)
            if x_index == num_players:
                card_type_id = cards[y_index].card_type_id
                same_type_ids = [c.card_id for c in cards if c.card_type_id == card_type_id]
                already_found = any(grid[num_players][cid] == 1 for cid in same_type_ids)
                unknown_ids = [cid for cid in same_type_ids if grid[num_players][cid] == 2]
                if not already_found and len(unknown_ids) == 1:
                    set_grid_value(num_players, unknown_ids[0], 1, num_players, grid)
        num_zeros_in_column = 0
        num_ones_in_column = 0
        for i in range(0, len(cards)):
            if (grid[x_index][i] == 0):
                num_zeros_in_column += 1
            if (grid[x_index][i] == 1):
                num_ones_in_column += 1
        num_cards = 3
        if (x_index < num_players):
            num_cards = players[x_index].num_cards
        if num_zeros_in_column == len(cards) - num_cards:
            for i in range(len(cards)):
                if grid[x_index][i] == 2:
                    set_grid_value(x_index, i, 1, num_players, grid)
        if num_ones_in_column == num_cards:
            for i in range(len(cards)):
                if grid[x_index][i] == 2:
                    set_grid_value(x_index, i, 0, num_players, grid)
        check_triples(num_players, grid)

# Returns one complete deal that fits every rule, or None if there isn't one
#   owners - for each card, the set of owner IDs that could hold it
#   groups - (owner, card_ids, count): the owner holds exactly count of those cards
#   clues  - (player, card_ids): the player holds at least one of those cards
def find_deal(owners, groups, clues):
    owners = [set(possible) for possible in owners]

    # Apply the rules repeatedly until nothing else changes
    changed = True
    while changed:
        changed = False
        for owner, card_ids, count in groups:
            possible = [c for c in card_ids if owner in owners[c]]
            held = [c for c in possible if len(owners[c]) == 1]
            if len(held) > count or len(possible) < count:
                return None
            for c in possible:
                if len(owners[c]) > 1:
                    if len(held) == count:
                        owners[c].discard(owner)
                        changed = True
                    elif len(possible) == count:
                        owners[c] = {owner}
                        changed = True
        for player_id, card_ids in clues:
            possible = [c for c in card_ids if player_id in owners[c]]
            if not possible:
                return None
            if len(possible) == 1 and len(owners[possible[0]]) > 1:
                owners[possible[0]] = {player_id}
                changed = True

    undecided = [c for c in range(len(owners)) if len(owners[c]) > 1]
    if not undecided:
        return [next(iter(possible)) for possible in owners]

    # Guess an owner for the most restricted card, then try to complete the deal
    card_id = min(undecided, key=lambda c: len(owners[c]))
    for owner in owners[card_id]:
        trial = owners.copy()
        trial[card_id] = {owner}
        deal = find_deal(trial, groups, clues)
        if deal:
            return deal
    return None

# For each card, returns every owner that appears in at least one valid deal
def find_possible_owners(owners, groups, clues):
    seen = [set() for _ in owners]
    for card_id, candidates in enumerate(owners):
        for owner in candidates:
            if owner in seen[card_id]:
                continue
            trial = list(owners)
            trial[card_id] = {owner}
            deal = find_deal(trial, groups, clues)
            if deal:
                for c, deal_owner in enumerate(deal):
                    seen[c].add(deal_owner)
    return seen

# Fills in every grid square that is logically certain
def solve_grid(num_players, grid):
    envelope_id = num_players
    all_card_ids = range(len(cards))
    owners = [{o for o in range(num_players + 1) if grid[o][c] != 0} for c in all_card_ids]

    # Each player holds their number of cards, the envelope holds one of each type
    groups = [(p, all_card_ids, players[p].num_cards) for p in range(num_players)]
    for card_type in card_types:
        type_card_ids = [card.card_id for card in cards if card.card_type_id == card_type.card_type_id]
        groups.append((envelope_id, type_card_ids, 1))

    # Each fulfiller holds at least one of the three suspected cards
    clues = [(s.fulfilee_player_id, [s.character_card_id, s.weapon_card_id, s.room_card_id])
             for s in suspicions if s.fulfilee_player_id >= 0]

    seen = find_possible_owners(owners, groups, clues)
    if not all(seen):
        print(COLOUR_RED + "Conflict: the recorded information is impossible" + COLOUR_RESET)
        return

    for c in all_card_ids:
        for o in range(num_players + 1):
            if o not in seen[c]:
                grid[o][c] = 0
            elif len(seen[c]) == 1:
                grid[o][c] = 1

    # Update the triple statuses to match the new grid
    check_triples(num_players, grid)

# Players who were asked and could not show a card, in clockwise order
def players_who_passed(num_players, suspector_id, fulfilee_id):
    passed = []
    player_id = (suspector_id + 1) % num_players
    while player_id not in (suspector_id, fulfilee_id):
        passed.append(player_id)
        player_id = (player_id + 1) % num_players
    return passed

# Returns a description of why a result is impossible, or None
def find_problem(num_players, grid, suspector_id, card_ids, fulfilee_id):
    for player_id in players_who_passed(num_players, suspector_id, fulfilee_id):
        for card_id in card_ids:
            if grid[player_id][card_id] == 1:
                return f"{players[player_id].name} holds {cards[card_id].name}, so could not have passed."
    if fulfilee_id >= 0 and all(grid[fulfilee_id][c] == 0 for c in card_ids):
        return f"{players[fulfilee_id].name} holds none of those cards."
    return None

# Reads inputs for a suspicion and populates the grid as appropriately as possible based on the result
def make_suspicion(num_players, grid):

    # Input player making suspicion
    suspicious_player_id = -1
    while True:
        print("Which Player is suspicious?")
        for i in range(0, num_players):
            print(str(i) + " - " + players[i].name)
        print(RETURN_TEXT)
        suspicious_player_id = read_int("")
        if suspicious_player_id == RETURN_TO_MENU:
            return
        if ((is_valid_player_id(suspicious_player_id)) and (suspicious_player_id < num_players)):
            break

    # Input suspicious cards
    suspicious_card_ids = [-1] * 3
    for card_type in card_types:
        while True:
            print("Which " + card_type.name + " is " + players[suspicious_player_id].name + " suspicious of?")
            for card in cards:
                if (card.card_type_id == card_type.card_type_id):
                    print(str(card.card_id) + " - " + card.name)
            print(RETURN_TEXT)
            suspicious_card_ids[card_type.card_type_id] = read_int("")
            if suspicious_card_ids[card_type.card_type_id] == RETURN_TO_MENU:
                return
            if (is_valid_card_id(suspicious_card_ids[card_type.card_type_id])):
                if (cards[suspicious_card_ids[card_type.card_type_id]].card_type_id == card_type.card_type_id):
                    break

    # Input fulfillment info
    fulfilee_player_id = -1
    shown_card_id = -1
    while True:
        print("Which Player, if any, fulfilled the suspicion?")
        for i in range(0, num_players):
            print(str(i) + " - " + players[i].name)
        fulfilee_player_id = read_int(str(num_players) + " - Unfulfilled\n" + RETURN_TEXT + "\n")
        if fulfilee_player_id == RETURN_TO_MENU:
            return
        is_unfulfilled = (fulfilee_player_id == num_players)
        is_other_player = (
            is_valid_player_id(fulfilee_player_id)
            and fulfilee_player_id < num_players
            and fulfilee_player_id != suspicious_player_id
        )
        if is_unfulfilled or is_other_player:
            if is_unfulfilled:
                fulfilee_player_id = -1
            problem = find_problem(num_players, grid, suspicious_player_id, suspicious_card_ids, fulfilee_player_id)
            if problem:
                print(COLOUR_RED + problem + " Please choose again." + COLOUR_RESET)
                continue
            if (not is_unfulfilled) and (suspicious_player_id == PLAYER_0):
                possible_card_ids = [card_id for card_id in suspicious_card_ids if grid[fulfilee_player_id][card_id] != 0]
                while True:
                    print("Which card were you shown?")
                    for card_id in possible_card_ids:
                        print(str(card_id) + " - " + cards[card_id].name)
                    print(RETURN_TEXT)
                    shown_card_id = read_int("")
                    if shown_card_id == RETURN_TO_MENU:
                        return
                    if shown_card_id in possible_card_ids:
                        break
                    print("Invalid card. Please choose one of the listed cards.")
            elif (fulfilee_player_id == PLAYER_0):
                held_card_ids = [card_id for card_id in suspicious_card_ids if grid[PLAYER_0][card_id] == 1]
                while True:
                    print("Which card did you show?")
                    for card_id in held_card_ids:
                        print(str(card_id) + " - " + cards[card_id].name)
                    print(RETURN_TEXT)
                    shown_card_id = read_int("")
                    if shown_card_id == RETURN_TO_MENU:
                        return
                    if shown_card_id in held_card_ids:
                        break
                    print("Invalid card. You must show one of the suspected cards that you hold.")
            break

    # Implement suspicion
    print("\nSuspicion:")
    fulfil_text = describe_fulfilment(fulfilee_player_id, shown_card_id)
    print(players[suspicious_player_id].name + ": " + cards[suspicious_card_ids[CARD_TYPE_CHARACTER]].name + ", " + cards[suspicious_card_ids[CARD_TYPE_WEAPON]].name + " & " + cards[suspicious_card_ids[CARD_TYPE_ROOM]].name + " - " + fulfil_text)
    if read_yn("Is this correct?"):
        suspicions.append(Suspicion(suspicious_player_id, suspicious_card_ids[0],suspicious_card_ids[1],suspicious_card_ids[2], fulfilee_player_id, shown_card_id))
        suspicion = suspicions[len(suspicions) - 1]
        if (suspicion.shown_card_id >= 0):
            set_grid_value(suspicion.fulfilee_player_id,suspicion.shown_card_id, 1, num_players, grid)
        for i in players_who_passed(num_players, suspicious_player_id, fulfilee_player_id):
            for card_id in suspicious_card_ids:
                set_grid_value(i, card_id, 0, num_players, grid)
        if fulfilee_player_id >= 0:
            if (suspicion.suspicious_player_id != PLAYER_0) and (suspicion.fulfilee_player_id != PLAYER_0) and (suspicion.shown_card_id == -1):
                triples.append(Triple(suspicion.suspicion_id))
                check_triples(num_players, grid)
        solve_grid(num_players, grid)

# Records a card accidentally revealed by an opposing player
def add_card_reveal(num_players, grid):

    # Input player ID (excluding yourself)
    while True:
        print("Which player revealed a card?")
        for i in range(1, num_players):
            print(str(i) + " - " + players[i].name)
        player_id = read_int("")
        if is_valid_player_id(player_id) and 1 <= player_id < num_players:
            break
        print_lines("Invalid input. Must be a valid player_id > 0.")

    # Input card ID
    while True:
        print("Which card was revealed?")
        for card in cards:
            print(str(card.card_id) + " - " + card.name)
        card_id = read_int("")
        if is_valid_card_id(card_id):
            break
        print_lines("Invalid input. Must be a card_id.")

    # Record that the player holds the revealed card
    set_grid_value(player_id, card_id, 1, num_players, grid)
    solve_grid(num_players, grid)


# Program starts here
def main():
    print_lines("Welcome to Cluedo Assistant")

    load_players()
    load_card_types()
    load_cards()

    # Input num players
    num_players = 0
    while True:
        num_players = read_int("How many players?\n")
        if ((is_valid_player_id(num_players-1)) and (num_players > 1)):
            break
        else:
            print_lines("Invalid input. num_players must be between 2 and " + str(len(players)))

    # Input player's names
    print("Starting with you, then continuing around the table clockwise, enter each player's name.")
    players[0].name = read_str("Your name:\n")
    for i in range(1, num_players):
        players[i].name = read_str("Player " + str(i) +" name:\n")

    # Input each player's num cards
    while True:
        num_card_count = 0
        min_player_cards = (len(cards)-3)//num_players
        max_player_cards = min_player_cards
        if (len(cards)-3) % num_players != 0:
            max_player_cards += 1
        allowed_text = str(min_player_cards)
        if max_player_cards != min_player_cards:
            allowed_text = "between " + str(min_player_cards) + " and " + str(max_player_cards)
        for i in range(0, num_players):
            while True:
                num_cards = read_int(players[i].name +"'s Num Cards:\n")
                if min_player_cards <= num_cards <= max_player_cards:
                    players[i].num_cards = num_cards
                    num_card_count += players[i].num_cards
                    break
                print_lines("Invalid input. " + players[i].name + "'s number of cards must be " + allowed_text + ".")
        if (num_card_count == len(cards)-3):
            break
        else:
            print("Invalid Inputs. Player's cards must total " + str(len(cards)-3) + ", not " + str(num_card_count))

    # Input player's starting cards
    grid = [[2] * len(cards) for _ in range(num_players + 1)]
    while True:
        grid = [[2] * len(cards) for _ in range(num_players + 1)]
        for i in range(0, players[PLAYER_0].num_cards):
            while True:
                print("Card " + str(i+1) + "/" + str(players[PLAYER_0].num_cards) + "?")
                for card in cards:
                    print(str(card.card_id) + " - " + card.name)
                grid_index = read_int("")
                if is_valid_card_id(grid_index) and grid[PLAYER_0][grid_index] == 2:
                    set_grid_value(PLAYER_0,grid_index, 1, num_players, grid)
                    break
                print_lines("Invalid input.")
        print("\nYour hand:")
        for card in cards:
            if grid[PLAYER_0][card.card_id] == 1:
                print("- " + card.name)
        if read_yn("Is this correct?"):
            break

    while True:
        print("\nWhat would you like to do?")
        print("1 - Print Grid")
        print("2 - Print Suspicions")
        print("3 - Print Triples")
        print("4 - Make Suspicion")
        print("5 - Add Card Reveal")
        menu_input = read_int("")
        if (menu_input == 1):
            print_grid(num_players, grid)
        elif (menu_input == 2):
            print_suspicions()
        elif (menu_input == 3):
            print_triples()
        elif (menu_input == 4):
            make_suspicion(num_players, grid)
        elif (menu_input == 5):
            add_card_reveal(num_players, grid)
        else:
            print("Invalid Input. menu_input must be between 1 and 5")

if __name__ == "__main__":
    main()