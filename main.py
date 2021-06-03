from Board import Board
from Board_words import BoardWords
# Size of Grid we want to play in.
GRID_SIZE = 20
file = 'words.txt'


def main():
    words = BoardWords(file)
    Board(file, words.words, GRID_SIZE, '#D6ED17')


if __name__ == '__main__':
    main()
