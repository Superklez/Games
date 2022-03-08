from deck import Deck
from player import Player


class CardGame:
    '''
    Abstract class for card games.
    '''
    def __init__(self):
        self.game_over = True

    def play_game(self):
        while not self.game_over:
            self.play_round()

    def play_round(self):
        raise NotImplementedError("play_round function has not been "
                                  + "implemented")

    @staticmethod
    def ask_to_play(prompt: str = "") -> bool:
        while True:
            answer = input(prompt)
            answer.lower()

            if answer in ["yes", "y"]:
                play = True
            elif answer in ["no", "n"]:
                play = False
            else:
                print("Invalid option. Please try again.")
                continue

            return play


class Blackjack(CardGame):
    max_hand_value = 21

    def __init__(self) -> None:
        super().__init__()
        self.player = Player()
        self.dealer = Player()
        self.deck = Deck()

    def play_game(self) -> None:
        self.game_over = False
        print("Welcome to Blackjack!")
        super().play_game()

    def play_round(self) -> None:
        prompt = f"\nYou are starting with ${self.player.balance : .2f}. " \
                 + "Would you like to play a hand? "
        self.game_over = not self.ask_to_play(prompt)

        # Prompt the user if they want to play
        if self.game_over:
            print(f"You left the game with ${self.player.balance : .2f}.")
            return None

        # Get deck for current round and ask how much the player will bet.
        self.deck = Deck()
        player_bet = self.get_bet(self.player.balance)

        # Draw 2 cards for both the player and the dealer.
        self.player.hand = self.deck.draw(2)
        self.dealer.hand = self.deck.draw(2)

        print(f"You are dealt: {', '.join(self.player.hand)}")

        natural = self.check_for_natural()
        if natural:
            print(f"The dealer is dealt: {', '.join(self.dealer.hand)}")
            print(f"Blackjack! You win ${player_bet * 1.5 : .2f}.")
            self.player.balance += player_bet * 1.5
            return None
        else:
            print(f"The dealer is dealt: {self.dealer.hand[0]}, Unknown")

        player_bust = self.player_move()
        if player_bust:
            print(f"You lost ${player_bet : .2f}.")
            self.player.balance -= player_bet
            if self.player.balance < 0.01:
                print("\nYou've ran out of money. Please restart this "
                      + "program to try again. Goodbye!")
                self.game_over = True
            return None

        dealer_bust = self.dealer_move()
        if dealer_bust:
            print(f"You win ${player_bet : .2f}.")
            self.player.balance += player_bet
            return None

        player_hand_value = self.get_hand_value(self.player.hand)
        dealer_hand_value = self.get_hand_value(self.dealer.hand)

        if player_hand_value > dealer_hand_value:
            print(f"You win ${player_bet : .2f}.")
            self.player.balance += player_bet
        elif player_hand_value < dealer_hand_value:
            print(f"You lose ${player_bet : .2f}.")
            self.player.balance -= player_bet
            if self.player.balance < 0.01:
                print("\nYou've ran out of money. Please restart this "
                      + "program to try again. Goodbye!")
                self.game_over = True
        else:
            print("You tie. Your bet has been returned.")

    @staticmethod
    def get_bet(balance: float) -> float:
        min_bet = 1

        while True:
            bet = input("Place your bet: $")
            if not bet.replace('.', '', 1).isdigit():
                print("You must enter a positive number. Please try again")
                continue

            bet = float(bet)
            if bet < min_bet:
                print(f"The minimum bet is ${min_bet : .2f}. Please try "
                      + "again.")
                continue
            elif bet > balance:
                print("Insufficient funds. Bet must not exceed "
                      + f"${balance : .2f}.")
                continue

            return bet

    def player_move(self) -> None:
        bust = False

        while True:
            hit = self.ask_if_hit()

            if hit:
                self.player.add_more_cards(self.deck.draw(1))
                print(f"You are dealt: {self.player.hand[-1]}")
                print(f"You not have: {', '.join(self.player.hand)}")

            hand_value = self.get_hand_value(self.player.hand)

            if hand_value > self.max_hand_value:
                print(f"Your hand value is now over {self.max_hand_value}.")
                bust = True
                break
            elif not hit:
                break

        return bust

    def dealer_move(self) -> bool:
        bust = False
        hand_value = self.get_hand_value(self.dealer.hand)
        dealer_max_hand_value = 17

        print(f"The dealer has: {', '.join(self.dealer.hand)}")

        while hand_value < dealer_max_hand_value:
            self.dealer.add_more_cards(self.deck.draw(1))
            print(f"The dealer hits and is dealt: {self.dealer.hand[-1]}")
            print(f"The dealer now has: {', '.join(self.dealer.hand)}")
            hand_value = self.get_hand_value(self.dealer.hand)

        if hand_value > self.max_hand_value:
            bust = True
            print("The dealer busts.")
        else:
            print("The dealer stays.")

        return bust

    @staticmethod
    def ask_if_hit() -> bool:
        while True:
            ans = input("Would you like to hit or stay? ").strip().lower()
            if ans == "hit":
                return True
            elif ans == "stay":
                return False
            else:
                print("That is not a valid option. Please try again.")

    @classmethod
    def get_hand_value(cls, hand: list) -> int:
        hand_value = 0
        num_aces = 0

        for card in hand:
            card = card[0]
            if card.isdigit():
                hand_value += int(card)
            elif card == 'A':
                hand_value += 11
                num_aces += 1
            elif card in ['J', 'Q', 'K']:
                hand_value += 10

        while hand_value > cls.max_hand_value and num_aces > 0:
            hand_value -= 10
            num_aces -= 1

        return hand_value

    def check_for_natural(self):
        natural = False

        if len(self.player.hand) == 2 \
           and self.get_hand_value(self.player.hand) == self.max_hand_value \
           and self.get_hand_value(self.dealer.hand) != self.max_hand_value:
            natural = True

        return natural
