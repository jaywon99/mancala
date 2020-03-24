import random
import sys

from mancala import Mancala

param = sys.argv[1]
seq = [param[c:c+2] for c in range(0, len(param), 2)]

m = Mancala()
obs = m.reset()
done = False
play_again = False

cnt = 0
for action in seq:
    player = m.next_player(play_again)    
    # action = random.choice(player.available_actions())
    print("Player: ", player.player_id(), "CANDIDATE:", ",".join(player.available_actions()))
    state, reward, done, play_again = player.step(action)
    cnt += 1
    print("Round: ", cnt, "Player: ", player.player_id(), "ACTION: ", action)
    print(reward, done, play_again)
    m.print()

