import importlib
import sys


othello_ai = importlib.import_module("othello-space-testing")

def main(argv):
    print(int(argv[0]))
    othello_ai.playGame(int(argv[0]), 0)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[1:])
    else:
        main(["1"])
