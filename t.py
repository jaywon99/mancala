import mancala as M

b = M.Mancala()
b.reset()

p = b.next_player()
print(p)
print(",".join( p.test_iter("R3", 3) ))
print(",".join( p.test_iter("R1", 2) ))
print(",".join( p.test_iter("R6", 20) ))
print(",".join( p.test_iter("R3", 5) ))
