# -*- coding: utf-8 -*- 

'''Mancala Board
https://www.thesprucecrafts.com/how-to-play-mancala-409424
'''

import pickle

class DistributeIterator:
    def __init__(self, order, start, nth):
        self.order = order
        self.start = start
        self.nth = nth
        self.pos = 0

    def _go_next(self):
        self.pos += 1
        if self.pos >= len(self.order):
            self.pos = self.pos % len(self.order)

    def __iter__(self):
        self.pos = self.order.index(self.start)
        return self

    def __next__(self):
        self.nth -= 1
        if self.nth < 0:
            raise StopIteration
        self._go_next()
        return self.order[self.pos]

class MancalaPlayer:
    def __init__(self, board, home, pits, pits_order):
        self.board = board                  # final
        self.home = home                    # final
        self.pits = pits                    # final
        self.pits_order = pits_order        # final
        self.opposite_player = None         # almost final (just 1 set)

    def reset(self):
        pass

    def set_opposite_player(self, opposite_player):
        self.opposite_player = opposite_player

    def available_actions(self):
        actions = []
        for pos in self.pits:
            if self.board[pos] != 0:
                actions.append(pos)
        return actions

    def get_stones_in_pits(self):
        return [self.board[pos] for pos in self.pits]

    def step(self, action):
        self.board.add_play_log(self.home, action)

        if action not in self.pits:
            # ERROR! FOUL! You can pick from your pits only.
            return None, -100, True, True
        if self.board[action] == 0:
            # ERROR! FOUL! You should pick pit which stone exist.
            return None, -100, True, True
        
        # pick up stones
        # Rule #04: The game begins with one player picking up all of the pieces in any one of the holes on their side.
        stones = self.board[action]

        # Rule #05: Moving counter-clockwise, the player deposits one of the stones in each hole until the stones run out.
        last_pos = None
        for pos in DistributeIterator(self.pits_order, action, stones):
            self.board.move(action, pos, 1)
            last_pos = pos

        # Rule #07: If the last piece you drop is in your own store, you get a free turn.
        play_again = False
        if last_pos == self.home:
            # DO ONE MORE
            play_again = True

        # landing my empty spot, take oppsite position stones, too
        # Rule #08: If the last piece you drop is in an empty hole on your side, you capture that piece and any pieces in the hole directly opposite.
        if last_pos in self.pits and self.board[last_pos] == 1:
            # another rule
            opposite_position = MancalaBoard.oppsite_position(last_pos)
            if self.board[opposite_position] != 0:
                self.board.move(opposite_position, self.home)
                self.board.move(last_pos, self.home)

        # check stones left on my pits?
        # Rule #10: The game ends when all six spaces on one side of the Mancala board are empty.
        done = False
        if len(self.available_actions()) == 0:
            # No more stones on my pits
            # Rule #11: The player who still has pieces on his side of the board when the game ends capture all of those pieces.
            self.opposite_player.swipe_out()
            done = True

        my_score = self.score()
        your_score = self.opposite_player.score()

        return self.board.observation(), my_score - your_score, done, play_again
        # return observation, my_score - your_score, done, play_again

    def score(self):
        ''' Rule #12: Count all the pieces in each store. The winner is the player with the most pieces.
        '''
        return self.board[self.home]

    def swipe_out(self):
        '''
        Rule #11: The player who still has pieces on his side of the board when the game ends capture all of those pieces.
        '''
        for pos in self.available_actions():
            self.board.move(pos, self.home)

    def player_id(self):
        return self.home

    def board_hash(self):
        ALPHADIGIT='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789' # 62자리
        stone_cnts = [self.board[pos] for pos in self.pits]
        stone_cnts.extend(self.board[pos] for pos in self.opposite_player.pits)
        return ''.join(ALPHADIGIT[n] for n in stone_cnts) # 각 자리의 최대 숫자는 48 (4*12), base64 비슷하게 처리 (' ', '/'는 불필요)

