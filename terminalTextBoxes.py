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
            "black"     : 1,
            "blue"      : 2,
            "green"     : 3,
            "cyan"      : 4,
            "red"       : 5,
            "magenta"   : 6,
            "yellow"    : 7,
            "white"     : 8
        }
        for color, value in self.COLORS.items():
            curses.init_pair(value, value - 1, -1)

        self.TEXT_ATTR = {
            "AltCharset"    : curses.A_ALTCHARSET,
            "Blink"         : curses.A_BLINK,
            "Bold"          : curses.A_BOLD,
            "Dim"           : curses.A_DIM,
            "Invis"         : curses.A_INVIS,
            "Italic"        : curses.A_ITALIC,
            "Normal"        : curses.A_NORMAL,
            "Protect"       : curses.A_PROTECT,
            "Reverse"       : curses.A_REVERSE,
            "Standout"      : curses.A_STANDOUT,
            "Underline"     : curses.A_UNDERLINE,
            "Horizontal"    : curses.A_HORIZONTAL,
            "Left"          : curses.A_LEFT,
            "Low"           : curses.A_LOW,
            "Right"         : curses.A_RIGHT,
            "Top"           : curses.A_TOP,
            "Vertical"      : curses.A_VERTICAL,
            "Chartext"      : curses.A_CHARTEXT
        }

        self.FRAME_CHAR = {
            "vertical"          : "║",
            "verticalLeft"      : "╣",
            "verticalRight"     : "╠",
            "horizontal"        : "═",
            "horizontalUp"      : "╩",
            "horizontalDown"    : "╦",
            "leftUp"            : "╝",
            "leftDown"          : "╗",
            "rightUp"           : "╚",
            "rightDown"         : "╔",
            "cross"             : "╬"
        }
        self.FRAME_CHAR_LEN = 1
        self.INPUT_PROMPT = "> "
        self.INPUT_PROMPT_LEN = len(self.INPUT_PROMPT)

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



        # NEW GENERIC
        self.SPLIT = {
            "Vertical"      : 0,
            "Horizontal"    : 1
        }

        self.H_ORIENT = {
            "Left"          : 0,
            "Right"         : 1
        }
        self.V_ORIENT = {
            "Up"            : 0,
            "Down"          : 1
        }

        self.BOX_MIN_HEIGHT = 1 + self.FRAME_CHAR_LEN * 2
        self.BOX_MIN_WIDTH = 1 + self.FRAME_CHAR_LEN * 2

        self.box = dict()
        self.boxOrder = []
        self.debug = True
        self.debugShow = {
            "name" : 0,
            "size" : 1
        }
        self.debugShowType = 1


    #def createTextBox(self, name, fixedHeight = None, fixedWidth = None, split = 0, orientation = 2):
    def createTextBox(self, name, width = None, height = None, pos = None, hOrient = 0, vOrient = 0,
                      visable = True, wTextIndent = 0, hTextIndent = 0):
        """
            Box properties:
                name                        - name of the textbox.
                width                       - None if not fixed width (becomes textWidth).      Default: None
                height                      - None if not fixed height (becomes textHeight).    Default: None
                pos                         - Position between already existing boxes.
                hOrient                     - Horizontal orientation of the box.                Default: 0 (Up)
                vOrient                     - Vertical orientation of the box.                  Default: 0 (Left)
                visable                     - If True the box is visable else it's not.         Default True
                wTextIndent                 - Width indentation for text.                       Default: 0
                hTextIndent                 - Height indentation for text.                      Default: 0

                boxWidth                    - The width of the box (frame included).
                boxHeight                   - The height of the box (frame included).
                textWidth                   - The width of the box (frame excluded).
                textHeight                  - The height of the box (fram excluded).

                FIX:
                textWidthStartPos
                textHeightStartPos
                textWidthEndPos
                textHeightEndPos
        """
        name = str(name)
        if name in self.box:
            raise Exception(f"TextBox {name} already exists.")

        self.box[name] = dict()

        if width != None and not isinstance(width, int):
            raise Exception("width is not of integer type.")
        self.box[name]["fixedWidth"] = width
        if height != None and not isinstance(height, int):
            raise Exception("height is not of integer type.")
        self.box[name]["fixedHeight"] = height

        if not isinstance(hOrient, int) or hOrient not in self.H_ORIENT.values():
            raise Exception("hOrient is not of integer type or not within acceptable range.")
        self.box[name]["hOrient"] = hOrient

        if not isinstance(vOrient, int) or vOrient not in self.V_ORIENT.values():
            raise Exception("vOrient is not of integer type or not within acceptable range.")
        self.box[name]["vOrient"] = vOrient

        if pos != None:
            if not isinstance(pos, int):
                raise Exception("pos is not of integer type")
            self.boxOrder.insert(pos, name)
            # TODO: modify vOrient by looking at elements on both sides
        elif hOrient == self.H_ORIENT["Left"]:
            self.boxOrder.insert(0, name)
        elif hOrient == self.H_ORIENT["Right"]:
            self.boxOrder.append(name)
        else:
            self.boxOrder.append(name)
        self.box = {key : self.box[key] for key in self.boxOrder} # Sort dict according to boxOrder

        if visable != True and visable != False:
            raise Exception("visable not a boolean.")
        self.box[name]["visable"] = visable

        if  not isinstance(wTextIndent, int):
            raise Exception("wTextIndent is not of integer type.")
        self.box[name]["wTextIndent"] = wTextIndent
        if not isinstance(hTextIndent, int):
            raise Exception("hTextIndent is not of integer type.")
        self.box[name]["hTextIndent"] = hTextIndent







    def update_vars(self):
        """ Update terminal variables such as box sizes. """
        self.hTerminal, self.wTerminal = self.screen.getmaxyx() # Get the terminal size

        nbrOfBoxes = len(self.box)  # Total amount of current boxes
        nbrOfWUnfixedBoxes = 0      # Number of boxes that does not have fixed width
        nbrOfWFixedBoxes = 0        # Number of boxes that does have fixed width
        wForFixed = 0               # Width of all fixed width boxes together
        for name, attr in self.box.items():
            if attr["fixedWidth"] == None:
                nbrOfWUnfixedBoxes = nbrOfWUnfixedBoxes + 1
            else:
                nbrOfWFixedBoxes = nbrOfWFixedBoxes + 1
                wForFixed = wForFixed + attr["fixedWidth"]

        wForUnfixed = 0             # Width of all unfixed width boxes in total
        wForUnused = 0              # Remaining unused width
        if nbrOfWUnfixedBoxes > 0 and nbrOfWFixedBoxes > 0:     # Fixed and Unfixed boxes
            wForUnused = 0
            wForUnfixed = self.wTerminal - wForFixed
        elif nbrOfWUnfixedBoxes > 0 and nbrOfWFixedBoxes == 0:  # Unfixed boxes
            wForUnused = 0
            wForUnfixed = self.wTerminal
        elif nbrOfWUnfixedBoxes == 0 and nbrOfWFixedBoxes > 0:  # Fixed boxes
            wForUnused = self.wTerminal - wForFixed
            wForUnfixed = 0

        # Remaining width that is uneven between the none fixed width boxes.
        # This will be distributed between the wForUnfixed boxes till remainingUnevenWidth == 0
        remainingUnevenWidth = wForUnfixed % (nbrOfWUnfixedBoxes if nbrOfWUnfixedBoxes > 0 else 1)

        wIndex = 0
        prevVerticalOrientation = None
        for name, attr in self.box.items():
            attr["boxHeight"] = self.hTerminal - (self.INPUT_BOX_HEIGHT + self.FRAME_CHAR_LEN)

            if attr["fixedWidth"] == None:
                attr["boxWidth"] = (wForUnfixed // nbrOfWUnfixedBoxes) + (1 if remainingUnevenWidth > 0 else 0)
                remainingUnevenWidth = (remainingUnevenWidth - 1) if remainingUnevenWidth > 0 else 0
            else:
                attr["boxWidth"] = attr["fixedWidth"]# + (self.FRAME_CHAR_LEN * 2)

            #attr["textHeight"] = attr["boxHeight"] - (self.FRAME_CHAR_LEN * 2) - (2 if self.debug else 0)
            #attr["textWidth"] = attr["boxWidth"] - (self.FRAME_CHAR_LEN * 2)

            if attr["hOrient"] == self.H_ORIENT["Right"] and attr["fixedWidth"] != None:
                wIndex = wIndex + wForUnused

            attr["topLeft"] = {"x" : wIndex, "y" : 0}
            attr["bottomRight"] = {"x" : wIndex + attr["boxWidth"] - 1, "y" : attr["boxHeight"] - 1}
            wIndex = wIndex + attr["boxWidth"]

        edgeConditions = []
        edgeConditions.append(self.hTerminal >= (self.BOX_MIN_HEIGHT + self.INPUT_BOX_HEIGHT + 1))
        edgeConditions.append(self.wTerminal >= (self.BOX_MIN_WIDTH * nbrOfBoxes))

        self.updateConditionsSatisfied = all(condition == True for condition in edgeConditions)

        self.inputBoxLineWidth = self.wTerminal - (len(self.INPUT_PROMPT) + 1)
        #self.infoBoxStartPos = self.textBoxWidth + 1






    def update_box_frames(self):
        """  """
        for name, attr in self.box.items():
            if attr["visable"] == False:
                continue

            boxTLX = attr["topLeft"]["x"]
            boxTLY = attr["topLeft"]["y"]
            boxBRX = attr["bottomRight"]["x"]
            boxBRY = attr["bottomRight"]["y"]
            for row in range(self.hTerminal):
                for column in range(self.wTerminal):
                    # DEBUG BOX ON THE BOTTOM OF EVERY BOX
                    if (boxBRY - 2) == row and boxTLX == column and self.debug:
                        self.screen.addstr(row, column, self.FRAME_CHAR["verticalRight"])
                    elif (boxBRY - 2) == row and boxBRX == column and self.debug:
                        self.screen.addstr(row, column, self.FRAME_CHAR["verticalLeft"])
                    elif (boxBRY - 2) == row and boxTLX < column and boxBRX > column and self.debug:
                        self.screen.addstr(row, column, self.FRAME_CHAR["horizontal"])

                    # NORMAL BOX FRAME
                    elif boxTLY == row and boxTLX == column:
                        self.screen.addstr(row, column, self.FRAME_CHAR["rightDown"])
                    elif boxTLY == row and boxBRX == column:
                        self.screen.addstr(row, column, self.FRAME_CHAR["leftDown"])
                    elif boxBRY == row and boxTLX == column:
                        self.screen.addstr(row, column, self.FRAME_CHAR["rightUp"])
                    elif boxBRY == row and boxBRX == column:
                        self.screen.addstr(row, column, self.FRAME_CHAR["leftUp"])
                    elif (boxTLY == row or boxBRY == row) and boxTLX < column and boxBRX > column:
                        self.screen.addstr(row, column, self.FRAME_CHAR["horizontal"])
                    elif boxTLY < row and boxBRY > row and (boxTLX == column or boxBRX == column):
                        self.screen.addstr(row, column, self.FRAME_CHAR["vertical"])

            if self.debug:
                if self.debugShowType == 0:
                    #self.screen.addstr(boxBRY - 1, boxTLX + 1, name[:attr["textWidth"]])
                    self.screen.addstr(boxBRY - 1, boxTLX + 1, name[:attr["boxWidth"]])
                elif self.debugShowType == 1:
                    #size = f'w = {attr["textWidth"]}, h = {attr["textHeight"]}'
                    #self.screen.addstr(boxBRY - 1, boxTLX + 1, size[:attr["textWidth"]])
                    size = f'w = {attr["boxWidth"]}, h = {attr["boxHeight"]}'
                    self.screen.addstr(boxBRY - 1, boxTLX + 1, size[:attr["boxWidth"]])

        self.screen.addstr(self.hTerminal - 1 - self.INPUT_BOX_HEIGHT, 0, \
            self.wTerminal * self.FRAME_CHAR["horizontal"])


    def run(self):
        """ The main function call. """
        #self.createTextBox("HejsanHejsanHejsanHejsanHejsan")
        #self.createTextBox("Hejsan1", 20, visable=False)
        #self.createTextBox("123456789012345678901234567890", 10, verticalOrientation=self.VERTICAL_ORIENTATION["Left"])
        #self.createTextBox("Hejsan4", 22, hOrient=self.H_ORIENT["Right"])

        self.createTextBox("Hejsan1", hOrient=self.H_ORIENT["Left"], visable=False)
        self.createTextBox("Hejsan2", 20, hOrient=self.H_ORIENT["Left"])
        self.createTextBox("Hejsan3", 20, hOrient=self.H_ORIENT["Right"])
        self.createTextBox("Hejsan4", hOrient=self.H_ORIENT["Right"], visable=False)
        self.createTextBox("Hejsan5", 20, hOrient=self.H_ORIENT["Right"])

        #self.createTextBox("Hejsan5")
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
        self.update_vars()
        if self.updateConditionsSatisfied:
            # Update text box lines format
            self.update_text_box_lines_format()
            # Clear the screen
            self.screen.clear()
            # Update separation characters
            #self.update_separation_characters()
            # Update all boxes
            self.update_input_box()
            self.update_box_frames()
            #self.update_info_box()
            #self.update_text_box()
            # Update the visual cursor
            self.update_visual_cursor()
        self.screen.refresh()


    def update_terminal_variables(self):
        """ Update terminal variables such as box sizes. """
        self.terminalHeight, self.terminalWidth = self.screen.getmaxyx()
        self.inputBoxHeight = self.INPUT_BOX_HEIGHT
        self.inputBoxWidth = self.terminalWidth
        self.infoBoxHeight = self.terminalHeight - (self.inputBoxHeight + self.FRAME_CHAR_LEN)
        self.infoBoxWidth = self.INFO_BOX_WIDTH
        self.textBoxHeight = self.infoBoxHeight
        self.textBoxWidth = self.terminalWidth - (self.INFO_BOX_WIDTH + self.FRAME_CHAR_LEN)

        # Edge conditions
        self.edgeConditions = [
            self.inputBoxHeight >= self.INPUT_BOX_MIN_HEIGHT,
            self.infoBoxHeight >= self.INFO_BOX_MIN_HEIGHT,
            self.infoBoxWidth >= self.INFO_BOX_MIN_WIDTH,
            self.textBoxHeight >= self.TEXT_BOX_MIN_HEIGHT,
            self.textBoxWidth >= self.TEXT_BOX_MIN_WIDTH
        ]
        self.updateConditionsSatisfied = all(condition == True for condition in self.edgeConditions)

        self.inputBoxLineWidth = self.terminalWidth - (len(self.INPUT_PROMPT) + 1)
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
                    self.screen.addstr(row, column, self.FRAME_CHAR["vertical"])
                elif row == horizontalLine and column != self.textBoxWidth:
                    self.screen.addstr(row, column, self.FRAME_CHAR["horizontal"])
                elif row == horizontalLine and column == self.textBoxWidth:
                    self.screen.addstr(row, column, self.FRAME_CHAR["horizontalUp"])


    def update_input_box(self):
        """ Update the input box. """
        self.inputBoxVLeftPos = self.inputBoxCursorPos - self.inputBoxVCursorPos
        self.inputBoxVRightPos = self.inputBoxVLeftPos + self.inputBoxLineWidth

        displayedString = ""
        if len(self.inputBoxString) >= self.inputBoxLineWidth:
            displayedString = self.inputBoxString[self.inputBoxVLeftPos:self.inputBoxVRightPos]
        else:
            displayedString = self.inputBoxString
        self.screen.addstr(self.terminalHeight - self.INPUT_BOX_HEIGHT, 0, self.INPUT_PROMPT + displayedString)


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
            len(self.INPUT_PROMPT))



if __name__ == "__main__":
    obj = TerminalTextBoxes()
    obj.run()


# CALLBACK SOLUTION

#def callback(sum):
#    print("Sum = {}".format(sum))
#
#def main(a, b, _callback = None):
#    print("adding {} + {}".format(a, b))
#    if _callback:
#        _callback(a+b)
#
#main(1, 2, callback)
