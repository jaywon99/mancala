
class TranspositionTree:
    def __init__(self, state):
        self.state = state
        self.score = None
        self.play_again = False
        self._actions = {}
        self._future_score = {}

    def next(self, action, next_state, play_again):
        self._actions[action] = (next_state, play_again)

    def negamax_score(self, depth, score):
        self._future_score[depth] = score


class TranspositionTable:
    def __init__(self):
        self.table = {}

    def get(self, state):
        if state in self.table:
            return self.table[state]
        else:
            return None

    def _prepare_node(self, state):
        if state not in self.table:
            self.table[state] = TranspositionTree(state)
        return self.table[state]

    def put_next(self, state, action, next_state, play_again):
        node = self._prepare_node(state)
        next_node = self._prepare_node(next_state)
        node.next(action, next_state, play_again)

    def put_score(self, state, score):
        node = self._prepare_node(state)
        node.score = score

    def put_negamax_score(self, state, depth, score):
        node = self._prepare_node(state)
        node.depth_score(depth, score)

