import numpy as np

class Env:
    deck = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

    def __init__(self):
        self.init_episode()

    def print_params(self):
        """ Print all the environment's parameters. """
        print('~' * 30)
        print("Episode finished:",self.episode_finished)
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
        print('~' * 30)

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

        if self.dealer_sum + value > 21 and self.dealer_has_usable_ace:
            self.dealer_sum -= 10    # Use the ace as 1 instead of 11
            self.dealer_sum += value
            self.dealer_has_usable_ace = False
        else:
            self.dealer_sum += value

    def player_add_card(self, card, value):
        """ Add a new card to the player's hand and compute the new sum. """
        self.player_cards.append(card)
        # in case that the card is an ace check some conditions
        if value == 11:
            if self.player_has_usable_ace:
                value -= 10
            elif self.player_sum + value > 21:
                value -= 10
            else:
                self.player_has_usable_ace = True

        if self.player_sum + value > 21 and self.player_has_usable_ace:
            self.player_sum -= 10    # Use the ace as 1 instead of 11
            self.player_sum += value
            self.player_has_usable_ace = False
        else:
            self.player_sum += value

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

        # draw player's cards
        while self.player_sum < 12:
            (card,value) = self.draw_card()
            self.player_add_card(card, value)

    def init_episode(self):
        self.dealer_cards = []
        self.dealer_sum = 0
        self.dealer_has_usable_ace = False
        self.dealer_showing = 0

        self.player_cards = []
        self.player_sum = 0
        self.player_has_usable_ace = False

        self.episode_finished = False

        self.deal_cards()

    def dealer_turn(self):
        """ The dealer's turn.
            Dealer draws until it's sum >= 17 """
        while self.dealer_sum < 17:
            (card,value) = self.draw_card()
            self.dealer_add_card(card, value)

    def get_state(self):
        """ Get the environment state, as experienced from the player. """
        return (self.player_sum, self.dealer_showing, self.player_has_usable_ace)

    def player_action(self, action):
        """ Handle player's action.
            The player can choose to hit or stick. The environment
            makes the appropriate state transition and returns the
            reward.
        """
        if action == "hit":
            (card, value) = self.draw_card()
            self.player_add_card(card, value)
            if self.player_sum > 21:
                # player busted
                reward = -1
                self.episode_finished = True
            else:
                reward = 0
            
        if action == "stick":
            self.dealer_turn()
            if self.dealer_sum > 21:
                # dealer busted
                reward = 1
            else:
                if self.player_sum > self.dealer_sum:
                    reward = 1
                elif self.player_sum < self.dealer_sum:
                    reward = -1
                else:
                    reward = 0
            self.episode_finished = True

        return reward


if __name__ == '__main__':
    print('Env main:')

    env = Env()
    env.init_episode()    
    env.print_params()
    while not env.episode_finished:
        action = input("hit / stick? -> ")
        reward = env.player_action(action)
        env.print_params()
        print ("Reward:", reward)
