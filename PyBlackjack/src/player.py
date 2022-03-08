from deck import Deck


class Player:
    '''
    Player class is specific to games involving cards and balances, such as
    blackjack or poker. This class can be extended to any card game if the
    balance is not required.
    '''

    def __init__(self) -> None:
        self._hand = []
        self._balance = 500

    @property
    def hand(self) -> list:
        return [c[:-1] + Deck.get_suit_char(c[-1]) for c in self._hand]

    @hand.setter
    def hand(self, hand: list) -> None:
        if not isinstance(hand, list):
            raise TypeError("Setter only accepts a list.")
        self._hand = hand

    @property
    def balance(self) -> float:
        return round(float(self._balance), 2)

    @balance.setter
    def balance(self, balance: float) -> None:
        if isinstance(balance, str) and \
           balance.lstrip('-').replace('.', '', 1).isdigit():
            self._balance = float(balance)
        elif isinstance(balance, int) or isinstance(balance, float):
            self._balance = balance
        else:
            raise TypeError("Invalid type. Must be either an int, float, or a "
                            + "string of digits.")

    def add_more_cards(self, cards: list) -> None:
        if not isinstance(cards, list):
            raise TypeError("Invalid type. Must be a list.")
        self._hand.extend(cards)

    def clear_hand(self) -> None:
        self.hand.clear()
