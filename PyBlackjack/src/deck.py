import random


class Deck:
    cards = ['2', '3', '4', '5', '6', '7', '8', '9', 'J', 'Q', 'K', 'A']
    suits = ['H', 'D', 'C', 'S']
    suit_chars = {'H': u'\u2665', 'D': u'\u2666', 'C': u'\u2663',
                  'S': u'\u2660'}

    def __init__(self) -> None:
        self._deck = [c + s for s in self.suits for c in self.cards]
        self.shuffle()

    @property
    def deck(self) -> list:
        return self._deck[:]

    def draw(self, n: int) -> list:
        cards = []
        for _ in range(n):
            if not self._deck:
                break
            cards.append(self._deck.pop())
        return cards

    def shuffle(self) -> None:
        random.shuffle(self._deck)

    def sort(self, reverse: bool = False) -> None:
        '''
        Sort the deck by value then by suit.
        '''
        self._deck.sort(key=lambda c: (self.suits.index(c[1]),
                                       self.cards.index(c[0])),
                        reverse=reverse)

    @classmethod
    def get_suit_char(cls, suit: str) -> str:
        if suit not in cls.suit_chars:
            raise ValueError("Please provide a valid suit "
                             + f"({'/'.join(cls.suit_chars)}).")
        return cls.suit_chars[suit]

    def __str__(self) -> str:
        return ", ".join(c[:-1] + self.get_suit_char(c[-1]) for c in 
                         self._deck)
