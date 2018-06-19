from game import *
import random

discount = 0.85
reward = 1
penalty = -1

epsilon = 0.5

class QTable(object):
    def __init__(self):
        self.table = dict()

    def _process_status(self, status):
        player_status = tuple(sorted(status[0]))
        dealer_status = tuple(sorted(status[1]))
        status = tuple([player_status, dealer_status])
        if self.table.get(status) == None:
            self.table[status] = dict()
            self.table[status][MOVE_HIT] = 0
            self.table[status][MOVE_STICK] = 0
        else:
            for m in [MOVE_HIT, MOVE_STICK]:
                if self.table[status].get(m) == None:
                    self.table[status][m] = 0
        return status

    def lookup(self, status, move):
        status = self._process_status(status)    
        return self.table[status][move]
    
    def update(self, status, move, value):
        status = self._process_status(status)
        self.table[status][move] = value

    def show(self):
        for status in self.table:
            if self.table[status][MOVE_HIT] > 2 or self.table[status][MOVE_HIT] < -2:
                print('STATUS', status)
                print('HIT   has reward', self.table[status][MOVE_HIT])
                print('STICK has reward', self.table[status][MOVE_STICK])


table = QTable()


class LearningPlayer(Player):
    def __init__(self, identity, _id):
        super().__init__(identity, _id)
        self.status_move = []

    def move(self, deck, players=[]):
        dealer = [p for p in players if p.identity == IDENTITY_DEALER][0]
        player_status = self._learn_stat(True)
        dealer_status = dealer._learn_stat()
        game_status = tuple([player_status, dealer_status])
        rnd = random.random()
        if rnd > epsilon:
            decision = random.choice([MOVE_HIT, MOVE_STICK])
        else:
            hit_reward = table.lookup(game_status, MOVE_HIT)
            stick_reward = table.lookup(game_status, MOVE_STICK)
            decision = MOVE_HIT if hit_reward > stick_reward else MOVE_STICK
        if decision == MOVE_HIT:
            self.hit(deck)
            self.status_move.append([game_status, MOVE_HIT])
        else:
            self.stick()
            self.status_move.append([game_status, MOVE_STICK])


class LearningGame(Game):
    def __init__(self):
        self.deck = Deck()
        self.dealer = Dealer(IDENTITY_DEALER, 0)
        self.players = [LearningPlayer(IDENTITY_PLAYER, 1)]
        for _ in range(2):
            self.dealer.hit(self.deck)
            for p in self.players:
                p.hit(self.deck)

    def run(self):
        while not self.is_end:
            # Players first run
            for p in self.players:
                while p.status == STATUS_PLAYING:
                    p.move(self.deck, self.all_players)
                    self.check(p)
            if self.is_players_bust:
                break
            # Then dealer run
            while self.dealer.status == STATUS_PLAYING:
                self.dealer.move(self.deck, self.all_players)
                self.check(self.dealer)

        if self.is_dealer_bust:
            p = self.players[0]
            c = len(p.status_move)
            for i in p.status_move:
                c -= 1
                status = i[0]
                move = i[1]
                val = table.lookup(status, move)
                table.update(status, move, val+reward*(discount**c))
        elif self.is_players_bust:
            p = self.players[0]
            c = len(p.status_move)
            for i in p.status_move:
                c -= 1
                status = i[0]
                move = i[1]
                val = table.lookup(status, move)
                table.update(status, move, val+penalty*(discount**c))
        else:
            final = sorted(self.all_players, key=lambda x: x.sum, reverse=True)
            final = [f for f in final if f.status != STATUS_BUST]
            if final[0].sum == final[1].sum:
                return
            if final[0].identity == IDENTITY_DEALER:
                p = self.players[0]
                c = len(p.status_move)
                for i in p.status_move:
                    c -= 1
                    status = i[0]
                    move = i[1]
                    val = table.lookup(status, move)
                    table.update(status, move, val+penalty*(discount**c))
            else:
                p = self.players[0]
                c = len(p.status_move)
                for i in p.status_move:
                    c -= 1
                    status = i[0]
                    move = i[1]
                    val = table.lookup(status, move)
                    table.update(status, move, val+reward*(discount**c))