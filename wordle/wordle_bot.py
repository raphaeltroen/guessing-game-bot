import numpy as np
from collections import Counter

import sys
from pathlib import Path
parent_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_dir))
import guess_bot as gb

class wordle_bot(gb.guess_bot):
    def __init__(self, words, remaining, word_length):
        gb.guess_bot.__init__(self, words, remaining, 3**word_length)
        self.word_length = word_length #the length of each word in the answer space

    def get_bucket(self, ans, guess) -> int:
        '''returns the number of the bucket returned when the answer is ans and guess is guessed'''
        word_length = len(ans)
        bucket = [0] * word_length

        unmatched_counts = {}

        for i in range(word_length):
            if guess[i] == ans[i]:
                bucket[i] = 2
            else:
                unmatched_counts[ans[i]] = unmatched_counts.get(ans[i], 0) + 1

        for i in range(word_length):
            if bucket[i] != 2:
                if unmatched_counts.get(guess[i], 0) > 0:
                    bucket[i] = 1
                    unmatched_counts[guess[i]] -= 1

        bucket_int = 0
        for b in bucket:
            bucket_int = (bucket_int * 3) + b

        return bucket_int

    def input_to_bucket(self, info) -> int:
        '''info: a string of 5 digits representing the standard output of a worlde game where 0 corresponds to gray, 1 corresponds to yellow, and 2 corresponds to green'''
        ans = 0
        for c in info:
            ans = ans*3 + int(c)
        return ans


words = np.loadtxt("official_wordle_all.txt", dtype=str)
remaining = np.loadtxt("official_wordle_common.txt", dtype=str)
bot = wordle_bot(words, remaining, 5)
print(bot.test_bot(10))