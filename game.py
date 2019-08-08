import enum
import random

import cards

class Game:
    TABLEAU_SIZE = 4

    def __init__(self):
        self._initialized = False
        self._finished = False

    @property
    def initialized(self):
        return self._initialized

    @property
    def finished(self):
        return self._finished

    def initialize(self, deck, strategy, options):
        self._initialized = False
        self._finished = False
        rand = random.Random()
        if options.seed:
            rand.seed(options.seed)
        shuffled_deck = deck[:]
        rand.shuffle(shuffled_deck)
        self.state = GameState(shuffled_deck, Game.TABLEAU_SIZE)
        self.strategy = strategy
        self.options = options
        self._initialized = True

    def play(self):
        if not self.initialized:
            raise Exception('Game has not been initialized')
        elif self.finished:
            raise Exception('Game is finished')
        if self.options.print_options == PrintOptions.VERBOSE:
            print('Starting game...')
            print('Initial stock: {}'.format(', '.join(str(card) for card in self.state.stock)))
            print()
        round_count = 1
        while len(self.state.stock) > 0:
            new_cards = self.state.deal()
            if self.options.print_options != PrintOptions.NONE:
                if round_count > 1:
                    print()
                self.print_tableau('Round {}'.format(round_count))
            if self.options.print_options != PrintOptions.NONE:
                print('Dealt: {}'.format(', '.join(str(card) for card in new_cards)))
            initial_clear_count = self.state.clear_all()
            if self.options.print_options != PrintOptions.NONE and initial_clear_count > 0:
                discards = self.state.heap[-initial_clear_count:]
                print('Discarded: {}'.format(', '.join(str(card) for card in discards)))
            if self.options.print_options == PrintOptions.VERBOSE:
                self.print_tableau('After initial clear')
                self.print_internals()
            move_count = 1
            while self.state.can_move() and self.make_move():
                if self.options.print_options == PrintOptions.VERBOSE:
                    self.print_tableau('After making move {}'.format(move_count), empty_line=False)
                clear_count = self.state.clear_all()
                if self.options.print_options != PrintOptions.NONE and clear_count > 0:
                    discards = self.state.heap[-clear_count:]
                    print('Discarded: {}'.format(', '.join(str(card) for card in discards)))
                if self.options.print_options == PrintOptions.VERBOSE:
                    self.print_tableau('Clear after move {}'.format(move_count), empty_line=False)
                    self.print_internals()
                move_count += 1
            round_count += 1
        if self.options.print_options != PrintOptions.NONE:
            print()
            print('Number of discarded cards: {}'.format(len(self.state.heap)))
        self._finished = True
        return len(self.state.heap)

    def make_move(self):
        move = self.strategy.move(self.state)
        if move:
            from_idx, to_idx = move
            if self.options.print_options != PrintOptions.NONE:
                print('Moved {} to column {}'.format(self.state.peek(from_idx), to_idx+1))
            self.state.move(from_idx, to_idx)
            return True
        else:
            return False
    
    def print_tableau(self, label = None, empty_line = True):
        if label:
            print(label)
        height = len(self.state.tableau[self.state.biggest_pile()])
        for row in range(height):
            for idx in range(Game.TABLEAU_SIZE):
                cell =  self.state.tableau[idx][row] if len(self.state.tableau[idx]) > row else '  '
                print(cell, end=' ')
            print()
        if empty_line:
            print()
    
    def print_internals(self):
        print('Stock: {}'.format(', '.join(str(card) for card in self.state.stock)))
        print('Heap: {}'.format(', '.join(str(card) for card in self.state.heap)))

class GameState:
    def __init__(self, deck, size):
        self.stock = deck
        self.heap = []
        self.tableau = []
        for _ in range(size):
            self.tableau.append([])
 
    def deal(self):
        new_cards = []
        for pile in self.tableau:
            card = self.draw()
            pile.append(card)
            new_cards.append(card)
        return new_cards
       
    def draw(self):
        return self.stock.pop()

    def clear(self, idx):
        self.heap.append(self.tableau[idx].pop())

    def peek(self, idx):
        pile = self.tableau[idx]
        return pile[-1] if pile else None
    
    def move(self, from_idx, to_idx):
        self.tableau[to_idx].append(self.tableau[from_idx].pop())
    
    def biggest_pile(self):
        max_idx = None
        max_length = -1
        for idx in range(Game.TABLEAU_SIZE):
            length = len(self.tableau[idx])
            if length > max_length:
                max_idx = idx
                max_length = length
        return max_idx

    def clear_all(self):
        total_clear_count = 0
        cleared_now = True
        while cleared_now:
            cleared_now = False
            for idx in range(Game.TABLEAU_SIZE):
                clear_count = self.clear_idx(idx)
                total_clear_count += clear_count
                cleared_now = cleared_now or clear_count > 0
        return total_clear_count
    
    def clear_idx(self, idx):
        clear_count = 0
        card = self.peek(idx)
        while card is not None:
            cleared_now = False
            for other in (self.peek(i) for i in range(Game.TABLEAU_SIZE) if i != idx):
                if other is not None and other.beats(card):
                    clear_count += 1
                    cleared_now = True
                    self.clear(idx)
                    card = self.peek(idx)
                    if card is None:
                        break
            if not cleared_now:
                break
        return clear_count

    def can_move(self):
        has_empty = False
        has_multi = False
        for pile in self.tableau:
            if not has_empty and not pile:
                has_empty = True
            elif not has_multi and len(pile) > 1:
                has_multi = True
            if has_empty and has_multi:
                return True
        return False

class PrintOptions(enum.Enum):
    NONE = 0
    SIMPLE = 1
    VERBOSE = 2

class GameOptions:
    def __init__(self, print_options = PrintOptions.SIMPLE, seed = None):
        self.print_options = print_options
        self.seed = seed