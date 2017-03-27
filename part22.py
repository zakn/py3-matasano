import time
import random
from part21 import myMT



initial_t = int(time.time())

time.sleep(random.randint(40, 1000))

seedtime = int(time.time())
print(seedtime)
x = myMT(seedtime)

time.sleep(random.randint(40, 1000))

outp = x.rand()
print(outp)


guess_time = int(time.time())
for i in range(2000):
    guess_seed = guess_time - i
    y = myMT(guess_seed)
    guess_outp = y.rand()

    if (guess_outp == outp):
        result = guess_seed
        print(result)
