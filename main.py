from Board_words import BoardWords
from Board_grid import BoardGrid
# Size of Grid we want to play in.
GRID_SIZE = 10


def main():
	# Creating instances of classes
	words = BoardWords('colors.txt')
	grid = BoardGrid(GRID_SIZE, words.words)

	# Calling the required function of the classes
	grid.print_grid()
	words.print_words()


if __name__ == '__main__':
	main()