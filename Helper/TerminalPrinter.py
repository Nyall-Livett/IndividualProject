import os

"""
Used to print message to terminal in a way that is more readable... and pretty
"""

class TerminalPrinter:
    def __init__(self):
        self.pattern = "<*><*>"
        self.green_start = "\033[92m"
        self.red_start   = "\033[31m"
        self.white_start = "\033[39m"
        self.yellow_start = "\033[93m"
        self.color_reset = "\033[0m"

    def __get_colour_code(self, colour):
        """
        Return the colour code for the terminal
        """
        if colour == "red":
            return self.red_start
        elif colour == "green":
            return self.green_start
        elif colour == "yellow":
            return self.yellow_start
        return self.white_start

    def clear_terminal(self):
        """
        Clear the current terminal to minimise noise
        """
        print('\033[2J\033[H', end='')

    def pretty_print(self, text):
        """
        Pretty print text inside a line pattern to indicate the next step of the process
        """    
        print('\n')
        columns, _ = os.get_terminal_size()
        text_length = len(text) + 2  # Adding spaces around the text
        available_space = columns - text_length

        available_space_per_side = max(available_space // 2, 0)
        repeat_count_per_side = available_space_per_side // len(self.pattern)

        left_pattern = self.pattern * repeat_count_per_side
        right_pattern = self.pattern * repeat_count_per_side

        if available_space % 2 != 0:
            right_pattern += self.pattern[:available_space_per_side % len(self.pattern)]

        full_pattern = f"{self.green_start}{left_pattern} {text} {right_pattern}{self.color_reset}"
        print(full_pattern)

    def print_with_color(self, text, colour):
        """
        Print text in a specific colour (green or red)
        """
        full_pattern = f"{self.__get_colour_code(colour)}{text}{self.color_reset}"
        print(full_pattern)
