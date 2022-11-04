# Class of the game
class LearningToSpell():
    def __init__(self):
        # Colors
        self.black = "#000000"
        self.green = "#00ff00"
        self.red = "#ff0000"

        # Game variables
        self.word = '' # Word to be spelled
        self.current_letter = 0 # Current letter to be spelled
        self.colors = [] # Colors of the letters
        self.winner = False # Winner flag
        self.fails = 0 # Number of fails
        
    def set_word(self, word):
        """
        Set the word to be spelled

        Parameters
        ----------
        word : str
            Word to be spelled
        
        Returns
        ----------
        None
        """
        self.word = word.lower() # Set the word
        self.colors = [self.black] * len(word) # Set the colors
        self.current_letter = 0 # Set the current letter
        self.winner = False # Set the winner flag
        self.fails = 0 # Set the number of fails

    def check_letter(self, letter):
        """
        Check if the letter is correct

        Parameters
        ----------
        letter : str
            Letter to be checked

        Returns
        ----------
        tuple (int, str, str)
            Tuple with the index of the current letter, the current letter and 
            the color of the letter
        """
        # Check if the letter is correct
        if letter.lower() == self.word[self.current_letter]:
            # Set the color of the letter to green
            self.colors[self.current_letter] = self.green
            # Check if the letter is the last one
            if self.current_letter < len(self.word) - 1: 
                self.current_letter += 1 # Set the next letter
            else:
                self.winner = True # Set the winner flag
            return (
                self.current_letter, # Index of the current letter
                self.word[self.current_letter], # Current letter
                self.green # Color of the current letter
            )
        # If the letter is incorrect
        else:
            self.fails += 1 # Increment the number of fails
            # Set the color of the letter to red
            self.colors[self.current_letter] = self.red 
            return (
                self.current_letter, # Index of the current letter
                self.word[self.current_letter], # Current letter
                self.red # Color of the current letter
            )

    def get_current_state(self):
        """
        Get the current state of the game

        Parameters
        ----------
        None

        Returns
        ----------
        dict ('word': str, 'colors': list, 'current_letter': int, 'fails': int, 'winner': bool)
            word: Word to be spelled
            colors: Colors of the letters
            current_letter: Current letter to be spelled
            winner: Winner flag
        """
        return {
            'word': self.word, # Word to be spelled
            'colors': self.colors, # Colors of the letters
            'current_letter': self.current_letter, # Current letter to be spelled
            'fails': self.fails, # Number of fails
            'winner': self.winner # Winner flag
        }

    def get_winner(self):
        """
        Get the winner flag

        Parameters
        ----------
        None

        Returns
        ----------
        bool
        """
        return self.winner # Return the winner flag

    def try_word(self, word):
        """
        Try to spell the word in one try (simillar to the game "wordle")

        Parameters
        ----------
        word : str
            Word of the try
        
        Returns
        ----------
        return of the method 'get_current_state()'
        """
        # Check if the word has the same length of the word to be spelled
        if len(word) > len(self.word):
            word = word[:len(self.word)] # Cut the word
        elif len(word) < len(self.word):
            word += ' ' * (len(self.word) - len(word))  # Add spaces to the end 
                                                        # of the word
                                          
        # Define initial variables
        self.current_letter = -1 # Set the current letter
        self.winner = True # Set the winner flag              
        check_word = list(self.word)    # List of the letters of the word to be 
                                        # spelled
        count_letters = {}  # Dictionary with the number of letters of the word 
                            # to be spelled
        
        # Count the number of letters of the word to be spelled
        for letter in check_word:
            if letter not in count_letters:
                count_letters[letter] = 1
            else:
                count_letters[letter] += 1
                
        # Check if the word is correct
        for i, letter in enumerate(word.lower()):
            # Check if the letter is in the correct position
            if letter == self.word[i]:
                self.colors[i] = self.green # Set the color of the letter to green (correct position)
                check_word[i] = -1 # Set the letter as checked
            # If the letter isn't in the correct position
            else:
                self.winner = False # Set the winner flag to False
                # Check if the letter is in the word to be spelled and if that
                # isn't verified yet
                if letter in check_word \
                    and count_letters[letter] > 0:
                    self.colors[i] = self.black # Set the color of the letter to black (incorrect position, but in the word)
                # If the letter isn't in the word to be spelled
                else:
                    self.colors[i] = self.red # Set the color of the letter to red (not in the word)
            # Check if the letter is in the word to be spelled and if that isn't
            # verified yet
            if letter in count_letters:
                count_letters[letter] -= 1 # Decrement the number of letters of the word to be spelled

        # Check if the player has failed
        if not self.winner:
            self.fails += 1 # Increment the number of fails

        return self.get_current_state() # Return the current state of the game