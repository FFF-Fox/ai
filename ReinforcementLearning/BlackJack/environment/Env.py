import numpy as np

class Env:
    deck = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

    def __init__(self):
        self.init_episode()

    def print_params(self):
        """ Print all the environment's parameters. """
        print('Dealer:')
        print("dealer's cards:", env.dealer_cards)
        print("dealer's sum:", env.dealer_sum)
        print("dealer has useable ace:", self.dealer_has_usable_ace)
        print("dealer's face-up card:", self.dealer_showing)
        print('~' * 30)
        print('Player:')
        print("player's cards:", env.player_cards)
        print("player's sum:", env.player_sum)
        print("player has useable ace:", self.player_has_usable_ace)

    def draw_card(self):
        """ Draw a card from the deck.
        Returns the card and the value as a tuple (card,value)."""
        K = len(Env.deck)
        i = np.random.randint(K)
        card = Env.deck[i]

        if i == 0:
            value = 11
        elif i in range(1,10):
            value = i + 1
        elif i in range(10,13):
            value = 10

        return (card, value)

    def dealer_add_card(self, card, value):
        """ Add a new card to the dealer's hand and compute the new sum. """
        self.dealer_cards.append(card)
        # in case that the card is an ace check some conditions
        if value == 11:
            if self.dealer_has_usable_ace:
                value -= 10
            elif self.dealer_sum + value > 21:
                value -= 10
            else:
                self.dealer_has_usable_ace = True
        self.dealer_sum += value

    def init_episode(self):
        self.dealer_cards = []
        self.dealer_sum = 0
        self.dealer_has_usable_ace = False
        self.dealer_showing = 0

        self.player_cards = []
        self.player_sum = 0
        self.player_has_usable_ace = False

    def deal_cards(self):
        """ Deal the first couple of cards:
                1. Dealer and player draw 2 cards
                2. Dealer's first card is known to the player"""
        # draw dealer's cards
        for i in range(2):
            (card,value) = self.draw_card()
            self.dealer_add_card(card, value)
            # expose the faceup card of the dealer
            if i == 0:
                if card in ['10','J','Q','K']:
                    self.dealer_showing = '10'    # using '10' for all the above cards to reduce the state space
                else:
                    self.dealer_showing = card





if __name__ == '__main__':
    print('Env main:')

    env = Env()
    # testing dealer_add_card(...)
    env.init_episode()
    env.deal_cards()
    env.print_params()