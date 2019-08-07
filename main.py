import timeit

import cards
import game
import strategy

def play(seed=None, silent=False, verbose=False):
    g = game.Game()
    options = game.GameOptions(
        print_options = game.PrintOptions.NONE if silent else game.PrintOptions.VERBOSE if verbose else game.PrintOptions.SIMPLE,
        seed = seed,
    )
    g.initialize(cards.DECK, strategy.FirstPossibleStrategy(), options)
    return g.play()

class Stats:
    def __init__(self, n, seeds, total_score, solved_count, time_taken):
        self.n = n
        self.seeds = seeds
        self.total_score = total_score
        self.solved_count = solved_count
        self.time_taken = time_taken
    
    def print(self):
        print('Trials: {}'.format(self.n))
        print('Average score: {}/48'.format(round(self.total_score / self.n, 2)))
        print('Times fully solved: {}/{} ({}%)'.format(self.solved_count, self.n, round(100 * self.solved_count / self.n, 2)))
        print('Time taken: {}s'.format(round(self.time_taken, 2)))

def get_stats(n):
    seeds = list(range(1, n+1))
    result = (0, 0)
    def go():
        total_score = 0
        solved_count = 0
        for seed in seeds:
            score = play(seed=seed, silent=True)
            total_score += score
            if score == 48:
                solved_count += 1
        nonlocal result
        result = (total_score, solved_count)
    time_taken = timeit.timeit(go, number=1)
    return Stats(n, seeds, result[0], result[1], time_taken)

def simulate(n):
    get_stats(n).print()