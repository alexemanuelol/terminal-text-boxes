#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import curses
import time
import threading

from textwrap import wrap


TEXT_ATTR = {
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

FRAME_STYLE = {
    "singleLine"    : ["│", "┤", "├", "─", "┴", "┬", "┘", "┐", "└", "┌", "┼"],
    "doubleLine"    : ["║", "╣", "╠", "═", "╩", "╦", "╝", "╗", "╚", "╔", "╬"],
    "hash"          : ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#"],
    "at"            : ["@", "@", "@", "@", "@", "@", "@", "@", "@", "@", "@"],
    "star"          : ["*", "*", "*", "*", "*", "*", "*", "*", "*", "*", "*"],
    "blockFull"     : ["█", "█", "█", "█", "█", "█", "█", "█", "█", "█", "█"],
    "blockVague0"   : ["▓", "▓", "▓", "▓", "▓", "▓", "▓", "▓", "▓", "▓", "▓"],
    "blockVague1"   : ["▒", "▒", "▒", "▒", "▒", "▒", "▒", "▒", "▒", "▒", "▒"],
    "blockVague2"   : ["░", "░", "░", "░", "░", "░", "░", "░", "░", "░", "░"],
    "invisible"     : [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "]
}



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

        # Color variables
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

        # Frame variables
        self.FRAME_SIZE = 1
        self.frame = {
            "vertical"          : FRAME_STYLE["singleLine"][0],
            "verticalLeft"      : FRAME_STYLE["singleLine"][1],
            "verticalRight"     : FRAME_STYLE["singleLine"][2],
            "horizontal"        : FRAME_STYLE["singleLine"][3],
            "horizontalUp"      : FRAME_STYLE["singleLine"][4],
            "horizontalDown"    : FRAME_STYLE["singleLine"][5],
            "leftUp"            : FRAME_STYLE["singleLine"][6],
            "leftDown"          : FRAME_STYLE["singleLine"][7],
            "rightUp"           : FRAME_STYLE["singleLine"][8],
            "rightDown"         : FRAME_STYLE["singleLine"][9],
            "cross"             : FRAME_STYLE["singleLine"][10]
        }

        # Prompt variables
        self.promptSign             = "> "
        self.promptSignSize         = len(self.promptSign)
        self.promptWidth            = None # Will be the same as self.wTerminal
        self.promptHeight           = 1
        self.promptLineWidth        = None # Will be self.wTerminal - (self.promptSignSize + 1)
        self.promptString           = ""
        self.promptCursorPos        = 0
        self.promptVCursorPos       = 0
        self.promptVLeftPos         = 0
        self.promptVRightPos        = 0

        # Box variables
        self.box                    = dict()
        self.boxOrder               = list()

        # Minimum sizes
        self.PROMPT_MIN_WIDTH       = self.promptSignSize + 10
        self.PROMPT_MIN_HEIGHT      = 1
        self.BOX_MIN_WIDTH          = self.FRAME_SIZE * 2
        self.BOX_MIN_HEIGHT         = self.FRAME_SIZE * 2

        # Orientations
        self.H_ORIENT = {
            "Left"          : 0,
            "Right"         : 1
        }
        self.V_ORIENT = {
            "Up"            : 0,
            "Down"          : 1
        }

        # Debug variables
        self.debugBoxPlacement = {
            "Top"           : 0,
            "Bottom"        : 1
        }
        self.debugBoxInfo = {
            "name"          : 0,
            "textSize"      : 1,
            "boxSize"       : 2
        }

        self.debug                  = True
        self.debugBoxPlacementShow  = 0
        self.debugBoxInfoShow       = 2

        self.update()


    def run(self):
        """ The main function call. """
        self.update()

        event = threading.Event()
        thread = threading.Thread(target=self.__key_handler, args=(event,))
        thread.start()


    def update(self):
        """ Updates all. """
        # Used to verify that prompt/box sizes doesn't become smaller than min size.
        self.edgeConditions = list()

        self.hTerminal, self.wTerminal = self.screen.getmaxyx() # Get the terminal size

        # Update the prompt variables (prompt size)
        self.update_prompt_variables(False)

        # Update box variables (box sizes)
        self.update_box_variables(False)

        if self.updateConditionsSatisfied:
            # Update text format by re-wrapping text to match new box sizes
            self.update_text_wrapping()

            # Clear the screen
            self.screen.clear()

            # Update all the boxes frames
            self.update_box_frames()

            # Update prompt
            self.update_prompt()

            # Update all boxes
            self.update_boxes()

            # Update the visual cursor
            self.update_visual_cursor()

        self.screen.refresh()


    def update_prompt_variables(self, updateTerminal=True):
        """ Update terminal variables such as box sizes. """
        if updateTerminal:
            self.hTerminal, self.wTerminal = self.screen.getmaxyx() # Get the terminal size

        self.promptWidth = self.wTerminal
        self.promptLineWidth = self.wTerminal - (self.promptSignSize + 1)

        # Edge conditions
        self.edgeConditions.append(self.wTerminal >= self.PROMPT_MIN_WIDTH)
        self.edgeConditions.append(self.hTerminal >= self.PROMPT_MIN_HEIGHT)

        self.updateConditionsSatisfied = all(condition == True for condition in self.edgeConditions)


    def update_box_variables(self, updateTerminal=True):
        """ Update terminal variables such as box sizes. """
        if updateTerminal:
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
        hIndex = 0
        wForUnusedUsed = False
        hForUnusedUsed = False
        prevVerticalOrientation = None
        for name, attr in self.box.items():
            # Box Width/ Height
            if attr["fixedWidth"] == None:
                attr["boxWidth"] = (wForUnfixed // nbrOfWUnfixedBoxes) + (1 if remainingUnevenWidth > 0 else 0)
                remainingUnevenWidth = (remainingUnevenWidth - 1) if remainingUnevenWidth > 0 else 0
            else:
                attr["boxWidth"] = attr["fixedWidth"]# + (self.FRAME_SIZE * 2)
            if attr["fixedHeight"] == None:
                attr["boxHeight"] = self.hTerminal - (self.promptHeight + self.FRAME_SIZE)
            else:
                attr["boxHeight"] = attr["fixedHeight"]

            # Text Width/ Height
            frameTotalWidth = self.FRAME_SIZE * 2
            attr["textWidth"] = attr["boxWidth"] - frameTotalWidth - (attr["wTextIndent"] * 2)
            frameTotalHeight = (self.FRAME_SIZE * 2) + (2 if self.debug else 0)
            attr["textHeight"] = attr["boxHeight"] - frameTotalHeight - (attr["hTextIndent"] * 2)

            # Box orientation horizontal/ vertical
            if attr["hOrient"] == self.H_ORIENT["Right"] and attr["fixedWidth"] != None and wForUnusedUsed == False:
                wIndex = wIndex + wForUnused
                wForUnusedUsed = True
            if attr["vOrient"] == self.V_ORIENT["Down"] and attr["fixedHeight"] != None and hForUnusedUsed == False:
                hIndex = hIndex + (self.hTerminal - (self.promptHeight + self.FRAME_SIZE) - attr["boxHeight"])
                hForUnusedUsed = True

            # topLeft point and bottomRight point of the box
            attr["topLeft"] = {"x" : wIndex, "y" : hIndex}
            attr["bottomRight"] = {"x" : wIndex + attr["boxWidth"] - 1, "y" : hIndex + attr["boxHeight"] - 1}

            # Text start/ end positions
            attr["textStartX"] = wIndex + self.FRAME_SIZE + attr["wTextIndent"]
            if self.debug and self.debugBoxPlacementShow == self.debugBoxPlacement["Top"]:
                attr["textStartY"] = hIndex + 2 + self.FRAME_SIZE + attr["hTextIndent"]
            else:
                attr["textStartY"] = hIndex + self.FRAME_SIZE + attr["hTextIndent"]

            hIndex = 0
            wIndex = wIndex + attr["boxWidth"]

        # TODO: Add edge condition cases (for visable False too)
        edgeConditions = []
        edgeConditions.append(self.hTerminal >= (self.BOX_MIN_HEIGHT + self.promptHeight + 1))
        edgeConditions.append(self.wTerminal >= (self.BOX_MIN_WIDTH * nbrOfBoxes))
        self.updateConditionsSatisfied = all(condition == True for condition in edgeConditions)

        self.promptLineWidth = self.wTerminal - (len(self.promptSign) + 1)


    def update_text_wrapping(self):
        """ Update text format by re-wrapping text to match new box sizes """
        for name, attr in self.box.items():
            self.box[name]["lines"] = list()
            for item, color in attr["textItems"]:
                lines = wrap(item, attr["textWidth"])
                for line in lines:
                    self.box[name]["lines"].append([line, color])


    def update_box_frames(self):
        """ Updates the frames for all the boxes as well as the bottom line that separate input bar from boxes. """
        for name, attr in self.box.items():
            if attr["visable"] == False:
                continue

            boxTLX = attr["topLeft"]["x"]
            boxTLY = attr["topLeft"]["y"]
            boxBRX = attr["bottomRight"]["x"]
            boxBRY = attr["bottomRight"]["y"]
            for row in range(self.hTerminal):
                for column in range(self.wTerminal):
                    # DEBUG BOX ON THE TOP OF EVERY BOX
                    if (boxTLY + 2) == row and boxTLX == column and self.debug and \
                            self.debugBoxPlacementShow == self.debugBoxPlacement["Top"]:
                        self.screen.addstr(row, column, self.frame["verticalRight"])
                    elif (boxTLY + 2) == row and boxBRX == column and self.debug and \
                            self.debugBoxPlacementShow == self.debugBoxPlacement["Top"]:
                        self.screen.addstr(row, column, self.frame["verticalLeft"])
                    elif (boxTLY + 2) == row and boxTLX < column and boxBRX > column and self.debug and \
                            self.debugBoxPlacementShow == self.debugBoxPlacement["Top"]:
                        self.screen.addstr(row, column, self.frame["horizontal"])

                    # DEBUG BOX ON THE BOTTOM OF EVERY BOX
                    elif (boxBRY - 2) == row and boxTLX == column and self.debug and \
                            self.debugBoxPlacementShow == self.debugBoxPlacement["Bottom"]:
                        self.screen.addstr(row, column, self.frame["verticalRight"])
                    elif (boxBRY - 2) == row and boxBRX == column and self.debug and \
                            self.debugBoxPlacementShow == self.debugBoxPlacement["Bottom"]:
                        self.screen.addstr(row, column, self.frame["verticalLeft"])
                    elif (boxBRY - 2) == row and boxTLX < column and boxBRX > column and self.debug \
                            and self.debugBoxPlacementShow == self.debugBoxPlacement["Bottom"]:
                        self.screen.addstr(row, column, self.frame["horizontal"])

                    # NORMAL BOX FRAME
                    elif boxTLY == row and boxTLX == column:
                        self.screen.addstr(row, column, self.frame["rightDown"])
                    elif boxTLY == row and boxBRX == column:
                        self.screen.addstr(row, column, self.frame["leftDown"])
                    elif boxBRY == row and boxTLX == column:
                        self.screen.addstr(row, column, self.frame["rightUp"])
                    elif boxBRY == row and boxBRX == column:
                        self.screen.addstr(row, column, self.frame["leftUp"])
                    elif (boxTLY == row or boxBRY == row) and boxTLX < column and boxBRX > column:
                        self.screen.addstr(row, column, self.frame["horizontal"])
                    elif boxTLY < row and boxBRY > row and (boxTLX == column or boxBRX == column):
                        self.screen.addstr(row, column, self.frame["vertical"])

            if self.debug:
                x = boxTLX + 1
                y = (boxTLY + 1) if self.debugBoxPlacementShow == self.debugBoxPlacement["Top"] else (boxBRY - 1)
                if self.debugBoxInfoShow == self.debugBoxInfo["name"]:
                    self.screen.addstr(y, x, name[:(attr["boxWidth"] - 1 - self.FRAME_SIZE)])
                elif self.debugBoxInfoShow == self.debugBoxInfo["textSize"]:
                    textSize = f'txt: w = {attr["textWidth"]}, h = {attr["textHeight"]}'
                    self.screen.addstr(y, x, textSize[:(attr["boxWidth"] - 1 - self.FRAME_SIZE)])
                elif self.debugBoxInfoShow == self.debugBoxInfo["boxSize"]:
                    boxSize = f'box: w = {attr["boxWidth"]}, h = {attr["boxHeight"]}'
                    self.screen.addstr(y, x, boxSize[:(attr["boxWidth"] - 1 - self.FRAME_SIZE)])

        self.screen.addstr(self.hTerminal - 1 - self.promptHeight, 0, \
            self.wTerminal * self.frame["horizontal"])



    def update_prompt(self):
        """ Update the prompt. """
        self.promptVLeftPos = self.promptCursorPos - self.promptVCursorPos
        self.promptVRightPos = self.promptVLeftPos + self.promptLineWidth

        displayedString = ""
        if len(self.promptString) >= self.promptLineWidth:
            displayedString = self.promptString[self.promptVLeftPos:self.promptVRightPos]
        else:
            displayedString = self.promptString
        self.screen.addstr(self.hTerminal - self.promptHeight, 0, self.promptSign + displayedString)


    def update_boxes(self):
        """ Updates all the boxes. """
        for name, attr in self.box.items():
            displayedText = list()
            if len(attr["lines"]) >= attr["textHeight"]:
                displayedText = attr["lines"][-attr["textHeight"] + attr["scrollIndex"]:][:attr["textHeight"]]
            else:
                displayedText = attr["lines"]

            for i, line in enumerate(displayedText):
                self.screen.addstr(attr["textStartY"] + i, attr["textStartX"], line[0], line[1])


    def update_visual_cursor(self):
        """ Update the visual cursor in the prompt. """
        self.screen.move(self.hTerminal - self.promptHeight, self.promptVCursorPos + len(self.promptSign))


    def createTextBox(self, name, width = None, height = None, hPos = None, vPos = 0, hOrient = 0, vOrient = 0,
                      visable = True, wTextIndent = 0, hTextIndent = 0):
        """
            Input parameters:
                name                - Name of the textbox.
                width               - None if not fixed width (becomes textWidth).          Default: None
                height              - None if not fixed height (becomes textHeight).        Default: None
                hPos                - Position between already existing boxes horizontally. Default: None
                vPos                - Position between already existing boxes vertically.   Default: 0      Not impl
                hOrient             - Horizontal orientation of the box.                    Default: 0 (Up)
                vOrient             - Vertical orientation of the box.                      Default: 0 (Left)
                visable             - If True the box is visable else it's not.             Default: True
                wTextIndent         - Width indentation for text.                           Default: 0
                hTextIndent         - Height indentation for text.                          Default: 0

            Box properties:
                name                - Name of the textbox
                fixedWidth          - None if not fixed width (becomes boxWidth).
                fixedHeight         - None if not fixed height (becomes boxHeight).
                hOrient             - Horizontal orientation of the box.                    Default: 0 (Up)
                vOrient             - Vertical orientation of the box.                      Default: 0 (Left)
                visable             - If True the box is visable else it's not.             Default: True
                wTextIndent         - Width indentation for text.                           Default: 0
                hTextIndent         - Height indentation for text.                          Default: 0
                boxWidth            - The width of the box (frame included).
                boxHeight           - The height of the box (frame included).
                textWidth           - The width of the text inside the box.
                textHeight          - The height of the text inside the box.
                topLeft             - Top left coordinate of the box.
                bottomRight         - Bottom right coordinate of the box.
                textStartX          - x-coordinate of where the text start in the box.
                textStartY          - y-coordinate of where the text start in the box.

            Box Text variables:
                textItems           - List of all the text items (One list item is one continuous message along
                                      with text color and other attributes).
                lines               - List of formatted textItems that is splitted to fit the text box width.
                scrollIndex         - Scroll index that keeps track of how much text in box have been scrolled.
        """
        if not isinstance(name, str):
            raise Exception("name is not of string type.")
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

        if hPos != None:
            if not isinstance(hPos, int):
                raise Exception("hPos is not of integer type")
            self.boxOrder.insert(hPos, name)
            prevBoxIndex = (self.boxOrder.index(name) - 1) if self.boxOrder.index(name) > 0 else 0
            self.box[name]["hOrient"] = self.box[self.boxOrder[prevBoxIndex]]["hOrient"]
            # TODO: fix vPos as well, check how big list is? (How deep vertical is)
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

        self.box[name]["textItems"] = list()
        self.box[name]["lines"] = list
        self.box[name]["scrollIndex"] = 0


    def __key_handler(self, event):
        """ Handler of key presses. """
        while True:
            char = self.screen.get_wch()

            if char == "\x1b":                  # <ESC> KEY (Exit)
                break

            elif char == 259:                   # <ARROW-UP> KEY (Scroll up)
                #if len(self.textBoxLines) + self.textBoxScrollIndex > self.textBoxHeight:
                #    self.textBoxScrollIndex -= 1
                pass

            elif char == 258:                   # <ARROW-DOWN> KEY (Scroll down)
                if self.textBoxScrollIndex != 0:
                    self.textBoxScrollIndex += 1

            elif char == 260:                   # <ARROW-LEFT> KEY (Scroll left)
                if self.promptVCursorPos != 0:
                    self.promptVCursorPos -= 1
                if self.promptCursorPos != 0:
                    self.promptCursorPos -= 1

            elif char == 261:                   # <ARROW-RIGHT> KEY (Scroll right)
                if self.promptVCursorPos < len(self.promptString) and \
                   self.promptVCursorPos != self.promptLineWidth:
                    self.promptVCursorPos += 1
                if self.promptCursorPos < len(self.promptString):
                    self.promptCursorPos += 1

            elif char == "\x00":                # WINDOWS KEY
                pass

            elif char == curses.KEY_RESIZE:     # RESIZE EVENT
                self.promptCursorPos = 0
                self.promptVCursorPos = 0

            elif char == 262:                   # HOME KEY
                self.promptVCursorPos = 0
                self.promptCursorPos = 0

            elif char == 358 or char == 360:    # END KEY
                if len(self.promptString) >= self.promptLineWidth:
                    self.promptVCursorPos = self.promptLineWidth
                else:
                    self.promptVCursorPos = len(self.promptString)
                self.promptCursorPos = len(self.promptString)

            elif char == "\n": # <ENTER>
                if self.promptString != "":
                    self.textBoxMessages.append([self.promptString,
                        curses.color_pair(self.COLORS["white"]) | curses.A_STANDOUT])
                self.promptString = ""
                self.promptCursorPos = 0
                self.promptVCursorPos = 0
                self.textBoxScrollIndex = 0

            elif char == 330:                   # DELETE KEY
                self.promptString = self.promptString[:self.promptCursorPos] + \
                    self.promptString[self.promptCursorPos:][1:]

                if len(self.promptString) >= self.promptLineWidth:
                    if len(self.promptString) == (self.promptVRightPos - 1) and \
                       self.promptVCursorPos != self.promptLineWidth:
                        self.promptVCursorPos += 1

            elif char == "\x08" or char == 263: # BACKSPACE KEY
                self.promptString = self.promptString[:self.promptCursorPos][:-1] + \
                    self.promptString[self.promptCursorPos:]

                if self.promptVCursorPos != 0 and len(self.promptString) <= self.promptLineWidth and \
                   self.promptVLeftPos == 0:
                    self.promptVCursorPos -= 1
                elif self.promptVCursorPos != 0 and len(self.promptString) >= self.promptLineWidth and \
                     self.promptVLeftPos == 0:
                    self.promptVCursorPos -= 1
                if self.promptCursorPos != 0:
                    self.promptCursorPos -= 1

            elif char == 339:                   # PAGE UP
                #self.textBoxScrollIndex -= self.textBoxHeight
                #if self.textBoxScrollIndex < -(len(self.textBoxLines) - self.textBoxHeight):
                #    self.textBoxScrollIndex = -(len(self.textBoxLines) - self.textBoxHeight)
                pass

            elif char == 338:                   # PAGE DOWN
                #self.textBoxScrollIndex += self.textBoxHeight
                #if self.textBoxScrollIndex > 0:
                #    self.textBoxScrollIndex = 0
                pass

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

            else: # Append characters to self.promptString
                self.promptString =   self.promptString[:self.promptCursorPos] + str(char) + \
                    self.promptString[self.promptCursorPos:]
                if self.promptVCursorPos != self.promptLineWidth:
                    self.promptVCursorPos += 1
                self.promptCursorPos += 1

            self.update()

        curses.endwin() # Close curses terminal






if __name__ == "__main__":
    obj = TerminalTextBoxes()

    #obj.createTextBox("HejsanHejsanHejsanHejsanHejsan")
    #obj.createTextBox("Hejsan1", 20, visable=False)
    #obj.createTextBox("123456789012345678901234567890", 10, verticalOrientation=obj.VERTICAL_ORIENTATION["Left"])
    #obj.createTextBox("Hejsan4", 22, hOrient=obj.H_ORIENT["Right"])

    #obj.createTextBox("Hejsan1", 5, hOrient=obj.H_ORIENT["Left"], visable=True)
    obj.createTextBox("TestBox2", hOrient=obj.H_ORIENT["Right"], wTextIndent=2)
    #obj.createTextBox("Hejsan3", 10, 10, hOrient=obj.H_ORIENT["Right"], vOrient=obj.V_ORIENT["Down"])
    #obj.createTextBox("Hejsan4", hOrient=obj.H_ORIENT["Right"], height=10)
    #obj.createTextBox("Hejsan5", 20, hOrient=obj.H_ORIENT["Right"])

    #obj.createTextBox("TestBox2", height=10, hOrient=obj.H_ORIENT["Right"], vOrient=obj.V_ORIENT["Up"])
    #obj.createTextBox("TestBox1", 15, 10, hOrient=obj.H_ORIENT["Right"], vOrient=obj.V_ORIENT["Down"])
    #obj.createTextBox("TestBox3", 15, 10, hOrient=obj.H_ORIENT["Right"], vOrient=obj.V_ORIENT["Up"])

    #obj.createTextBox("Inbetween", 20, 20, vOrient=obj.V_ORIENT["Up"], hPos=1)

    obj.createTextBox("TestBox1", 25, 30, wTextIndent=2, hTextIndent=1)
    txt = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
    for a in range(10):
        obj.box["TestBox1"]["textItems"].append([txt, curses.color_pair(obj.COLORS["green"])])

    for a in range(10):
        obj.box["TestBox2"]["textItems"].append([txt, curses.color_pair(obj.COLORS["red"])])


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
