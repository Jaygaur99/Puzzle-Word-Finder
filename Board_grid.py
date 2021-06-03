from random import choice, randint
STRINGS = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
ORIENTATIONS = ['updown', 'leftright', 'diagonalup', 'diagonaldown']


class BoardGrid:
    """
    A class that basically represents the board of the puzzle.
    """
    def __init__(self, grid_size, words):
        self.grid_size = grid_size
        # Creating a basic _ grid of size 'grid_size'
        self.grid = [['_' for _ in range(self.grid_size)] for _ in range(grid_size)]
        # method to create the grid
        self.populate_grid(words)

    def populate_grid(self, words):
        """
        Creates the grid and puts the words in it.
        :param words: words -> list
        """
        for word in words:
            word_len = len(word)
            placed = False
            while not placed:
                # making a choice which orientation we want for the particular word
                orientation = choice(ORIENTATIONS)
                if orientation == 'leftright':
                    step_x = 1
                    step_y = 0
                if orientation == 'updown':
                    step_x = 0
                    step_y = 1
                if orientation == 'diagonalup':
                    step_x = 1
                    step_y = 1
                if orientation == 'diagonaldown':
                    step_x = 1
                    step_y = -1

                # Starting position of x and y
                x_position = randint(0, self.grid_size-1)
                y_position = randint(0, self.grid_size-1)

                # Ending position of x and y
                ending_x = x_position + word_len * step_x
                ending_y = y_position + word_len * step_y

                # Checking if the starting or ending is out of bound or not
                if ending_x < 0 or ending_x >= self.grid_size or ending_y < 0 or ending_y >= self.grid_size:
                    continue

                # Keeping track that if a letter is placed or not
                failed = False
                for i in range(word_len):
                    character = word[i]

                    new_position_x = x_position + i * step_x
                    new_position_y = y_position + i * step_y
                    character_at_new_position = self.grid[new_position_x][new_position_y]
                    # Checking if the character is '_' or not
                    if character_at_new_position != '_':
                        # If two character are equal the continue. Like in case of 'Green' and 'Grey', 'e' matches in
                        # both otherwise break because there is a difference word already over there so start over
                        if character_at_new_position == character:
                            continue
                        else:
                            failed = True
                            break
                if failed:
                    continue
                else:
                    # If everything okay then put the word in that position
                    for i in range(word_len):
                        character = word[i]

                        new_position_x = x_position + i * step_x
                        new_position_y = y_position + i * step_y

                        self.grid[new_position_x][new_position_y] = character
                    placed = True
        # Fill the remaining '_' with a random letter
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                if self.grid[x][y] == '_':
                    self.grid[x][y] = choice(STRINGS)

    def print_grid(self):
        """
        A method to print the grid
        """
        print()
        for i in range(self.grid_size):
            print('\t' * 4 + '\t'.join(self.grid[i]))
