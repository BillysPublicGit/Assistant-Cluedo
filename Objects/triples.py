class Triple:
    def __init__(self, linked_suspicion_id):
        self.triple_id = len(triples)
        self.linked_suspicion_id = linked_suspicion_id
        self.resolved = 0
triples = []


# Validates an input to determine if it is within the boundaries of the triples array
def is_valid_triple_id(input):
    return 0 <= input < len(triples)