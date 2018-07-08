class Player(object):
    def empty_hand(self):
        """ Empty the player's hand. """
        self.cards = []
        self.points = 0
        self.has_usable_ace = False

    def __init__(self):
        self.empty_hand()

    def __repr__(self):
        s = "{}: {}\n{}: {}\n{}: {}".format('Cards', self.cards, 'Points', self.points, 'Has usable ace', self.has_usable_ace)
        return s

    def add_card(self, card, value):
        """ Add a new card to the player's hand and compute the new points. """
        self.cards.append(card)
        # in case that the card is an ace check some conditions
        if value == 11:
            if self.has_usable_ace:
                value -= 10
            elif self.points + value > 21:
                value -= 10
            else:
                self.has_usable_ace = True

        self.points += value        
        if self.points > 21 and self.has_usable_ace:
            self.points -= 10    # Use the ace as 1 instead of 11
            self.has_usable_ace = False

if __name__ == '__main__':
    p = Player()
    print(p.points)
    p.add_card('A', 11)
    print(p.points)
    p.add_card('A', 11)
    print(p.points)
    p.add_card('10', 10)
    print(p.points)
    print(p)