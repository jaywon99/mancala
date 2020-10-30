

class TranspositionTable:
    def __init__(self):
        self.table = {}

    def get(self, state):
        if state in self.table:
            return self.table[state]
        else:
            return None

    def put(self, state, score, actions, depth):
        self.table[state] = {'score': score, 'actions': actions, 'depth': depth}