class MancalaBoard:
    CELL_LIST = ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'RH', 'BH']
    RED_HOME = 'RH'
    BLUE_HOME = 'BH'
    # RED_PITS = ['R6', 'R5', 'R4', 'R3', 'R2', 'R1']
    # BLUE_PITS = ['B6', 'B5', 'B4', 'B3', 'B2', 'B1']
    RED_PITS = ['R1', 'R2', 'R3', 'R4', 'R5', 'R6']
    BLUE_PITS = ['B1', 'B2', 'B3', 'B4', 'B5', 'B6']
    # Rule 06: If you run into your own store, deposit one piece in it. If you run into your opponent's store, skip it.
    RED_ORDER = ['R6', 'R5', 'R4', 'R3', 'R2', 'R1', 'RH', 'B6', 'B5', 'B4', 'B3', 'B2', 'B1']
    BLUE_ORDER = ['B6', 'B5', 'B4', 'B3', 'B2', 'B1', 'BH', 'R6', 'R5', 'R4', 'R3', 'R2', 'R1']
    OPPOSITE_POSITION = {
        'R6': 'B1',
        'R5': 'B2',
        'R4': 'B3',
        'R3': 'B4',
        'R2': 'B5',
        'R1': 'B6',
        'B6': 'R1',
        'B5': 'R2',
        'B4': 'R3',
        'B3': 'R4',
        'B2': 'R5',
        'B1': 'R6',
    }

    def __init__(self):
        self.board = {c:0 for c in MancalaBoard.CELL_LIST}
        self.log = []

    def reset(self):
        self.board = {c:4 for c in MancalaBoard.CELL_LIST}
        self.board['BH'] = 0
        self.board['RH'] = 0
        self.log = []

    def observation(self):
        # 이걸 어떻게 define할지
        # 가장 쉬운 건 [self.board[pos] for pos in CELL_LIST] 일텐데.. Compact 할 수는 없을까?
        return [self.board[pos] for pos in self.CELL_LIST]

    def add_play_log(self, who, action):
        self.log.append((who, action)) # we can get who from action anyway

    def move(self, pos_from, pos_to, cnt = None):
        '''
        to animate, make log here.
        if cnt == None: move everything
        '''
        # make log to animate
        # print(pos_from, pos_to, cnt)
        if cnt == None:
            cnt = self.board[pos_from]
        self.board[pos_from] -= cnt
        self.board[pos_to] += cnt

    @staticmethod
    def oppsite_position(pos):
        return MancalaBoard.OPPOSITE_POSITION[pos]

    def create_memento(self):
        return pickle.dumps((self.board, self.log))
    
    def restore_memento(self, memory):
        (self.board, self.log) = pickle.loads(memory)

    def __getitem__(self, key):
        return self.board[key]

    def __setitem__(self, key, value):
        self.board[key] = value

class Mancala:
    def __init__(self):
        self.board = MancalaBoard()
        self.player1 = MancalaPlayer(self.board, MancalaBoard.RED_HOME, MancalaBoard.RED_PITS, MancalaBoard.RED_ORDER)
        self.player2 = MancalaPlayer(self.board, MancalaBoard.BLUE_HOME, MancalaBoard.BLUE_PITS, MancalaBoard.BLUE_ORDER)
        self.reset()

    def reset(self):
        self.board.reset()
        self.player1.reset()
        self.player2.reset()
        self.player1.set_opposite_player(self.player2)
        self.player2.set_opposite_player(self.player1)
        self.current_player = self.player2
        return self.board.observation()

    def next_player(self, play_again):
        if play_again:
            return self.current_player

        if self.current_player == self.player1:
            self.current_player = self.player2
        else:
            self.current_player = self.player1
        return self.current_player
    
    def oppsite_player(self):
        if self.current_player == self.player1:
            return self.player2
        return self.player1

    def create_memento(self):
        return (self.board.create_memento(), self.current_player.player_id())

    def restore_memento(self, memory):
        self.board.restore_memento(memory[0])
        if memory[1] == self.player1.player_id():
            self.current_player = self.player1
        else:
            self.current_player = self.player2

    def print(self):
        print("+----+----+----+----+----+----+----+----+")
        print("|    | %2d | %2d | %2d | %2d | %2d | %2d |    |" % (self.board['R1'], self.board['R2'], self.board['R3'], self.board['R4'], self.board['R5'], self.board['R6']))
        print("+ %2d +----+----+----+----+----+----+ %2d +" % (self.board['RH'], self.board['BH']))
        print("|    | %2d | %2d | %2d | %2d | %2d | %2d |    |" % (self.board['B6'], self.board['B5'], self.board['B4'], self.board['B3'], self.board['B2'], self.board['B1']))
        print("+----+----+----+----+----+----+----+----+")
        print("-----------------------------------------------")
