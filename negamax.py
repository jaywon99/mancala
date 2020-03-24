import random
import math

from mancala import Mancala

# AI Game
# #1 Negamax
# #2 Alpha Beta Pruning
# #3 Null Window
# #4 Iterative Deepening
# #5 Transposition Table
# #6 Alpha Beta Pruning Transposition Table

def negamax(env, player, depth=10):
    negamax.counter += 1

    actions = player.available_actions()
    best_score = -math.inf
    best_action = None

    for action in actions:
        memento = env.create_memento()
        (_, reward, done, play_again) = player.step(action)
        # print('??', "".join([a[1] for a in env.board.log]), reward, done)
        if done:
            score = reward
        else:
            if play_again:
                score, _ = negamax(env, env.next_player(play_again), depth)
            elif depth == 1:
                score = reward
            else:
                score, _ = negamax(env, env.next_player(play_again), depth-1)
                score = -score # negamax
        env.restore_memento(memento)

        # print('~', "".join([a[1] for a in env.board.log]), score, action)
        # env.print()
        if score > best_score:
            best_score = score
            best_action = action

    # print('!', "".join([a[1] for a in env.board.log]), best_score, best_action)
    return (best_score, best_action)

env = Mancala()
state = env.reset()
done = False
play_again = False
reward = 0
negamax.counter = 0
cnt = 0
while not done:
    player = env.next_player(play_again)    
    score, action = negamax(env, player, depth=7)
    # action = random.choice(player.available_actions())
    state, reward, done, play_again = player.step(action)
    cnt += 1
    print("Round: ", cnt, "Player: ", player.player_id(), "ACTION: ", action, "Score:", score)
    print(reward, done, play_again)
    env.print()

if reward > 0:
    winner = player.player_id()
else:
    winner = player.opposite_player.player_id()
    reward = -reward
print(winner, len(env.board.log), reward, "".join([a[1] for a in env.board.log]))

# print('LOG', "".join([a[1] for a in env.board.log]))