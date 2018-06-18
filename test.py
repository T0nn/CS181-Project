from learn import *
import pickle

table = None
with open('table', 'rb') as f:
    table = pickle.load(f)

class RandomPlayer(Player):
    def move(self, deck, players=[]):
        decision = random.choice([MOVE_HIT, MOVE_STICK])
        if decision == MOVE_HIT:
            self.hit(deck)
        else:
            self.stick()


class QPolicyPlayer(Player):
    def move(self, deck, players=[]):
        player_status = self._learn_stat(True)
        dealer_status = [p for p in players if p.identity == \
                            IDENTITY_DEALER][0]._learn_stat()
        game_status = tuple([player_status, dealer_status])
        hit_reward = table.lookup(game_status, MOVE_HIT)
        stick_reward = table.lookup(game_status, MOVE_STICK)
        decision = MOVE_HIT if hit_reward > stick_reward else MOVE_STICK
        if decision == MOVE_HIT:
            self.hit(deck)
        else:
            self.stick()

class RandomGame(Game):
    def __init__(self):
        self.deck = Deck()
        self.dealer = Dealer(IDENTITY_DEALER, 0)
        self.players = [RandomPlayer(IDENTITY_PLAYER, 1)]
        for _ in range(2):
            self.dealer.hit(self.deck)
            for p in self.players:
                p.hit(self.deck)


class TestGame(Game):
    def __init__(self):
        self.deck = Deck()
        self.dealer = Dealer(IDENTITY_DEALER, 0)
        self.players = [QPolicyPlayer(IDENTITY_PLAYER, 1)]
        for _ in range(2):
            self.dealer.hit(self.deck)
            for p in self.players:
                p.hit(self.deck)

class DVDGame(Game):
    def __init__(self):
        self.deck = Deck()
        self.dealer = Dealer(IDENTITY_DEALER, 0)
        self.players = [Dealer(IDENTITY_PLAYER, 1)]
        for _ in range(2):
            self.dealer.hit(self.deck)
            for p in self.players:
                p.hit(self.deck)


if __name__ == "__main__":
    n = 5000
    c = 0
    for i in range(n):
        game = TestGame()
        ret = game.run()
        if ret == RESULT_PLAYER_WIN:
            c += 1
    print('Q-Agent')
    print(c / n)

    c = 0
    for i in range(n):
        game = RandomGame()
        ret = game.run()
        if ret == RESULT_PLAYER_WIN:
            c += 1
    print('Random Agent')
    print(c / n)

    c = 0
    for i in range(n):
        game = DVDGame()
        ret = game.run()
        if ret == RESULT_PLAYER_WIN:
            c += 1
    print('Dealer Policy Agent')
    print(c / n)

