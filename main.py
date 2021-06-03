from Board import Board
from Board_words import BoardWords
from Board_grid import BoardGrid

# Size of Grid we want to play in.
GRID_SIZE = 20
file = 'colors.txt'


def main():
    # Creating instances of classes
    words = BoardWords(file)
    # grid = BoardGrid(GRID_SIZE, words.words)

    # Calling the required function of the classes
    # grid.print_grid()
    words.print_words()

    # Calling the Board
    board = Board(words.words,GRID_SIZE, '#D6ED17', file)


if __name__ == '__main__':
    main()
