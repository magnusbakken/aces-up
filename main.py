import random
import timeit

import cards
import game
import strategy

def play(strat, rng=None, silent=False, verbose=False):
    g = game.Game()
    options = game.GameOptions(
        print_options = game.PrintOptions.NONE if silent else game.PrintOptions.VERBOSE if verbose else game.PrintOptions.SIMPLE,
        rng = rng,
    )
    g.initialize(cards.DECK, strat, options)
    return g.play()

class Stats:
    def __init__(self, n, total_score, solved_count, time_taken):
        self.n = n
        self.total_score = total_score
        self.solved_count = solved_count
        self.time_taken = time_taken
    
    def print(self):
        print('Trials: {}'.format(self.n))
        print('Average score: {}/48'.format(round(self.total_score / self.n, 2)))
        print('Times fully solved: {}/{} ({}%)'.format(self.solved_count, self.n, round(100 * self.solved_count / self.n, 2)))
        print('Time taken: {}s'.format(round(self.time_taken, 2)))

def get_stats(n, strat, random_shuffles, silent, verbose):
    result = (0, 0)
    def go():
        total_score = 0
        solved_count = 0
        rng = random.Random()
        for seed in range(1, n+1):
            if not random_shuffles:
                rng.seed(seed)
            score = play(strat, rng=rng, silent=silent, verbose=verbose)
            total_score += score
            if score == 48:
                solved_count += 1
        nonlocal result
        result = (total_score, solved_count)
    time_taken = timeit.timeit(go, number=1)
    return Stats(n, result[0], result[1], time_taken)

def simulate(n, strat, random_shuffles=False, silent=True, verbose=False):
    get_stats(n, strat, random_shuffles, silent, verbose).print()

def simulate_stupid(n):
    simulate(n, strategy.FirstPossibleStrategy())

def simulate_random(n, strategy_seed=None):
    simulate(n, strategy.RandomStrategy(strategy_seed))

def simulate_trivial_removal(n):
    simulate(n, strategy.TrivialRemovalStrategy())

def simulate_minimization(n):
    simulate(n, strategy.MinimizationStrategy())

STRATEGIES = ['NOOP', 'SIMPLE', 'RANDOM', 'TRIVIAL', 'MINIMIZATION']

def create_strategy(args):
    name = args.strategy
    if name == 'NOOP':
        return strategy.NoOpStrategy()
    elif name =='SIMPLE':
        return strategy.FirstPossibleStrategy()
    elif name =='RANDOM':
        return strategy.RandomStrategy(args.strategy_seed)
    elif name == 'TRIVIAL':
        return strategy.TrivialRemovalStrategy()
    elif name == 'MINIMIZATION':
        return strategy.MinimizationStrategy(args.verbose)
    else:
        raise Exception('Invalid strategy: {}'.format(name))

STRATEGY_DESCRIPTION = '''The strategy to use. The default is MINIMIZATION.
- NOOP: Never moves cards.
- SIMPLE: Always moves the first available card from the left to the first empty space from the left.
- RANDOM: Moves a random card to a random empty space.
- TRIVIAL: Detects cases where moving a card to an empty space causes it to immediately be discarded.
- MINIMIZATION: Makes the move that will cause the maximum number of cards to get discarded in each round.'''

def parse_cli():
    import argparse
    parser = argparse.ArgumentParser(
        description='Simulate Aces Up solves with different strategies',
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('n', metavar='N', type=int, help='The number of trials to run.')
    parser.add_argument('-s', '--strategy', choices=STRATEGIES, default='MINIMIZATION', help=STRATEGY_DESCRIPTION)
    parser.add_argument('-r', '--random-shuffles', action='store_true',
        help='Whether to use random shuffles. If not set, any combination of N and --strategy will give the same result each time.')
    parser.add_argument('--strategy-seed', type=int,
        help='The seed for the RNG used by the strategy function. This is separate from the RNG used to shuffle cards. Currently this is only applicable for the RANDOM strategy.')
    parser.add_argument('-v', '--verbose', action='store_true',
        help='Output internal information. Note that enabling this option will cause the program to run much slower.')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_cli()
    strat = create_strategy(args)
    simulate(args.n, strat, args.random_shuffles, verbose=args.verbose)