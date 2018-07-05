import numpy as np

class Env:
    deck = ['A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K']

    def __init__(self):
        self.dealer_cards = []
        self.dealer_sum = 0

        self.player_cards = []
        self.player_sum = 0

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



if __name__ == '__main__':
    print('Env main:')

    env = Env()
    print ('some random generated cards:')

    for i in range(15):
        card = env.draw_card()
        print(card)