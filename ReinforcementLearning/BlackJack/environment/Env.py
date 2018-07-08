import numpy as np

from Player import Player

class Env(object):
    deck = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

    def __init__(self):
        self.player = Player()
        self.dealer = Player()
        self.init_episode()

    def print_params(self):
        """ Print all the environment's parameters. """
        print('~' * 30)
        print("Episode finished:",self.episode_finished)
        print('Dealer:')
        print(self.dealer)
        print('~' * 30)
        print('Player:')
        print(self.player)
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

    def deal_cards(self):
        """ Deal the first couple of cards:
                1. Dealer and player draw 2 cards
                2. Dealer's first card is known to the player"""
        # draw dealer's cards
        for i in range(2):
            (card,value) = self.draw_card()
            self.dealer.add_card(card, value)
            # expose the faceup card of the dealer
            if i == 0:
                if card in ['10','J','Q','K']:
                    self.dealer_showing = '10'    # using '10' for all the above cards to reduce the state space
                else:
                    self.dealer_showing = card

        # draw player's cards
        while self.player.points < 12:
            (card,value) = self.draw_card()
            self.player.add_card(card, value)

    def init_episode(self):
        self.episode_finished = False

        self.dealer.empty_hand()
        self.player.empty_hand()
        
        self.dealer_showing = 0
        self.deal_cards()

    def dealer_turn(self):
        """ The dealer's turn.
            Dealer draws until it's sum >= 17 """
        while self.dealer.points < 17:
            (card,value) = self.draw_card()
            self.dealer.add_card(card, value)

    def get_state(self):
        """ Get the environment state, as experienced from the player. """
        return (self.dealer_showing, self.player.points, self.player.has_usable_ace)

    def player_action(self, action):
        """ Handle player's action.
            The player can choose to hit or stick. The environment
            makes the appropriate state transition and returns the
            reward.
        """
        if action == "hit":
            (card, value) = self.draw_card()
            self.player.add_card(card, value)
            if self.player.points > 21:
                # player busted
                reward = -1
                self.episode_finished = True
            else:
                reward = 0
            
        if action == "stick":
            self.dealer_turn()
            if self.dealer.points > 21:
                # dealer busted
                reward = 1
            else:
                if self.player.points > self.dealer.points:
                    reward = 1
                elif self.player.points < self.dealer.points:
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
