import random

class Card(object):
    def __init__(self, char):
        self.expval = char
        self.values = {
            "A": [1],
            "2": [2],
            "3": [3],
            "4": [4],
            "5": [5],
            "6": [6],
            "7": [7],
            "8": [8],
            "9": [9],
            "10": [10],
            "J": [10],
            "Q": [10],
            "K": [10]
        }[char]
        self.hidden = True

    def __str__(self):
        return self.expval if not self.hidden else "*"

class Deck(object):
    def __init__(self):
        self.cards = []
        for _ in range(4):
            self.cards += [Card(x) for x in ["A", "2", "3", "4", "5", "6", "7", \
                                        "8", "9", "10", "J", "Q", "K"]]
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)
        return self

    def pop(self):
        self.shuffle()
        return self.cards.pop()

    def recruit(self):
        self.__init__()


IDENTITY_DEALER = 0
IDENTITY_PLAYER = 1

STATUS_PLAYING = 0
STATUS_STICK = 1
STATUS_BUST = 2

class Player(object):
    def __init__(self, identity, _id):
        self.cards = []
        self.identity = identity
        self.id = _id
        self.status = STATUS_PLAYING

    def hit(self, deck):
        if len(self.cards) >= 2:
            print("Player {} HIT".format(self.id))
        self.cards.append(deck.pop())
        if len(self.cards) == 1:
            self.cards[0].hidden = False

    def stick(self):
        if len(self.cards) >= 2:
            print("Player {} STICK".format(self.id))
        self.status = STATUS_STICK

    def move(self, deck, players):
        pass
    
    @property
    def sum(self):
        return sum([x.values[0] for x in self.cards])

    @property
    def is_playing(self):
        return True if self.status == STATUS_PLAYING else False

    def __str__(self):
        return "Player {}: {}".format(self.id, [str(x) for x in self.cards])

    def show(self):
        print("Player {}: {}".format(self.id, [x.expval for x in self.cards]),
              "SUM", self.sum)


class Dealer(Player):
    def move(self, deck, players=[]):
        if self.is_playing:
            if self.sum < 17:
                self.hit(deck)
            else:
                self.stick()


class InputPlayer(Player):
    def move(self, deck, players=[]):
        for p in players:
            if p.id != self.id:
                print(p)
        print("Player {} (me): {}".format(self.id, [x.expval \
                                                    for x in self.cards]))
        print("My sum now is", self.sum)
        while True:
            decision = input()
            if decision == 'H':
                self.hit(deck)
                break
            elif decision == 'S':
                self.stick()
                break
            else:
                print("Please input 'H' for hit for 'S' for stick")


class Game(object):
    def __init__(self, num_players=1):
        self.deck = Deck()
        self.dealer = Dealer(IDENTITY_DEALER, 0)
        self.players = [InputPlayer(IDENTITY_PLAYER, i) \
                        for i in range(1, num_players+1)]
        for _ in range(2):
            self.dealer.hit(self.deck)
            for p in self.players:
                p.hit(self.deck)

    @property
    def all_players(self):
        return [self.dealer] + self.players


    # 3 Cases to determine the current game status
    @property
    def is_all_stick(self):
        for p in self.all_players:
            if p.status != STATUS_STICK:
                return False
        return True

    @property
    def is_dealer_bust(self):
        if self.dealer.status == STATUS_BUST:
            return True
        return False

    @property
    def is_players_bust(self):
        for p in self.players:
            if p.status != STATUS_BUST:
                return False
        return True

    @property
    def is_end(self):
        return self.is_all_stick or self.is_dealer_bust or self.is_players_bust

    def check(self, player):
        if player.status != STATUS_BUST and player.sum > 21:
            player.status = STATUS_BUST

    def run(self):
        print("GAME START")
        for p in self.all_players:
            print(p)
        while not self.is_end:
            # Dealer first turn
            if self.dealer.status == STATUS_PLAYING:
                self.dealer.move(self.deck, self.all_players)
                self.check(self.dealer)
                if self.is_dealer_bust:
                    break
            # Then come to the players
            for p in self.players:
                if p.status == STATUS_PLAYING:
                    p.move(self.deck, self.all_players)
                    self.check(p)

        print("\nGame Ends")
        print("\n- SCOREBOARD -")
        for p in self.all_players:
            p.show()
        print("\nResults")

        if self.is_dealer_bust:
            print("The dealer busts, players win")
        elif self.is_players_bust:
            print("The player bust, dealer wins")
        else:
            final = sorted(self.all_players, key=lambda x: x.sum, reverse=True)
            final = [f for f in final if f.status != STATUS_BUST]
            print("Winner is {}\n".format(final[0].id))
        
        

if __name__ == "__main__":
    game = Game()
    game.run()