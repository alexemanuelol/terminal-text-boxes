#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import curses
import time
import threading

from textwrap import wrap
from pynput.keyboard import Key, Controller

from unicode import isUnicode


class TerminalTextBoxes():
    """  """
    def __init__(self):
        """ Init. """
        self.fakeKeyboard = Controller()

        # Text color/ attribute variables
        self.TEXT_COLOR = {
            "black"                 : 1,
            "blue"                  : 2,
            "green"                 : 3,
            "cyan"                  : 4,
            "red"                   : 5,
            "magenta"               : 6,
            "yellow"                : 7,
            "white"                 : 8
        }

        # Text attributes
        self.TEXT_ATTR = {
            "altCharset"            : curses.A_ALTCHARSET,
            "blink"                 : curses.A_BLINK,
            "bold"                  : curses.A_BOLD,
            "dim"                   : curses.A_DIM,
            "invis"                 : curses.A_INVIS,
            "italic"                : curses.A_ITALIC,
            "normal"                : curses.A_NORMAL,
            "protect"               : curses.A_PROTECT,
            "reverse"               : curses.A_REVERSE,
            "standout"              : curses.A_STANDOUT,
            "underline"             : curses.A_UNDERLINE,
            "horizontal"            : curses.A_HORIZONTAL,
            "left"                  : curses.A_LEFT,
            "low"                   : curses.A_LOW,
            "right"                 : curses.A_RIGHT,
            "top"                   : curses.A_TOP,
            "vertical"              : curses.A_VERTICAL,
            "chartext"              : curses.A_CHARTEXT
        }

        # Frame variables
        self.FRAME_STYLE = {
            "singleLine"            : ["│", "┤", "├", "─", "┴", "┬", "┘", "┐", "└", "┌", "┼"],
            "doubleLine"            : ["║", "╣", "╠", "═", "╩", "╦", "╝", "╗", "╚", "╔", "╬"],
            "hash"                  : ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#"],
            "at"                    : ["@", "@", "@", "@", "@", "@", "@", "@", "@", "@", "@"],
            "star"                  : ["*", "*", "*", "*", "*", "*", "*", "*", "*", "*", "*"],
            "blockFull"             : ["█", "█", "█", "█", "█", "█", "█", "█", "█", "█", "█"],
            "blockVague0"           : ["▓", "▓", "▓", "▓", "▓", "▓", "▓", "▓", "▓", "▓", "▓"],
            "blockVague1"           : ["▒", "▒", "▒", "▒", "▒", "▒", "▒", "▒", "▒", "▒", "▒"],
            "blockVague2"           : ["░", "░", "░", "░", "░", "░", "░", "░", "░", "░", "░"],
            "invisible"             : [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "]
        }

        self.FRAME_SIZE = 1
        self.frame = {
            "vertical"              : self.FRAME_STYLE["singleLine"][0],
            "verticalLeft"          : self.FRAME_STYLE["singleLine"][1],
            "verticalRight"         : self.FRAME_STYLE["singleLine"][2],
            "horizontal"            : self.FRAME_STYLE["singleLine"][3],
            "horizontalUp"          : self.FRAME_STYLE["singleLine"][4],
            "horizontalDown"        : self.FRAME_STYLE["singleLine"][5],
            "leftUp"                : self.FRAME_STYLE["singleLine"][6],
            "leftDown"              : self.FRAME_STYLE["singleLine"][7],
            "rightUp"               : self.FRAME_STYLE["singleLine"][8],
            "rightDown"             : self.FRAME_STYLE["singleLine"][9],
            "cross"                 : self.FRAME_STYLE["singleLine"][10]
        }

        # Terminal Box Setups
        self.boxSetup               = dict()
        self.activeBoxSetup         = None

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

        # Prompt info box
        self.infoPromptBg           = "═"
        self.infoPromptBgAttr       = "white"
        self.infoPromptTextAttr     = "yellow"
        self.infoPromptCurrMessage  = ""
        self.infoPromptActive       = False
        self.infoPromptTextIndent   = 3
        self.infoPromptTimer        = threading.Timer(5, self.reset_info_prompt)

        # wrap if the text item can wrap, single if text item only should be displayed on a single line
        self.LINE_TYPE = {
            "wrap"                  : 0,
            "single"                : 1
        }

        # Minimum sizes
        self.PROMPT_MIN_WIDTH       = self.promptSignSize + 10
        self.PROMPT_MIN_HEIGHT      = 1
        self.BOX_MIN_WIDTH          = self.FRAME_SIZE * 2
        self.BOX_MIN_HEIGHT         = self.FRAME_SIZE * 2

        # Orientations
        self.H_ORIENT = {
            "Left"                  : 0,
            "Right"                 : 1
        }
        self.V_ORIENT = {
            "Up"                    : 0,
            "Down"                  : 1
        }

        # Debug variables
        self.debugBoxPlacement = {
            "Top"                   : 0,
            "Bottom"                : 1
        }
        self.debugBoxInfo = {
            "name"                  : 0,
            "textSize"              : 1,
            "boxSize"               : 2
        }

        self.debug                  = True
        self.debugBoxPlacementShow  = 0
        self.debugBoxInfoShow       = 0


    def start(self):
        """ Start displaying the terminal text boxes module. """
        # Terminal window initialization
        self.screen = curses.initscr()
        self.screen.keypad(True)
        curses.noecho()

        self.init_colors()

        self.update_boxes_frame_attr()

        self.update()

        event = threading.Event()
        thread = threading.Thread(target=self.__key_handler, args=(event,))
        thread.start()


    def stop(self):
        """ Stop displaying the terminal text boxes module. """
        self.fakeKeyboard.press(Key.esc)


    def init_colors(self):
        """ Init curses colors. """
        curses.start_color()
        curses.use_default_colors()

        for color, value in self.TEXT_COLOR.items():
            curses.init_pair(value, value - 1, -1)


    def update_boxes_frame_attr(self):
        """  """
        for setupName, setupAttr in self.boxSetup.items():
            for boxName, boxAttr in setupAttr["boxes"].items():
                boxAttr["frameAttr"] = self.merge_attributes(boxAttr["frameAttrUnmerged"])


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

        nbrOfBoxes = len(self.boxSetup[self.activeBoxSetup]["boxes"]) # Total amount of current boxes
        nbrOfWUnfixedBoxes = 0      # Number of boxes that does not have fixed width
        nbrOfWFixedBoxes = 0        # Number of boxes that does have fixed width
        wForFixed = 0               # Width of all fixed width boxes together
        for name, attr in self.boxSetup[self.activeBoxSetup]["boxes"].items():
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
        for name, attr in self.boxSetup[self.activeBoxSetup]["boxes"].items():
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
        for name, attr in self.boxSetup[self.activeBoxSetup]["boxes"].items():
            self.boxSetup[self.activeBoxSetup]["boxes"][name]["lines"] = list()
            for item, txtAttr, lineType in attr["textItems"]:
                if lineType == self.LINE_TYPE["single"]:
                    self.boxSetup[self.activeBoxSetup]["boxes"][name]["lines"].append(
                            [item[:attr["textWidth"]], txtAttr])
                else:
                    lines = wrap(item, attr["textWidth"])
                    for line in lines:
                        self.boxSetup[self.activeBoxSetup]["boxes"][name]["lines"].append([line, txtAttr])


    def update_box_frames(self):
        """ Updates the frames for all the boxes as well as the bottom line that separate input bar from boxes. """
        for name, attr in self.boxSetup[self.activeBoxSetup]["boxes"].items():
            if attr["visable"] == False:
                continue

            boxTLX = attr["topLeft"]["x"]
            boxTLY = attr["topLeft"]["y"]
            boxBRX = attr["bottomRight"]["x"]
            boxBRY = attr["bottomRight"]["y"]

            if name == self.boxSetup[self.activeBoxSetup]["focusedBox"] and self.debug:
                self.screen.addstr(boxTLY + 1, boxBRX - 1, "*", curses.color_pair(self.TEXT_COLOR["red"]))

            for row in range(self.hTerminal):
                for column in range(self.wTerminal):
                    # DEBUG BOX ON THE TOP OF EVERY BOX
                    if (boxTLY + 2) == row and boxTLX == column and self.debug and \
                            self.debugBoxPlacementShow == self.debugBoxPlacement["Top"]:
                        self.screen.addstr(row, column, self.frame["verticalRight"], attr["frameAttr"])
                    elif (boxTLY + 2) == row and boxBRX == column and self.debug and \
                            self.debugBoxPlacementShow == self.debugBoxPlacement["Top"]:
                        self.screen.addstr(row, column, self.frame["verticalLeft"], attr["frameAttr"])
                    elif (boxTLY + 2) == row and boxTLX < column and boxBRX > column and self.debug and \
                            self.debugBoxPlacementShow == self.debugBoxPlacement["Top"]:
                        self.screen.addstr(row, column, self.frame["horizontal"], attr["frameAttr"])

                    # DEBUG BOX ON THE BOTTOM OF EVERY BOX
                    elif (boxBRY - 2) == row and boxTLX == column and self.debug and \
                            self.debugBoxPlacementShow == self.debugBoxPlacement["Bottom"]:
                        self.screen.addstr(row, column, self.frame["verticalRight"], attr["frameAttr"])
                    elif (boxBRY - 2) == row and boxBRX == column and self.debug and \
                            self.debugBoxPlacementShow == self.debugBoxPlacement["Bottom"]:
                        self.screen.addstr(row, column, self.frame["verticalLeft"], attr["frameAttr"])
                    elif (boxBRY - 2) == row and boxTLX < column and boxBRX > column and self.debug \
                            and self.debugBoxPlacementShow == self.debugBoxPlacement["Bottom"]:
                        self.screen.addstr(row, column, self.frame["horizontal"], attr["frameAttr"])

                    # NORMAL BOX FRAME
                    elif boxTLY == row and boxTLX == column:
                        self.screen.addstr(row, column, self.frame["rightDown"], attr["frameAttr"])
                    elif boxTLY == row and boxBRX == column:
                        self.screen.addstr(row, column, self.frame["leftDown"], attr["frameAttr"])
                    elif boxBRY == row and boxTLX == column:
                        self.screen.addstr(row, column, self.frame["rightUp"], attr["frameAttr"])
                    elif boxBRY == row and boxBRX == column:
                        self.screen.addstr(row, column, self.frame["leftUp"], attr["frameAttr"])
                    elif (boxTLY == row or boxBRY == row) and boxTLX < column and boxBRX > column:
                        self.screen.addstr(row, column, self.frame["horizontal"], attr["frameAttr"])
                    elif boxTLY < row and boxBRY > row and (boxTLX == column or boxBRX == column):
                        self.screen.addstr(row, column, self.frame["vertical"], attr["frameAttr"])

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

        if not self.infoPromptActive:
            self.reset_info_prompt()
        else:
            self.set_info_prompt_message(self.infoPromptCurrMessage)



    def update_prompt(self):
        """ Update the prompt. """
        self.promptVLeftPos = self.promptCursorPos - self.promptVCursorPos
        self.promptVRightPos = self.promptVLeftPos + self.promptLineWidth

        # Clear prompt
        txt = " " * (self.wTerminal - 1)
        for i in range(self.promptHeight):
            self.screen.addstr(self.hTerminal - self.promptHeight - i, 0, txt)

        displayedString = ""
        if len(self.promptString) >= self.promptLineWidth:
            displayedString = self.promptString[self.promptVLeftPos:self.promptVRightPos]
        else:
            displayedString = self.promptString
        self.screen.addstr(self.hTerminal - self.promptHeight, 0, self.promptSign + displayedString)


    def update_boxes(self):
        """ Updates all the boxes. """
        for name, attr in self.boxSetup[self.activeBoxSetup]["boxes"].items():
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


    def reset_info_prompt(self):
        """  """
        startOfInfoPromptX = 0
        startOfInfoPromptY = self.hTerminal - 1 - self.promptHeight
        bg = self.merge_attributes(self.infoPromptBgAttr)
        self.screen.addstr(startOfInfoPromptY, startOfInfoPromptX, self.wTerminal * self.infoPromptBg, bg)


    def set_info_prompt_message(self, message, timeout=None):
        """ Timeout = ms """
        if not isinstance(message,str):
            raise Exception("Message needs to be of type str.")

        self.reset_info_prompt()

        infoPromptY = self.hTerminal - 1 - self.promptHeight
        textStartX = self.infoPromptTextIndent + 1
        textMaxLen = self.wTerminal - (self.infoPromptTextIndent * 2) - 2
        textEndX = textStartX + len(message[:textMaxLen])

        self.infoPromptCurrMessage = message
        bgAttr = self.merge_attributes(self.infoPromptBgAttr)
        textAttr = self.merge_attributes(self.infoPromptTextAttr)

        self.screen.addstr(infoPromptY, self.infoPromptTextIndent," ", bgAttr)
        self.screen.addstr(infoPromptY, textStartX, message[:textMaxLen], textAttr)
        self.screen.addstr(infoPromptY, textEndX," ", bgAttr)

        if timeout != None:
            self.infoPromptTimer.cancel()
            self.infoPromptTimer = threading.Timer(timeout//1000, self.__info_prompt_text_timeout)
            self.infoPromptTimer.start()
            self.infoPromptActive = True
        self.screen.refresh()

    def __info_prompt_text_timeout(self):
        """  """
        self.infoPromptActive = False
        self.reset_info_prompt()
        self.update_visual_cursor()
        self.screen.refresh()


    def create_text_box_setup(self, name):
        """ Creates a new 'text box setup' in which you can add text boxes to. """
        if not isinstance(name, str):
            raise Exception("name is not of string type.")
        if name in self.boxSetup:
            raise Exception(f"TextBoxSetup {name} already exists.")

        self.boxSetup[name] = {}

        self.boxSetup[name]["boxes"] = dict()
        self.boxSetup[name]["boxOrder"] = list()
        self.boxSetup[name]["focusedBox"] = None

        self.activeBoxSetup = name


    def create_text_box(self, setupName, boxName, width = None, height = None, hPos = None, vPos = 0, hOrient = 0,
                        vOrient = 0, visable = True, wTextIndent = 0, hTextIndent = 0, frameAttr="white"):
        """
            Input parameters:
                setupName           - Name of the box setup that the box belongs to.
                boxName             - Name of the textbox.
                width               - None if not fixed width (becomes textWidth).          Default: None
                height              - None if not fixed height (becomes textHeight).        Default: None
                hPos                - Position between already existing boxes horizontally. Default: None
                vPos                - Position between already existing boxes vertically.   Default: 0      Not impl
                hOrient             - Horizontal orientation of the box.                    Default: 0 (Up)
                vOrient             - Vertical orientation of the box.                      Default: 0 (Left)
                visable             - If True the box is visable else it's not.             Default: True
                wTextIndent         - Width indentation for text.                           Default: 0
                hTextIndent         - Height indentation for text.                          Default: 0
                frameAttr           - The attributes of the frame.                          Default: white

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
        if not isinstance(setupName, str):
            raise Exception("setupName is not of string type.")
        if setupName not in self.boxSetup:
            raise Exception(f"Box setup {name} does not exist.")

        if not isinstance(boxName, str):
            raise Exception("name is not of string type.")
        if boxName in self.boxSetup[setupName]["boxes"]:
            raise Exception(f"TextBox {boxName} already exists.")

        self.boxSetup[setupName]["boxes"][boxName] = dict()
        self.boxSetup[setupName]["focusedBox"] = boxName

        if width != None and not isinstance(width, int):
            raise Exception("width is not of integer type.")
        self.boxSetup[setupName]["boxes"][boxName]["fixedWidth"] = width
        if height != None and not isinstance(height, int):
            raise Exception("height is not of integer type.")
        self.boxSetup[setupName]["boxes"][boxName]["fixedHeight"] = height

        if not isinstance(hOrient, int) or hOrient not in self.H_ORIENT.values():
            raise Exception("hOrient is not of integer type or not within acceptable range.")
        self.boxSetup[setupName]["boxes"][boxName]["hOrient"] = hOrient

        if not isinstance(vOrient, int) or vOrient not in self.V_ORIENT.values():
            raise Exception("vOrient is not of integer type or not within acceptable range.")
        self.boxSetup[setupName]["boxes"][boxName]["vOrient"] = vOrient

        if hPos != None:
            if not isinstance(hPos, int):
                raise Exception("hPos is not of integer type")
            self.boxSetup[setupName]["boxOrder"].insert(hPos, boxName)

            if self.boxSetup[setupName]["boxOrder"].index(boxName) > 0:
                prevBoxIndex = self.boxSetup[setupName]["boxOrder"].index(boxName) - 1
            else:
                prevBoxIndex = 0

            self.boxSetup[setupName]["boxes"][boxName]["hOrient"] = \
                    self.boxSetup[setupName]["boxes"][self.boxSetup[setupName]["boxOrder"][prevBoxIndex]]["hOrient"]

            # TODO: fix vPos as well, check how big list is? (How deep vertical is)
        elif hOrient == self.H_ORIENT["Left"]:
            self.boxSetup[setupName]["boxOrder"].insert(0, boxName)
        elif hOrient == self.H_ORIENT["Right"]:
            self.boxSetup[setupName]["boxOrder"].append(boxName)
        else:
            self.boxSetup[setupName]["boxOrder"].append(boxName)
        # Sort dict according to boxOrder
        self.boxSetup[setupName]["boxes"] = \
                {key : self.boxSetup[setupName]["boxes"][key] for key in self.boxSetup[setupName]["boxOrder"]}

        if visable != True and visable != False:
            raise Exception("visable not a boolean.")
        self.boxSetup[setupName]["boxes"][boxName]["visable"] = visable

        if  not isinstance(wTextIndent, int):
            raise Exception("wTextIndent is not of integer type.")
        self.boxSetup[setupName]["boxes"][boxName]["wTextIndent"] = wTextIndent
        if not isinstance(hTextIndent, int):
            raise Exception("hTextIndent is not of integer type.")
        self.boxSetup[setupName]["boxes"][boxName]["hTextIndent"] = hTextIndent

        self.boxSetup[setupName]["boxes"][boxName]["textItems"] = list()
        self.boxSetup[setupName]["boxes"][boxName]["lines"] = list()
        self.boxSetup[setupName]["boxes"][boxName]["scrollIndex"] = 0

        self.boxSetup[setupName]["boxes"][boxName]["frameAttrUnmerged"] = frameAttr


    def add_text_item(self, setupName, boxName, message, attributes="white", lineType="wrap"):
        """ Add a text item to the textItems list of messages. """
        if boxName not in self.boxSetup[setupName]["boxes"]:
            raise Exception(f"Box {boxName} is not in box setup {setupName} dictonary.")

        attributes = self.merge_attributes(attributes)

        if lineType not in self.LINE_TYPE:
            raise Exception(f"Line type {lineType} does not exist.")

        self.boxSetup[setupName]["boxes"][boxName]["textItems"].append([message, attributes, self.LINE_TYPE[lineType]])


    def merge_attributes(self, attributes):
        """ Merges all attribute values to a single attribute and returns it.
            Raises exception if invalid attribute exist.
        """
        if attributes == None:
            return None

        if isinstance(attributes, list) or isinstance(attributes, str):
            if isinstance(attributes, str):
                attributes = [attributes]
        else:
            raise Exception("Attributes needs to be either string or list.")

        merged = 0
        for item in attributes:
            if item in self.TEXT_COLOR:
                merged = merged | curses.color_pair(self.TEXT_COLOR[item])
            elif item in self.TEXT_ATTR:
                merged = merged | self.TEXT_ATTR[item]
            else:
                raise Exception(f"Attribute {item} is not available.")

        return merged


    def set_focus_box(self, setupName, boxName):
        """ Set a box in focus i.e. make it scrollable. """
        if boxName not in self.boxSetup[setupName]["boxes"]:
            raise Exception(f"Box {boxName} is not in box setup {setupName} dictonary.")

        self.boxSetup[setupName]["focusedBox"] = boxName


    def set_active_box_setup(self, setupName):
        """  """
        if setupName not in self.boxSetup:
            raise Exception(f"Setup {setupName} does not exist in boxSetup dictonary.")

        self.activeBoxSetup = setupName


    def set_box_frame_attr(self, setupName, boxName, attributes):
        """  """
        if not isinstance(setupName, str):
            raise Exception("setupName is not of string type.")
        if setupName not in self.boxSetup:
            raise Exception(f"Box setup {name} does not exist.")

        if not isinstance(boxName, str):
            raise Exception("name is not of string type.")
        if boxName not in self.boxSetup[setupName]["boxes"]:
            raise Exception(f"TextBox {boxName} does not exist.")

        self.boxSetup[setupName]["boxes"][boxName]["frameAttrUnmerged"] = attributes


    def __key_handler(self, event):
        """ Handler of key presses. """
        while True:
            char = self.screen.get_wch()

            focusedBox = self.boxSetup[self.activeBoxSetup]["focusedBox"]

            # GENERAL KEY EVENTS --------------------------------------------------------------------------------------
            if char == "\x1b":                  # <ESC> KEY (Exit)
                break

            elif char == "\x00":                # "WINDOWS" KEY
                pass

            elif char == curses.KEY_RESIZE:     # RESIZE EVENT
                self.promptCursorPos = 0
                self.promptVCursorPos = 0


            # PROMPT KEY EVENTS ---------------------------------------------------------------------------------------
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

            elif char == 262:                   # HOME KEY
                self.promptVCursorPos = 0
                self.promptCursorPos = 0

            elif char == 358 or char == 360:    # END KEY
                if len(self.promptString) >= self.promptLineWidth:
                    self.promptVCursorPos = self.promptLineWidth
                else:
                    self.promptVCursorPos = len(self.promptString)
                self.promptCursorPos = len(self.promptString)

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

            elif char == "\n": # <ENTER>
                if self.promptString != "":
                    self.add_text_item("setup", "box", self.promptString, ["blue", "bold"], lineType="wrap")
                self.set_info_prompt_message(self.promptString, 5000)
                self.promptString = ""
                self.promptCursorPos = 0
                self.promptVCursorPos = 0
                #TEMP:
                self.boxSetup[self.activeBoxSetup]["boxes"][focusedBox]["scrollIndex"] = 0


            # BOX KEY EVENTS ------------------------------------------------------------------------------------------
            elif char == 259:                   # <ARROW-UP> KEY (Scroll up)
                lines = self.boxSetup[self.activeBoxSetup]["boxes"][focusedBox]["lines"]
                scrollIndex = self.boxSetup[self.activeBoxSetup]["boxes"][focusedBox]["scrollIndex"]
                textHeight = self.boxSetup[self.activeBoxSetup]["boxes"][focusedBox]["textHeight"]
                if len(lines) + scrollIndex > textHeight:
                    self.boxSetup[self.activeBoxSetup]["boxes"][focusedBox]["scrollIndex"] -= 1

            elif char == 258:                   # <ARROW-DOWN> KEY (Scroll down)
                if self.boxSetup[self.activeBoxSetup]["boxes"][focusedBox]["scrollIndex"] != 0:
                    self.boxSetup[self.activeBoxSetup]["boxes"][focusedBox]["scrollIndex"] += 1

            elif char == 339:                   # PAGE UP (Scroll up)
                lines = self.boxSetup[self.activeBoxSetup]["boxes"][focusedBox]["lines"]
                textHeight = self.boxSetup[self.activeBoxSetup]["boxes"][focusedBox]["textHeight"]
                self.boxSetup[self.activeBoxSetup]["boxes"][focusedBox]["scrollIndex"] -= textHeight
                scrollIndex = self.boxSetup[self.activeBoxSetup]["boxes"][focusedBox]["scrollIndex"]
                if scrollIndex < -(len(lines) - textHeight):
                    self.boxSetup[self.activeBoxSetup]["boxes"][focusedBox]["scrollIndex"] = -(len(lines) - textHeight)

            elif char == 338:                   # PAGE DOWN (Scroll down)
                textHeight = self.boxSetup[self.activeBoxSetup]["boxes"][focusedBox]["textHeight"]
                self.boxSetup[self.activeBoxSetup]["boxes"][focusedBox]["scrollIndex"] += textHeight
                if self.boxSetup[self.activeBoxSetup]["boxes"][focusedBox]["scrollIndex"] > 0:
                    self.boxSetup[self.activeBoxSetup]["boxes"][focusedBox]["scrollIndex"] = 0


            # REGULAR ASCII KEY EVENTS --------------------------------------------------------------------------------
            else: # Append characters to self.promptString
                if isUnicode(char):
                    self.promptString =   self.promptString[:self.promptCursorPos] + str(char) + \
                        self.promptString[self.promptCursorPos:]
                    if self.promptVCursorPos != self.promptLineWidth:
                        self.promptVCursorPos += 1
                    self.promptCursorPos += 1
                self.update_prompt()
                continue

            self.update()

        curses.endwin() # Close curses terminal






if __name__ == "__main__":
    obj = TerminalTextBoxes()

    obj.create_text_box_setup("setup")
    obj.create_text_box("setup", "box", frameAttr="red")
    obj.create_text_box("setup", "box1", 20, 20, hOrient=obj.H_ORIENT["Right"], frameAttr="green")
    obj.set_focus_box("setup", "box")

    obj.set_box_frame_attr("setup", "box", "cyan")


    obj.create_text_box_setup("setup2")
    obj.create_text_box("setup2", "box2")

    obj.set_active_box_setup("setup")

    obj.start()


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
