class Suspicion:
    def __init__(self, suspicious_player_id, character_card_id,weapon_card_id,room_card_id, fulfilee_player_id, shown_card_id):
        self.suspicion_id = len(suspicions)
        self.suspicious_player_id = suspicious_player_id
        self.character_card_id = character_card_id
        self.weapon_card_id = weapon_card_id
        self.room_card_id = room_card_id
        self.fulfilee_player_id = fulfilee_player_id
        self.shown_card_id = shown_card_id
suspicions = []


# Validates an input to determine if it is within the boundaries of the suspicions array
def is_valid_suspicion_id(input):
    return 0 <= input < len(suspicions)