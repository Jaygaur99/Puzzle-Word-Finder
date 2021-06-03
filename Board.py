import tkinter as tk
import tkinter.font as tkFont
from os import listdir, getcwd
from random import choice
from functools import partial
from Board_grid import BoardGrid


class Board:
    """
    The Board class is the GUI of the Board_grid class. The grid is displayed
    on the left side of the app as a grid of buttons that capture which words
    have been found. The right side of the GUI features a menu allowing the user
    to see the solutions, reshuffle the board, or create a new board with
    completely new words (randomly chosen from file_name). The user can also
    export the current board as an html file containing the board in html <table>,
    LaTeX and String form. This file also contains the solution.
    """
    def __init__(self, file, words=None, grid_size=10, color='#D6ED17'):
        """
        Initialize the Board GUI
        :param words: words -> List (A list of words selected from the file or given by the user)
        :param grid_size: grid_size -> int (Size of the grid)
        :param color: color -> str (Colour code of the bg of user choice)
        :param file: file -> str (File name of the file from where data is read)
        """
        root = tk.Tk()
        root.title('Word Search Puzzle')
        root.resizable(width=False, height=False)

        self._word_grid = tk.Frame(root)
        self._word_list = tk.Frame(root)
        self._menu = tk.Frame(root)

        self._solution_shown = False
        self._size = grid_size
        self._color = color
        self._words = words

        # If file_name is not present in the current directory, the
        # New Words button will be disabled.
        new_word_button = tk.DISABLED
        if file in listdir(getcwd()):
            new_word_button = tk.NORMAL
            with open(file) as f:
                self._words_txt = filter(None, f.read().split('\n'))
                self._words_txt = list(filter(lambda x: len(x) < grid_size - 3, self._words_txt))
        elif self._words is None:
            raise FileNotFoundError(f'''{file} not present in the current directory. {file}
                                    must contain words separated by newline (\\n) characters.''')

        # Buttons that have been pushed
        self._pushed = set()

        # Check if 'words' is None and if it is None then provide words
        if self._words is None:
            self._choose_random_words()
        else:
            self._words = list(set(map(str.upper, self._words)))

        # Create empty Size*Size grid of buttons
        self._buttons = []
        for i in range(self._size):
            row = []
            for j in range(self._size):
                row.append(
                    tk.Button(self._word_grid, padx=5, command=partial(self._pressed, i, j))
                )
                row[-1].grid(row=i, column=j, sticky='ew')
            self._buttons.append(row)

        # Menu button at the top right of the GUI
        # Menu label
        tk.Label(
            self._menu, text='Menu', pady=5, font=tkFont.Font(weight='bold')
        ).grid(row=0, column=0, columnspan=2, sticky='ew')
        # New Word Button
        tk.Button(
            self._menu, text='New Words', padx=1, pady=1,
            state=new_word_button, command=self._select_new
        ).grid(row=1, column=0, sticky='ew')
        # Export button
        self._export_button = tk.Button(
            self._menu, text='Export', padx=1, pady=1, command=self._export
        )
        self._export_button.grid(row=1, column=1, sticky='ew')
        # Solution Button
        tk.Button(
            self._menu, text='Solution', padx=1, pady=1, command=self._solution
        ).grid(row=2, column=0, sticky='ew')
        # Reshuffle button
        tk.Button(
            self._menu, text='Reshuffle', padx=1, pady=1, command=self._reshuffle
        ).grid(row=2, column=1, sticky='ew')

        self._labels = {}
        self._word_search = None
        self._create_labels()
        self._reshuffle()

        self._word_grid.pack(side=tk.LEFT)
        self._menu.pack(side=tk.TOP, pady=self._size)
        self._word_list.pack(side=tk.TOP, padx=40, pady=20)

        tk.mainloop()

    def _choose_random_words(self):
        """
        Chooses 10 new random  words from the file_name file.
        """
        self._words = set()
        for _ in range(10):
            self._words.add(choice(self._words_txt).upper())
        self._words = list(self._words)

    def _create_labels(self):
        """
        Creates/changes the word labels on the right side of the GUI.
        """
        for label in self._labels.values():
            label.destroy()
        self._labels.clear()
        self._labels = {'Words': tk.Label(self._word_list, text='Words', pady=5, font=tkFont.Font)}
        self._labels['Words'].grid(row=2, column=0, columnspan=2)
        for i, word in enumerate(sorted(self._words)):
            self._labels[word] = tk.Label(self._word_list, text=word, anchor='w')
            self._labels[word].grid(row=(i // 2) + (i % 1) + 3, column=i % 2, sticky='W')

    def _pressed(self, row, column):
        """
        Check for the button if it is pressed. Also checks if a certain
        word is found or not and disables it if found.
        :param row: row -> int (Number of row)
        :param column: column -> int (Number of column)
        """
        if self._buttons[row][column].cget('bg') == self._color:
            self._buttons[row][column].configure(bg='SystemButtonFace')
            self._pushed.remove((self._buttons[row][column].cget('text'), row, column))
        else:
            self._buttons[row][column].configure(bg=self._color)
            self._pushed.add((self._buttons[row][column].cget('text'), row, column))

            # Checks if a word is completely found or not.
            for word, coordinates in self._word_search.word_position.items():
                if coordinates & self._pushed == coordinates:
                    for _, r, c in coordinates:
                        self._buttons[r][c].configure(state=tk.DISABLED)
                    self._labels[word].configure(bg=self._color)

    def _reshuffle(self):
        """
        Command for the "Reshuffle" button. Uses the existing words and
        creates a new word search board with the words in new locations.
        """
        self._export_button.configure(text='Export', state=tk.NORMAL)

        if self._solution_shown:
            self._solution_shown = not self._solution_shown
        self._word_search = BoardGrid(self._size, self._words)
        self._pushed.clear()

        for i in range(self._size):
            for j in range(self._size):
                self._buttons[i][j].configure(
                    text=self._word_search.grid[i][j], bg='SystemButtonFace', state=tk.NORMAL
                )
            for label in self._labels.values():
                label.configure(bg="SystemButtonFace")

    def _solution(self):
        """
        Command for the "Solution" button. Toggles the solutions on/off when
        pressed by lighting up the backgrounds of the buttons that contain
        the words in the board.
        """
        if self._solution_shown:
            bg = 'SystemButtonFace'
            state = tk.NORMAL
            self._pushed.clear()
        else:
            bg = self._color
            state = tk.DISABLED

        self._solution_shown = not self._solution_shown
        for word, coordinates in self._word_search.word_position.items():
            # print(word)
            self._labels[word].configure(bg=bg)
            for _, r, c in coordinates:
                #  print(_, r, c)
                self._buttons[r][c].configure(state=state, bg=bg)

    def _select_new(self):
        """
        Command for the "New Words" button. Chooses a new randoms set of
        words from the file_name file and fills up the board with the new
        words and displays it in the GUI.
        """
        self._choose_random_words()
        self._reshuffle()
        self._create_labels()

    def _export(self):
        """
        Command for the "Export" button. Creates an html file containing
        a html table. Includes the solution and the words at the bottom
        of the page.
        """
        self._export_button.configure(state=tk.DISABLED)
        with open('templates/index.html') as template:
            content = template.readlines()
        number = 0
        file_name = 'Exported File/WordSearch.html'
        while file_name in listdir(getcwd()):
            number += 1
            file_name = f'Exported File/WordSearch{number}.html'

        with open(file_name, 'w') as f:
            # Write first few lines from templates
            for i in range(11):
                f.write(content[i])

            # Create HTML Table Version of the Word Search Grid
            f.write('<table align="center">\n')
            for i in range(self._size):
                f.write('\t<tr>\n\t\t')
                for j in range(self._size):
                    f.write(f'<td padding=2em>{self._word_search.grid[i][j]}</td>')
                f.write('\t</tr>\n')
            f.write('</table>\n<br><br>')

            # Add solution to the bottom of the file
            f.write('\n<br><br><h2 align="center">Solution</h2><br><br>\n')
            board = self._word_search.solution
            f.write('<table align="center">\n')
            for i in range(self._size):
                f.write('\t<tr>\n\t\t')
                for j in range(self._size):
                    f.write(f'<td padding=2em>{board[i][j]}</td>')
                f.write('\t</tr>\n')
            f.write('</table>\n<br><br>')

            # Add words used in the Word Search and the size of the board
            f.write('\n<br><br><h2 align="center">Words</h2><br><br>\n')
            f.write(f'''<ul align="center"><li>{'</li><li>'.join(self._words)}</li></ul>\n''')
            f.write(f'\n<br><br><h2 align="center">SIZE: {self._size}x{self._size}</h2><br><br>\n')

            # Write few last lines from templates
            for i in range(11, 14):
                f.write(content[i])
