import abc
import random

class Strategy(abc.ABC):
    def move(self, stock, heap, tableau):
        pass

    def first_target(self, tableau):
        for i in range(len(tableau)):
            if self.is_target(tableau[i]):
                return i
        return None # Shouldn't happen. Strategy should only be called if there are piles with no cards.

    def all_targets(self, tableau):
        return list(idx for idx, pile in enumerate(tableau) if self.is_target(pile))

    def first_source(self, tableau):
        for i in range(len(tableau)):
            if self.is_source(tableau[i]):
                return i
        return None # Shouldn't happen. Strategy should only be called if there are piles with multiple cards.

    def all_sources(self, tableau):
        return list(idx for idx, pile in enumerate(tableau) if self.is_source(pile))

    def is_target(self, pile):
        return len(pile) == 0

    def is_source(self, pile):
        return len(pile) > 1

class NoOpStrategy(Strategy):
    def move(self, stock, heap, tableau):
        return None

class FirstPossibleStrategy(Strategy):
    def move(self, stock, heap, tableau):
        target_idx = self.first_target(tableau)
        if target_idx is not None:
            source_idx = self.first_source(tableau)
            if source_idx is not None:
                return (source_idx, target_idx)
        return None

class RandomStrategy(Strategy):
    def __init__(self, seed=None):
        self.rand = random.Random()
        if seed is not None:
            self.rand.seed(seed)

    def move(self, stock, heap, tableau):
        sources = self.all_sources(tableau)
        targets = self.all_targets(tableau)
        if len(sources) == 0 or len(targets) == 0:
            return None
        else:
            source_idx = self.rand.choice(sources)
            target_idx = self.rand.choice(targets)
            return (source_idx, target_idx)
