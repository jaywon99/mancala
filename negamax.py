import sys
import random
import math

from mancala import Mancala
from transposition import TranspositionTable

# AI Game
# #1 Negamax
# #2 Alpha Beta Pruning
# #3 Null Window
# #4 Iterative Deepening
# #5 Transposition Table
# #6 Alpha Beta Pruning Transposition Table

tp = TranspositionTable()

def negamax(env, player, depth=10, again=0):
    negamax.counter += 1

    board_hash = player.board_hash()
    cache = tp.get(board_hash)

    if cache:
        if cache['depth'] >= depth: # cache가 더 깊이까지 가 봄
            print("CACHE HIT!")
            return cache['score'], cache['actions']

    tp.put_score(board_hash, player.winning_score())

    actions = player.available_actions()
    best_score = -math.inf
    best_actions = []

    for action in actions:
        # print("~~~~ PLAYER", player.player_id(), "ACTION:", action)
        memento = env.create_memento()
        (_, reward, done, play_again) = player.step(action)
        # print('??', "".join([a[1] for a in env.board.log]), reward, done)
        if done:
            score = reward
            # 여기에서는 뭘 저장하지?
        else:
            next_player = env.next_player(play_again)
            tp.put_next(board_hash, next_player.board_hash(), play_again)
            if play_again:
                score, _ = negamax(env, next_player, depth, again+1)
            elif depth == 1:
                score = reward
                next_results = None
            else:
                score, _ = negamax(env, next_player, depth-1, 0)
                score = -score # negamax
        env.restore_memento(memento)

        # print('~', "".join([a[1] for a in env.board.log]), score, action)
        # env.print()
        if score > best_score:
            best_score = score
            best_actions = [action]
        elif score == best_score:
            best_actions.append(action)

    # print('!', "".join([a[1] for a in env.board.log]), best_score, best_action)
    tp.put(board_hash, best_score, best_actions, depth)
    return (best_score, best_actions)

env = Mancala()
state = env.reset()
done = False
play_again = False
reward = 0
negamax.counter = 0
cnt = 0
while not done:
    player = env.next_player(play_again)    
    score, actions = negamax(env, player, depth=4)
    action = random.choice(actions)
    # action = random.choice(player.available_actions())
    state, reward, done, play_again = player.step(action)
    cnt += 1
    print("Round: ", cnt, "Player: ", player.player_id(), "ACTIONS:", actions, "ACTION: ", action, "Score:", score)
    print("TP SIZE", len(tp.table))
    print(reward, done, play_again)
    env.print()

if reward > 0:
    winner = player.player_id()
else:
    winner = player.opposite_player.player_id()
    reward = -reward
print(winner, len(env.board.log), reward, "".join([a[1] for a in env.board.log]))
print("TP SIZE", len(tp.table))
# print('LOG', "".join([a[1] for a in env.board.log]))