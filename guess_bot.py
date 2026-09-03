from abc import ABC, abstractmethod
import numpy as np
from scipy.stats import entropy

class guess_bot(ABC):
    def __init__(self, words, remaining, buckets_cnt):
        self.words = np.array(words)
        self.remaining = np.array(remaining)
        self.buckets_cnt = buckets_cnt

        remaining_vec = self.remaining[:, np.newaxis]
        words_vec = self.words[np.newaxis, :]
        get_bucket_vec = np.vectorize(self.get_bucket)
        self.GBM = get_bucket_vec(remaining_vec, words_vec) #Guess Bucket Matrix, matrix where i can quickly get the bucket of a word guessed on a specific candidate

        self.remaining_idx = np.ones(self.remaining.shape, dtype=bool)

    @abstractmethod
    def get_bucket(self, ans, guess)->int:
        '''returns the bucket id that would be outputted if the answer is "ans" and you guessed "guess"'''
        pass

    @abstractmethod
    def input_to_bucket(self, info) -> int:
        '''returns the bucket id of what was inputted to the system by the game'''
        pass

    def make_guess(self):
        '''returns the optimal guess to make given the remaining words'''
        sub_GBM = self.GBM[self.remaining_idx]

        word_indxs = np.tile(np.arange(sub_GBM.shape[1]), (sub_GBM.shape[0], 1))
        buckets_hist = np.zeros((self.buckets_cnt, sub_GBM.shape[1]), dtype=int)

        np.add.at(buckets_hist, (sub_GBM, word_indxs), 1)
        entropies = entropy(buckets_hist, axis=0, base=2)
        return np.argmax(entropies)

    def simulate_game(self):
        self.remaining_idx = np.ones(self.remaining.shape, dtype=bool)
        turn = 0
        num_remaining = self.remaining.shape[0]
        while num_remaining > 1:
            turn+=1
            guess_idx = self.make_guess()
            print("guessed: ", self.words[guess_idx])
            bucket = self.input_to_bucket(input("return value was: "))
            self.remaining_idx = (self.GBM[:,guess_idx] == bucket) & self.remaining_idx
            num_remaining = self.remaining_idx.sum()
            if bucket == self.buckets_cnt - 1:
                turn -= 1

        if num_remaining==0:
            print("No answer?")
            return 0

        turn += 1
        print("the answer is: ", self.remaining[self.remaining_idx][0], "\n found in ", turn, " moves")
        return 0

    def test_bot(self, times) -> float:
        '''tests how many guesses on average it takes for the bot to get to the solution'''
        total_turns = 0.0
        self.remaining_idx = np.ones(self.remaining.shape, dtype=bool)
        original = self.remaining_idx.copy()
        tests = np.random.choice(self.remaining.shape[0], size=times, replace=False)
        for ans_idx in tests:
            self.remaining_idx = original
            num_remaining = self.remaining.shape[0]
            while num_remaining > 1:
                total_turns += 1
                guess_idx = self.make_guess()
                bucket = self.GBM[ans_idx, guess_idx]
                if bucket == self.buckets_cnt-1:
                    total_turns -=1
                self.remaining_idx = (self.GBM[:, guess_idx] == bucket) & self.remaining_idx
                num_remaining = self.remaining_idx.sum()
            if num_remaining == 0:
                print("No answer?")
                return 0

            total_turns += 1
            print("the answer is: ", self.remaining[self.remaining_idx][0], "\n found in ", total_turns, " moves")

        return total_turns/float(times)
