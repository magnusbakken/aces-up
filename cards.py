import enum

class OrderedEnum(enum.Enum):
    def __ge__(self, other):
        if self.__class__ is other.__class__:
            return self.value >= other.value
        return NotImplemented

    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self.value > other.value
        return NotImplemented

    def __le__(self, other):
        if self.__class__ is other.__class__:
            return self.value <= other.value
        return NotImplemented

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented

class Suit(OrderedEnum):
    CLUBS = 1
    DIAMONDS = 2
    HEARTS = 3
    SPADES = 4

SUIT_SHORT_NAMES = {
    Suit.CLUBS: 'c',
    Suit.DIAMONDS: 'd',
    Suit.HEARTS: 'h',
    Suit.SPADES: 's',
}

class Rank(OrderedEnum):
    TWO = 1
    THREE = 2
    FOUR = 3
    FIVE = 4
    SIX = 5
    SEVEN = 6
    EIGHT = 7
    NINE = 8
    TEN = 9
    JACK = 10
    QUEEN = 11
    KING = 12
    ACE = 13

RANK_SHORT_NAMES = {
    Rank.TWO: '2',
    Rank.THREE: '3',
    Rank.FOUR: '4',
    Rank.FIVE: '5',
    Rank.SIX: '6',
    Rank.SEVEN: '7',
    Rank.EIGHT: '8',
    Rank.NINE: '9',
    Rank.TEN: 'T',
    Rank.JACK: 'J',
    Rank.QUEEN: 'Q',
    Rank.KING: 'K',
    Rank.ACE: 'A',
}

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self._repr_cache = None
        self._str_cache = None
    
    def __repr__(self):
        if not self._repr_cache:
            self._repr_cache = 'Card({}, {})'.format(self.rank, self.suit)
        return self._repr_cache

    def __str__(self):
        if not self._str_cache:
            self._str_cache = RANK_SHORT_NAMES[self.rank] + SUIT_SHORT_NAMES[self.suit]
        return self._str_cache

    def beats(self, other):
        return self.suit == other.suit and self.rank > other.rank

DECK = [Card(rank, suit) for rank in list(Rank) for suit in list(Suit)]