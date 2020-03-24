import random

from mancala import Mancala

def play(env, done, play_again):
    if done:
        return

    player = env.next_player(play_again)
    for action in player.available_actions():
        memento = env.create_memento()
        state, reward, done, play_again = player.step(action)
        if done:
            if reward > 0:
                winner = player.player_id()
            else:
                winner = player.opposite_player.player_id()
                reward = -reward
            print(winner, len(env.board.log), reward, "".join([a[1] for a in env.board.log]))
        else:
            play(env, done, play_again)
        env.restore_memento(memento)

env = Mancala()
obs = env.reset()
done = False
play_again = False

play(env, done, play_again)