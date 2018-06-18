from learn import *
import pickle

table = None
with open('teble2', 'rb') as f:
    table = pickle.load(f)

class QPolicyAgent(Player):
    pass

class TestGame(Game):
    pass
