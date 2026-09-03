import numpy as np
import time

import sys
from pathlib import Path
parent_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_dir))
import wordle_bot as wb

words = np.loadtxt("official_wordle_all.txt", dtype=str)
remaining = np.loadtxt("official_wordle_common.txt", dtype=str)

start = time.perf_counter()
bot = wb.wordle_bot(words, remaining, 5)
end = time.perf_counter()
print("initializing time: ", end-start)

bot.simulate_game()

start = time.perf_counter()
acc = bot.test_bot(10)
end = time.perf_counter()
print("got accuracy: ", acc, "in testing time: ", end-start)