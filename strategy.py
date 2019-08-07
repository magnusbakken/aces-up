import abc

class Strategy(abc.ABC):
    def move(self, stock, heap, tableau):
        pass

    def first_target(self, tableau):
        for i in range(len(tableau)):
            if self.is_target(tableau[i]):
                return i
        return None # Shouldn't happen. Strategy should only be called if there are piles with no cards.

    def first_source(self, tableau):
        for i in range(len(tableau)):
            if self.is_source(tableau[i]):
                return i
        return None # Shouldn't happen. Strategy should only be called if there are piles with multiple cards.

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