import random

class Deck(object):
    def __init__(self):
        self.cards = [1,2,3,4,5,6,7,8,9,10,11,12,13] * 4
    
    def configure(self, parameter_list):
        pass

    def shuffle(self):
        random.shuffle(self.cards)
        return self

    def popCard(self):
        random.shuffle(self.cards)
        return self.cards.pop()

class Player(object):
    def __init__(self, number):
        self.hand = []
        self.number = int(number)

    def configure(self, parameter_list):
        pass
    
    def drawCard(self, deck, count = 1):
        for i in range(count):
            self.hand.append(deck.popCard())
    
    def calculteScore(self):
        score = 0
        for c in self.hand:
            score += c
        return score

class Dealer(Player):
    pass

class Game(object):
    def __init__(self, numPlayer = 10):
        self.deck = Deck().shuffle()
        self.dealer = Dealer(0)
        self.players = [Player(i) for i in range(numPlayer)]

    def configure(self, parameter_list):
        pass
    
    def draw(self):
        self.dealer.drawCard(self.deck, count = 2)
        for p in self.players:
            p.drawCard(self.deck, count = 2)

    def score(self):
        dealerScore = self.dealer.calculteScore()
        for p in self.players:
            playererScore = p.calculteScore()
            if playererScore > dealerScore:
                print("Player " + str(p.number) + " win: " + str(playererScore) + " vs " + str(dealerScore))
            else:
                print("Player " + str(p.number) + " lose: " + str(playererScore) + " vs " + str(dealerScore))

    def run(self):
        self.draw()
        self.score()

if __name__ == "__main__":
    game = Game()
    game.run()