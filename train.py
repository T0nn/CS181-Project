import learn
import pickle

if __name__ == "__main__":
    for i in range(1000000):
        print(i)
        game = learn.LearningGame()
        game.run()
    learn.table.show()
    with open('table', 'wb') as f:
        pickle.dump(learn.table, f)