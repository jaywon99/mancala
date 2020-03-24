import random

from mancala import Mancala

m = Mancala()
obs = m.reset()
done = False
play_again = False

cnt = 0
while not done:
    player = m.next_player(play_again)    
    action = random.choice(player.available_actions())
    state, reward, done, play_again = player.step(action)
    cnt += 1
    print("Round: ", cnt, "Player: ", player.player_id(), "ACTION: ", action)
    print(reward, done, play_again)
    m.print()

