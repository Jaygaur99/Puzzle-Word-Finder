from random import choice
WORDS_SHOW_PER_LINE = 5


class BoardWords:
    """
    A class to take words from a file.
    """
    def __init__(self, filename):
        """
        Initialize the words.
        :param filename -> str
        """
        handle = open(filename)
        words = handle.readlines()
        handle.close()
        self.words = []
        for _ in range(10):
            w = choice(words)
            self.words.append(w.upper().strip())
            words.remove(w)

    # CLI Based print method
    def print_words(self):
        """
        A method to print the list of words that need to be find
        """
        print("\nWords to find are: ")
        i = 0
        for word in self.words:
            print(word, end='  ')
            i += 1
            if i % WORDS_SHOW_PER_LINE == 0:
                print()
