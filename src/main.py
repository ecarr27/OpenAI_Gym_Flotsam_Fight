from FlotsamFight import FlotsamFight
from time import time
import sys

start = time()

gameCount = 3
loud = True
if (len(sys.argv) >= 3):
	gameCount = int(sys.argv[1])
	loud = sys.argv[2]
	if (loud == "False" or loud == "0"):
		loud = False
	else:
		loud = True

f = FlotsamFight()
f.play(gameCount, loud)

end = time()
print("Total run time:", end - start)