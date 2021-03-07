#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import curses
import time
import threading

from textwrap import wrap


class TerminalTextBoxes():
    """  """
    def __init__(self):
        """ Init. """
        # Terminal window initialization
        self.screen = curses.initscr()
        self.screen.keypad(True)
        curses.noecho()
        curses.start_color()
        curses.use_default_colors()

        # Colors initialization
        self.COLORS = {
            "black" : 1,
            "blue" : 2,
            "green" : 3,
            "cyan" : 4,
            "red" : 5,
            "magenta" : 6,
            "yellow" : 7,
            "white" : 8,
        }
        for color, value in self.COLORS.items():
            curses.init_pair(value, value - 1, -1)

        self.MESSAGE_ATTRIBUTE = {
            "AltCharset" : curses.A_ALTCHARSET,
            "Blink" : curses.A_BLINK,
            "Bold" : curses.A_BOLD,
            "Dim" : curses.A_DIM,
            "Invis" : curses.A_INVIS,
            "Italic" : curses.A_ITALIC,
            "Normal" : curses.A_NORMAL,
            "Protect" : curses.A_PROTECT,
            "Reverse" : curses.A_REVERSE,
            "Standout" : curses.A_STANDOUT,
            "Underline" : curses.A_UNDERLINE,
            "Horizontal" : curses.A_HORIZONTAL,
            "Left" : curses.A_LEFT,
            "Low" : curses.A_LOW,
            "Right" : curses.A_RIGHT,
            "Top" : curses.A_TOP,
            "Vertical" : curses.A_VERTICAL,
            "Chartext" : curses.A_CHARTEXT
        }

        self.SEPARATOR_LENGTH = 1
        self.SEPARATOR_CHARACTER = {
            "vertical"          : "║",
            "horizontal"        : "═",
            "horizontalUp"      : "╩",
            "horizontalDown"    : "╦",
            "verticalLeft"      : "╣",
            "verticalRight"     : "╠",
            "cross"             : "╬"
        }
        self.INPUT_CHARACTER = "> "

        # These values determine the constant size of the input box and info box
        self.INPUT_BOX_HEIGHT = 1
        self.INFO_BOX_WIDTH = 20

        # Edge values (These should really remain the way they are, otherwise it'll be very hard to read the boxes)
        self.INPUT_BOX_MIN_HEIGHT = 1
        self.INFO_BOX_MIN_HEIGHT = 10
        self.INFO_BOX_MIN_WIDTH = 20
        self.TEXT_BOX_MIN_HEIGHT = 10
        self.TEXT_BOX_MIN_WIDTH = 20

        self.update_terminal_variables()

        self.inputBoxString = ""
        self.inputBoxCursorPos = 0
        self.inputBoxVCursorPos = 0
        self.inputBoxVLeftPos = 0
        self.inputBoxVRightPos = 0

        self.infoBoxLines = []

        self.textBoxMessages = [] # A single list item is one message
        self.textBoxLines = [] # A single list item is one formatted line
        self.textBoxScrollIndex = 0


    def run(self):
        """ The main function call. """
        self.update()

        event = threading.Event()
        thread = threading.Thread(target=self.__key_handler, args=(event,))
        thread.start()


    def __key_handler(self, event):
        """ Handler of key presses. """
        while True:
            char = self.screen.get_wch()

            if char == "\x1b":                  # <ESC> KEY (Exit)
                break

            elif char == 259:                   # <ARROW-UP> KEY (Scroll up)
                if len(self.textBoxLines) + self.textBoxScrollIndex > self.textBoxHeight:
                    self.textBoxScrollIndex -= 1

            elif char == 258:                   # <ARROW-DOWN> KEY (Scroll down)
                if self.textBoxScrollIndex != 0:
                    self.textBoxScrollIndex += 1

            elif char == 260:                   # <ARROW-LEFT> KEY (Scroll left)
                if self.inputBoxVCursorPos != 0:
                    self.inputBoxVCursorPos -= 1
                if self.inputBoxCursorPos != 0:
                    self.inputBoxCursorPos -= 1

            elif char == 261:                   # <ARROW-RIGHT> KEY (Scroll right)
                if self.inputBoxVCursorPos < len(self.inputBoxString) and \
                   self.inputBoxVCursorPos != self.inputBoxLineWidth:
                    self.inputBoxVCursorPos += 1
                if self.inputBoxCursorPos < len(self.inputBoxString):
                    self.inputBoxCursorPos += 1

            elif char == "\x00":                # WINDOWS KEY
                pass

            elif char == curses.KEY_RESIZE:     # RESIZE EVENT
                self.inputBoxCursorPos = 0
                self.inputBoxVCursorPos = 0

            elif char == 262:                   # HOME KEY
                self.inputBoxVCursorPos = 0
                self.inputBoxCursorPos = 0

            elif char == 358 or char == 360:    # END KEY
                if len(self.inputBoxString) >= self.inputBoxLineWidth:
                    self.inputBoxVCursorPos = self.inputBoxLineWidth
                else:
                    self.inputBoxVCursorPos = len(self.inputBoxString)
                self.inputBoxCursorPos = len(self.inputBoxString)

            elif char == "\n": # <ENTER>
                if self.inputBoxString != "":
                    self.textBoxMessages.append([self.inputBoxString,
                        curses.color_pair(self.COLORS["white"]) | curses.A_STANDOUT])
                self.inputBoxString = ""
                self.inputBoxCursorPos = 0
                self.inputBoxVCursorPos = 0
                self.textBoxScrollIndex = 0

            elif char == 330:                   # DELETE KEY
                self.inputBoxString = self.inputBoxString[:self.inputBoxCursorPos] + \
                    self.inputBoxString[self.inputBoxCursorPos:][1:]

                if len(self.inputBoxString) >= self.inputBoxLineWidth:
                    if len(self.inputBoxString) == (self.inputBoxVRightPos - 1) and \
                       self.inputBoxVCursorPos != self.inputBoxLineWidth:
                        self.inputBoxVCursorPos += 1

            elif char == "\x08" or char == 263: # BACKSPACE KEY
                self.inputBoxString = self.inputBoxString[:self.inputBoxCursorPos][:-1] + \
                    self.inputBoxString[self.inputBoxCursorPos:]

                if self.inputBoxVCursorPos != 0 and len(self.inputBoxString) <= self.inputBoxLineWidth and \
                   self.inputBoxVLeftPos == 0:
                    self.inputBoxVCursorPos -= 1
                elif self.inputBoxVCursorPos != 0 and len(self.inputBoxString) >= self.inputBoxLineWidth and \
                     self.inputBoxVLeftPos == 0:
                    self.inputBoxVCursorPos -= 1
                if self.inputBoxCursorPos != 0:
                    self.inputBoxCursorPos -= 1

            elif char == 339:                   # PAGE UP
                self.textBoxScrollIndex -= self.textBoxHeight
                if self.textBoxScrollIndex < -(len(self.textBoxLines) - self.textBoxHeight):
                    self.textBoxScrollIndex = -(len(self.textBoxLines) - self.textBoxHeight)

            elif char == 338:                   # PAGE DOWN
                self.textBoxScrollIndex += self.textBoxHeight
                if self.textBoxScrollIndex > 0:
                    self.textBoxScrollIndex = 0

            #elif char == "\x16":                # CTRL + V (paste)
            #    try:
            #        copy = self.get_clipboard()
            #        if copy != None and copy != False:
            #            self.inputString = self.inputString[:self.cursorPos] + copy + self.inputString[self.cursorPos:]
            #            self.cursorPos += len(copy)
            #            if (self.visualCursorPos + len(copy)) >= self.lineWidth:
            #                self.visualCursorPos = self.lineWidth
            #            else:
            #                self.visualCursorPos += len(copy)

            #    except Exception as e:
            #        pass

            else: # Append characters to self.inputBoxString
                self.inputBoxString =   self.inputBoxString[:self.inputBoxCursorPos] + str(char) + \
                    self.inputBoxString[self.inputBoxCursorPos:]
                if self.inputBoxVCursorPos != self.inputBoxLineWidth:
                    self.inputBoxVCursorPos += 1
                self.inputBoxCursorPos += 1

            self.update()

        curses.endwin() # Close curses terminal


    def update(self):
        """ Updates all. """
        self.update_terminal_variables()
        if self.updateConditionsSatisfied:
            # Update text box lines format
            self.update_text_box_lines_format()
            # Clear the screen
            self.screen.clear()
            # Update separation characters
            self.update_separation_characters()
            # Update all boxes
            self.update_input_box()
            self.update_info_box()
            self.update_text_box()
            # Update the visual cursor
            self.update_visual_cursor()
        self.screen.refresh()


    def update_terminal_variables(self):
        """ Update terminal variables such as box sizes. """
        self.terminalHeight, self.terminalWidth = self.screen.getmaxyx()
        self.inputBoxHeight = self.INPUT_BOX_HEIGHT
        self.inputBoxWidth = self.terminalWidth
        self.infoBoxHeight = self.terminalHeight - (self.inputBoxHeight + self.SEPARATOR_LENGTH)
        self.infoBoxWidth = self.INFO_BOX_WIDTH
        self.textBoxHeight = self.infoBoxHeight
        self.textBoxWidth = self.terminalWidth - (self.INFO_BOX_WIDTH + self.SEPARATOR_LENGTH)

        # Edge conditions
        self.edgeConditions = [
            self.inputBoxHeight >= self.INPUT_BOX_MIN_HEIGHT,
            self.infoBoxHeight >= self.INFO_BOX_MIN_HEIGHT,
            self.infoBoxWidth >= self.INFO_BOX_MIN_WIDTH,
            self.textBoxHeight >= self.TEXT_BOX_MIN_HEIGHT,
            self.textBoxWidth >= self.TEXT_BOX_MIN_WIDTH
        ]
        self.updateConditionsSatisfied = all(condition == True for condition in self.edgeConditions)

        self.inputBoxLineWidth = self.terminalWidth - (len(self.INPUT_CHARACTER) + 1)
        self.infoBoxStartPos = self.textBoxWidth + 1


    def update_text_box_lines_format(self):
        """ Update the text box lines format """
        self.textBoxLines = []
        for message, color in self.textBoxMessages:
            lines = wrap(message, self.textBoxWidth)
            for line in lines:
                self.textBoxLines.append([line, color])


    def update_separation_characters(self):
        """ Update the separation characters that split up the different boxes. """
        horizontalLine = self.terminalHeight - self.INPUT_BOX_HEIGHT - 1
        for row in range(self.terminalHeight):
            for column in range(self.terminalWidth):
                if row < horizontalLine and column == self.textBoxWidth:
                    self.screen.addstr(row, column, self.SEPARATOR_CHARACTER["vertical"])
                elif row == horizontalLine and column != self.textBoxWidth:
                    self.screen.addstr(row, column, self.SEPARATOR_CHARACTER["horizontal"])
                elif row == horizontalLine and column == self.textBoxWidth:
                    self.screen.addstr(row, column, self.SEPARATOR_CHARACTER["horizontalUp"])


    def update_input_box(self):
        """ Update the input box. """
        self.inputBoxVLeftPos = self.inputBoxCursorPos - self.inputBoxVCursorPos
        self.inputBoxVRightPos = self.inputBoxVLeftPos + self.inputBoxLineWidth

        displayedString = ""
        if len(self.inputBoxString) >= self.inputBoxLineWidth:
            displayedString = self.inputBoxString[self.inputBoxVLeftPos:self.inputBoxVRightPos]
        else:
            displayedString = self.inputBoxString
        self.screen.addstr(self.terminalHeight - self.INPUT_BOX_HEIGHT, 0, self.INPUT_CHARACTER + displayedString)


    def update_info_box(self):
        """ Update the info box. """
        for i, item in enumerate(self.infoBoxLines):
            if i == self.infoBoxHeight:
                break
            self.screen.addstr(i, self.infoBoxStartPos, item[:self.infoBoxWidth])


    def update_text_box(self):
        """ Update the text box. """
        displayedText = []
        if len(self.textBoxLines) >= self.textBoxHeight:
            displayedText = self.textBoxLines[-self.textBoxHeight + self.textBoxScrollIndex:][:self.textBoxHeight]
        else:
            displayedText = self.textBoxLines

        for i, line in enumerate(displayedText):
            self.screen.addstr(i, 0, line[0], line[1])


    def update_visual_cursor(self):
        """ Update the visual cursor in the input box. """
        self.screen.move(self.terminalHeight - self.INPUT_BOX_HEIGHT, self.inputBoxVCursorPos + \
            len(self.INPUT_CHARACTER))



if __name__ == "__main__":
    obj = TerminalTextBoxes()
    obj.run()
