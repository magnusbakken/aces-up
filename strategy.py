import abc
import random

class Strategy(abc.ABC):
    def move(self, state):
        pass

    def first_target(self, state):
        for i in range(len(state.tableau)):
            if self.is_target(state.tableau[i]):
                return i
        return None # Shouldn't happen. Strategy should only be called if there are piles with no cards.

    def all_targets(self, state):
        return list(idx for idx, pile in enumerate(state.tableau) if self.is_target(pile))

    def first_source(self, state):
        for i in range(len(state.tableau)):
            if self.is_source(state.tableau[i]):
                return i
        return None # Shouldn't happen. Strategy should only be called if there are piles with multiple cards.

    def all_sources(self, state):
        return list(idx for idx, pile in enumerate(state.tableau) if self.is_source(pile))

    def is_target(self, pile):
        return len(pile) == 0

    def is_source(self, pile):
        return len(pile) > 1

class NoOpStrategy(Strategy):
    def move(self, state):
        return None

class FirstPossibleStrategy(Strategy):
    def move(self, state):
        target_idx = self.first_target(state)
        if target_idx is not None:
            source_idx = self.first_source(state)
            if source_idx is not None:
                return (source_idx, target_idx)
        return None

class RandomStrategy(Strategy):
    def __init__(self, seed=None):
        self.rand = random.Random()
        if seed is not None:
            self.rand.seed(seed)

    def move(self, state):
        sources = self.all_sources(state)
        targets = self.all_targets(state)
        if len(sources) == 0 or len(targets) == 0:
            return None
        else:
            source_idx = self.rand.choice(sources)
            target_idx = self.rand.choice(targets)
            return (source_idx, target_idx)

class TrivialRemovalStrategy(Strategy):
    def move(self, state):
        sources = self.all_sources(state)
        target_idx = self.first_target(state)
        if len(sources) == 0 or target_idx is None:
            return None
        if len(sources) == 1:
            return (sources[0], target_idx)
        preferred_source_idx = sources[0]
        for source_idx in sources:
            if state.tableau[source_idx][-2].beats(state.tableau[source_idx][-1]):
                preferred_source_idx = source_idx
                break
        return (preferred_source_idx, target_idx)