import random
from abc import ABC, abstractmethod
import numpy as np
from scipy.stats import entropy

class guess_bot(ABC):
    def __init__(self, words, remaining, buckets_cnt):
        self.words = np.array(words)
        self.remaining = np.array(remaining)
        self.buckets_cnt = buckets_cnt


        remaining_col = self.remaining[:, np.newaxis]
        words_row = self.words[np.newaxis, :]
        get_bucket_vec = np.vectorize(self.get_bucket)
        self.GBM = get_bucket_vec(remaining_col, words_row) #matrix where i can quickly get the bucket of a word guessed on a specific candidate

    @abstractmethod
    def get_bucket(self, ans, guess)->int:
        '''returns the bucket id that would be outputted if the answer is "ans" and you guessed "guess"'''
        pass

    @abstractmethod
    def input_to_bucket(self, info) -> int:
        '''returns the bucket id of what was inputted to the system by the game'''
        pass

    def get_entropy(self, word) -> float:
        '''returns the shannon entropy in the guess "word"'''
        v = np.zeros(self.buckets_cnt, dtype=float)
        for contender in self.remaining:
            v[self.get_bucket(contender, word)]+=1.0
        return entropy(v, base=2)

    def make_guess(self):
        '''returns the optimal guess to make given the remaining words'''
        get_entropy_vec = np.vectorize(self.get_entropy)
        entropies = get_entropy_vec(self.words)
        best_index = np.argmax(entropies)
        return self.words[best_index]

    def simulate_game(self):
        turn = 0
        while len(self.remaining) > 1:
            turn+=1
            guess = self.make_guess()
            print("guessed: ", guess)
            bucket = self.input_to_bucket(input("return value was: "))
            self.remaining = [contender for contender in self.remaining if self.get_bucket(contender, guess)==bucket]

        if len(self.remaining)==0:
            print("No answer?")
        else:
            print("the answer is: ", self.remaining[0], "\n found in ", turn, " moves")
        return 0

    def test_bot(self, times) -> float:
        '''tests how many guesses on average it takes for the bot to get to the solution'''
        turns = 0.0
        original = self.remaining
        for _ in range(times):
            self.remaining = original
            ans = np.random.choice(self.remaining)
            while len(self.remaining)>1:
                turns+=1
                guess = self.make_guess()
                bucket = self.get_bucket(ans, guess)
                self.remaining = [contender for contender in self.remaining if self.get_bucket(contender, guess) == bucket]

            if len(self.remaining)==0:
                print("No answer?")
                return 0

        return turns/float(times)

