#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import curses
import sys
import time
import threading

from pynput.keyboard import Key, Controller
from textwrap import wrap

from unicode import isUnicode

if sys.platform == "win32":
    import win32clipboard


# Char color
CHAR_COLOR = {
    "black"                 : 1,
    "blue"                  : 2,
    "green"                 : 3,
    "cyan"                  : 4,
    "red"                   : 5,
    "magenta"               : 6,
    "yellow"                : 7,
    "white"                 : 8
}

# Char attributes
CHAR_ATTR = {
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
FRAME_STYLE = {
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



class TerminalTextBoxes():
    """  """
    def __init__(self, callback):
        """ Init. """
        self.fakeKeyboard = Controller()

        # Prompt callback function
        self.promptCallbackFunction = callback

        # Operating system
        self.platform = sys.platform
        self.platform_linux = ["linux", "linux2"]
        self.platform_windows = ["Windows", "win32", "cygwin"]
        self.platform_mac = ["Mac", "darwin", "os2", "os2emx"]

        self.FRAME_SIZE = 1

        # Resize variables
        self.resizeDone             = True
        self.resizeTimer            = threading.Timer(.1, self.resize_timeout)

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
        self.infoPromptHeight       = 1
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
        self.PROMPT_MIN_HEIGHT      = self.promptHeight
        self.INFO_PROMPT_MIN_WIDTH  = self.infoPromptTextIndent * 2 + (2 + 5)
        self.INFO_PROMPT_MIN_HEIGHT = self.infoPromptHeight
        self.BOX_MIN_WIDTH          = (self.FRAME_SIZE * 2) + 1
        self.BOX_MIN_HEIGHT         = (self.FRAME_SIZE * 2) + 1

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


    ###################################################################################################################
    # PUBLIC FUNCTIONS                                                                                                #
    ###################################################################################################################

    def start(self):
        """ Start displaying the terminal text boxes module. """
        # Terminal window initialization
        if not self.boxSetup:
            raise Exception("There are no setups created.")
        if len(self.boxSetup[self.activeBoxSetup]["boxes"]) == 0:
            raise Exception("There are no boxes in the active box setup.")

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


    def create_text_box_setup(self, name):
        """ Creates a new 'text box setup' in which you can add text boxes to. """
        self.__check_box_setup_valid(name, False)

        self.boxSetup[name] = {}

        self.boxSetup[name]["boxes"] = dict()
        self.boxSetup[name]["boxOrder"] = list()
        self.boxSetup[name]["focusedBox"] = None

        self.activeBoxSetup = name


    def create_text_box(self, setupName, boxName, width = None, height = None, hPos = None, vPos = 0, hOrient = 0,
                        vOrient = 0, visable = True, wTextIndent = 0, hTextIndent = 0, frameChar="singleLine",
                        frameAttr="white", scrollVisable=True):
        """
            Input parameters:
                setupName           - Name of the box setup that the box belongs to.
                boxName             - Name of the textbox.
                width               - None if not fixed width (becomes textWidth).          Default: None
                height              - None if not fixed height (becomes textHeight).        Default: None
                hPos                - Position between already existing boxes horizontally. Default: None
                vPos                - Position between already existing boxes vertically.   Default: 0      Not impl
                hOrient             - Horizontal orientation of the box.                    Default: 0 (Left)
                vOrient             - Vertical orientation of the box.                      Default: 0 (Up)
                visable             - If True the box is visable else it's not.             Default: True
                wTextIndent         - Width indentation for text.                           Default: 0
                hTextIndent         - Height indentation for text.                          Default: 0
                frameChar           - Character for the frame.                              Default: singleLine
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
                prevBoxWidth        - The previous box width.
                prevBoxHeight       - The previous box height.
                prevTextItemsLength - The previous length of the textItems variable.
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
        self.__check_text_box_valid(setupName, boxName, False)

        self.__init_box_default_parameters(setupName, boxName)

        if width != None and not isinstance(width, int):
            raise Exception("width is not of integer type.")
        if width != None and width < self.BOX_MIN_WIDTH:
            raise Exception(f"width is too small, must be bigger than or equal to {self.BOX_MIN_WIDTH}")
        if width != None and width < (self.BOX_MIN_WIDTH + 2 * wTextIndent):
            raise Exception(f"width is too small, must be bigger than or equal to {self.BOX_MIN_WIDTH + 2 * wTextIndent}")
        self.boxSetup[setupName]["boxes"][boxName]["fixedWidth"] = width

        if height != None and not isinstance(height, int):
            raise Exception("height is not of integer type.")
        if height != None and height < self.BOX_MIN_HEIGHT:
            raise Exception(f"height is too small, must be bigger than or equal to {self.BOX_MIN_HEIGHT}")
        if height != None and height < (self.BOX_MIN_HEIGHT + 2 * hTextIndent):
            raise Exception(f"height is too small, must be bigger than or equal to {self.BOX_MIN_HEIGHT + 2 * hTextIndent}")
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

        self.boxSetup[setupName]["boxes"][boxName]["frameChar"] = frameChar
        self.boxSetup[setupName]["boxes"][boxName]["frameAttrUnmerged"] = frameAttr

        self.boxSetup[setupName]["boxes"][boxName]["scrollVisable"] = scrollVisable


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


    def add_text_item(self, setupName, boxName, message, attributes="white", lineType="wrap"):
        """ Add a text item to the textItems list of messages. """
        self.__check_text_box_valid(setupName, boxName)

        if self.boxSetup[setupName]["boxes"][boxName]["visable"] == False:
            raise Exception(f"Can not add text item to an invisable box.")

        attributes = self.merge_attributes(attributes)

        if lineType not in self.LINE_TYPE:
            raise Exception(f"Line type {lineType} does not exist.")

        self.boxSetup[setupName]["boxes"][boxName]["prevTextItemsLength"] = \
                len(self.boxSetup[setupName]["boxes"][boxName]["textItems"])

        self.boxSetup[setupName]["boxes"][boxName]["textItems"].append([message, attributes, self.LINE_TYPE[lineType]])


    ###################################################################################################################
    # UPDATE FUNCTIONS                                                                                                #
    ###################################################################################################################

    def update(self):
        """ Updates all. """
        # Used to verify that prompt/box sizes doesn't become smaller than min size.
        self.edgeConditions = list()

        self.hTerminal, self.wTerminal = self.screen.getmaxyx() # Get the terminal size

        # Update the prompt variables (prompt size)
        self.update_prompt_variables(False)

        # Update box variables (box sizes)
        self.update_box_variables(False)

        # Update edge conditions
        self.update_box_edge_condition()

        if self.updateConditionsSatisfied and self.resizeDone:
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

            # Update boxes scrolls
            self.update_boxes_scrolls()

            # Update the visual cursor
            self.update_visual_cursor()
        elif not self.updateConditionsSatisfied and self.resizeDone:
            self.screen.addstr(0,0, "Terminal too small.")

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
            # Update prev variables
            attr["prevBoxWidth"] = attr["boxWidth"]
            attr["prevHeight"] = attr["boxHeight"]

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

            if attr["visable"] == False:
                self.edgeConditions.append(attr["boxWidth"] >= (self.BOX_MIN_WIDTH + 2 * attr["wTextIndent"]))
                self.edgeConditions.append(attr["boxHeight"] >= (self.BOX_MIN_HEIGHT + 2 * attr["hTextIndent"]))

        self.updateConditionsSatisfied = all(condition == True for condition in self.edgeConditions)

        self.promptLineWidth = self.wTerminal - (len(self.promptSign) + 1)


    def update_box_edge_condition(self):
        """  """
        boxesMinWidth = 0
        boxesMinHeight = self.BOX_MIN_HEIGHT
        for name, attr in self.boxSetup[self.activeBoxSetup]["boxes"].items():
            if attr["fixedWidth"] == None:
                boxesMinWidth += (self.BOX_MIN_WIDTH + 2 * attr["wTextIndent"]) if attr["visable"] else 0
            else:
                boxesMinWidth += attr["boxWidth"] if attr["visable"] else 0

            if attr["fixedHeight"] != None:
                if attr["boxHeight"] > boxesMinHeight:
                    boxesMinHeight = attr["boxHeight"]

        self.edgeConditions.append(self.wTerminal >= boxesMinWidth)
        self.edgeConditions.append(self.hTerminal >= (boxesMinHeight + self.INFO_PROMPT_MIN_HEIGHT + self.PROMPT_MIN_HEIGHT))

        self.updateConditionsSatisfied = all(condition == True for condition in self.edgeConditions)


    def update_text_wrapping(self):
        """ Update text format by re-wrapping text to match new box sizes """
        for name, attr in self.boxSetup[self.activeBoxSetup]["boxes"].items():
            if attr["visable"] == False:
                continue

            if not (attr["boxWidth"] != attr["prevBoxWidth"] or \
                    attr["boxHeight"] != attr["prevBoxHeight"] or \
                    len(attr["textItems"]) != attr["prevTextItemsLength"]):
                continue

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

            style = self.get_box_frame_char_dict(self.activeBoxSetup, name)

            if name == self.boxSetup[self.activeBoxSetup]["focusedBox"] and self.debug:
                self.screen.addstr(boxTLY + 1, boxBRX - 1, "*", curses.color_pair(CHAR_COLOR["red"]))

            for row in range(self.hTerminal):
                for column in range(self.wTerminal):
                    # DEBUG BOX ON THE TOP OF EVERY BOX
                    if (boxTLY + 2) == row and boxTLX == column and self.debug and \
                            self.debugBoxPlacementShow == self.debugBoxPlacement["Top"]:
                        self.screen.addstr(row, column, style["verticalRight"], attr["frameAttr"])
                    elif (boxTLY + 2) == row and boxBRX == column and self.debug and \
                            self.debugBoxPlacementShow == self.debugBoxPlacement["Top"]:
                        self.screen.addstr(row, column, style["verticalLeft"], attr["frameAttr"])
                    elif (boxTLY + 2) == row and boxTLX < column and boxBRX > column and self.debug and \
                            self.debugBoxPlacementShow == self.debugBoxPlacement["Top"]:
                        self.screen.addstr(row, column, style["horizontal"], attr["frameAttr"])

                    # DEBUG BOX ON THE BOTTOM OF EVERY BOX
                    elif (boxBRY - 2) == row and boxTLX == column and self.debug and \
                            self.debugBoxPlacementShow == self.debugBoxPlacement["Bottom"]:
                        self.screen.addstr(row, column, style["verticalRight"], attr["frameAttr"])
                    elif (boxBRY - 2) == row and boxBRX == column and self.debug and \
                            self.debugBoxPlacementShow == self.debugBoxPlacement["Bottom"]:
                        self.screen.addstr(row, column, style["verticalLeft"], attr["frameAttr"])
                    elif (boxBRY - 2) == row and boxTLX < column and boxBRX > column and self.debug \
                            and self.debugBoxPlacementShow == self.debugBoxPlacement["Bottom"]:
                        self.screen.addstr(row, column, style["horizontal"], attr["frameAttr"])

                    # NORMAL BOX FRAME
                    elif boxTLY == row and boxTLX == column:
                        self.screen.addstr(row, column, style["rightDown"], attr["frameAttr"])
                    elif boxTLY == row and boxBRX == column:
                        self.screen.addstr(row, column, style["leftDown"], attr["frameAttr"])
                    elif boxBRY == row and boxTLX == column:
                        self.screen.addstr(row, column, style["rightUp"], attr["frameAttr"])
                    elif boxBRY == row and boxBRX == column:
                        self.screen.addstr(row, column, style["leftUp"], attr["frameAttr"])
                    elif (boxTLY == row or boxBRY == row) and boxTLX < column and boxBRX > column:
                        self.screen.addstr(row, column, style["horizontal"], attr["frameAttr"])
                    elif boxTLY < row and boxBRY > row and (boxTLX == column or boxBRX == column):
                        self.screen.addstr(row, column, style["vertical"], attr["frameAttr"])

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
            if attr["visable"] == False:
                continue

            displayedText = list()
            if len(attr["lines"]) >= attr["textHeight"]:
                displayedText = attr["lines"][-attr["textHeight"] + attr["scrollIndex"]:][:attr["textHeight"]]
            else:
                displayedText = attr["lines"]

            for i, line in enumerate(displayedText):
                self.screen.addstr(attr["textStartY"] + i, attr["textStartX"], line[0], line[1])


    def update_boxes_scrolls(self):
        """  """
        for name, attr in self.boxSetup[self.activeBoxSetup]["boxes"].items():
            if attr["visable"] == False:
                continue

            if not attr["scrollVisable"]:
                continue

            scrollBoundary = attr["textHeight"] + (attr["hTextIndent"] * 2)

            if len(attr["lines"]) >= attr["textHeight"]:
                boundaryStart = attr["textStartY"] - attr["hTextIndent"]
                boundaryEnd = attr["textStartY"] + attr["textHeight"] + attr["hTextIndent"]

                below = -attr["scrollIndex"] if attr["scrollIndex"] < 0 else 0
                above = len(attr["lines"]) - (below + attr["textHeight"])

                startY = int(scrollBoundary * (above / len(attr["lines"]))) + boundaryStart
                endY = boundaryEnd - int(scrollBoundary * (below / len(attr["lines"])))

                for row in range(startY, endY):
                    self.screen.addstr(row, attr["bottomRight"]["x"], attr["scrollChar"], attr["frameAttr"])


    def update_visual_cursor(self):
        """ Update the visual cursor in the prompt. """
        self.screen.move(self.hTerminal - self.promptHeight, self.promptVCursorPos + len(self.promptSign))


    def update_boxes_frame_attr(self):
        """  """
        for setupName, setupAttr in self.boxSetup.items():
            for boxName, boxAttr in setupAttr["boxes"].items():
                boxAttr["frameAttr"] = self.merge_attributes(boxAttr["frameAttrUnmerged"])


    ###################################################################################################################
    # GET/SET FUNCTIONS                                                                                               #
    ###################################################################################################################

    def set_active_box_setup(self, setupName):
        """  """
        self.__check_box_setup_valid(setupName)

        self.activeBoxSetup = setupName


    def set_focus_box(self, setupName, boxName):
        """ Set a box in focus i.e. make it scrollable. """
        self.__check_text_box_valid(setupName, boxName)

        if self.boxSetup[setupName]["boxes"][boxName]["visable"] == False:
            raise Exception(f"Can not set focus on an invisible box.")

        self.boxSetup[setupName]["focusedBox"] = boxName


    def set_box_scroll_visable(self, setupName, boxName, value):
        """  """
        self.__check_text_box_valid(setupName, boxName)

        self.boxSetup[setupName]["boxes"][boxName]["scrollVisable"] = value


    def set_box_frame_char(self, setupName, boxName, char):
        """  """
        self.__check_text_box_valid(setupName, boxName)

        if not isinstance(char, str):
            raise Exception("char is not of string type.")
        if char not in FRAME_STYLE:
            raise Exception(f"{char} not in FRAME_STYLE.")

        self.boxSetup[setupName]["boxes"][boxName]["frameChar"] = char


    def get_box_frame_char_dict(self, setupName, boxName):
        """  """
        self.__check_text_box_valid(setupName, boxName)

        style = self.boxSetup[setupName]["boxes"][boxName]["frameChar"]

        frame = {
            "vertical"              : FRAME_STYLE[style][0],
            "verticalLeft"          : FRAME_STYLE[style][1],
            "verticalRight"         : FRAME_STYLE[style][2],
            "horizontal"            : FRAME_STYLE[style][3],
            "horizontalUp"          : FRAME_STYLE[style][4],
            "horizontalDown"        : FRAME_STYLE[style][5],
            "leftUp"                : FRAME_STYLE[style][6],
            "leftDown"              : FRAME_STYLE[style][7],
            "rightUp"               : FRAME_STYLE[style][8],
            "rightDown"             : FRAME_STYLE[style][9],
            "cross"                 : FRAME_STYLE[style][10]
        }

        return frame


    def set_box_frame_attr(self, setupName, boxName, attributes):
        """  """
        self.__check_text_box_valid(setupName, boxName)

        self.boxSetup[setupName]["boxes"][boxName]["frameAttrUnmerged"] = attributes


    ###################################################################################################################
    # KEY HANDLER FUNCTION                                                                                            #
    ###################################################################################################################

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

                if self.resizeDone:
                    self.screen.clear()

                self.resizeDone = False
                self.resizeTimer.cancel()
                self.resizeTimer = threading.Timer(.1, self.resize_timeout)
                self.resizeTimer.start()


            # PROMPT KEY EVENTS ---------------------------------------------------------------------------------------
            elif char == 260:                   # <ARROW-LEFT> KEY (Scroll left)
                if self.promptVCursorPos != 0:
                    self.promptVCursorPos -= 1
                if self.promptCursorPos != 0:
                    self.promptCursorPos -= 1

                if self.resizeDone:
                    self.update_prompt()
                    self.update_visual_cursor()
                    continue

            elif char == 261:                   # <ARROW-RIGHT> KEY (Scroll right)
                if self.promptVCursorPos < len(self.promptString) and \
                   self.promptVCursorPos != self.promptLineWidth:
                    self.promptVCursorPos += 1
                if self.promptCursorPos < len(self.promptString):
                    self.promptCursorPos += 1

                if self.resizeDone:
                    self.update_prompt()
                    self.update_visual_cursor()
                    continue

            elif char == 262:                   # HOME KEY
                self.promptVCursorPos = 0
                self.promptCursorPos = 0

                if self.resizeDone:
                    self.update_prompt()
                    self.update_visual_cursor()
                    continue

            elif char == 358 or char == 360:    # END KEY
                if len(self.promptString) >= self.promptLineWidth:
                    self.promptVCursorPos = self.promptLineWidth
                else:
                    self.promptVCursorPos = len(self.promptString)
                self.promptCursorPos = len(self.promptString)

                if self.resizeDone:
                    self.update_prompt()
                    self.update_visual_cursor()
                    continue

            elif char == 330:                   # DELETE KEY
                self.promptString = self.promptString[:self.promptCursorPos] + \
                    self.promptString[self.promptCursorPos:][1:]

                if len(self.promptString) >= self.promptLineWidth:
                    if len(self.promptString) == (self.promptVRightPos - 1) and \
                       self.promptVCursorPos != self.promptLineWidth:
                        self.promptVCursorPos += 1

                if self.resizeDone:
                    self.update_prompt()
                    self.update_visual_cursor()
                    continue

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

                if self.resizeDone:
                    self.update_prompt()
                    self.update_visual_cursor()
                    continue

            elif char == "\x16":                # CTRL + V (paste)
                copy = self.get_clipboard()
                if copy != None and copy != False:
                    self.promptString = self.promptString[:self.promptCursorPos] + copy + self.promptString[self.promptCursorPos:]
                    self.promptCursorPos += len(copy)
                    if (self.promptVCursorPos + len(copy)) >= self.promptLineWidth:
                        self.promptVCursorPos = self.promptLineWidth
                    else:
                        self.promptVCursorPos += len(copy)

                if self.resizeDone:
                    self.update_prompt()
                    self.update_visual_cursor()
                    continue

            elif char == "\n": # <ENTER>
                if self.promptString != "":
                    self.promptCallbackFunction(self.promptString)
                self.promptString = ""
                self.promptCursorPos = 0
                self.promptVCursorPos = 0
                # TEMP
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

                if self.resizeDone:
                    self.update_prompt()
                    self.update_visual_cursor()
                    continue

            self.update()

        curses.endwin() # Close curses terminal


    ###################################################################################################################
    # OTHER FUNCTIONS                                                                                                 #
    ###################################################################################################################

    def init_colors(self):
        """ Init curses colors. """
        curses.start_color()
        curses.use_default_colors()

        for color, value in CHAR_COLOR.items():
            curses.init_pair(value, value - 1, -1)


    def __init_box_default_parameters(self, setupName, boxName):
        """  """
        self.boxSetup[setupName]["boxes"][boxName] = dict()
        self.boxSetup[setupName]["focusedBox"] = boxName

        self.boxSetup[setupName]["boxes"][boxName]["fixedWidth"] = None
        self.boxSetup[setupName]["boxes"][boxName]["fixedHeight"] = None
        self.boxSetup[setupName]["boxes"][boxName]["hOrient"] = self.H_ORIENT["Left"]
        self.boxSetup[setupName]["boxes"][boxName]["vOrient"] = self.V_ORIENT["Up"]
        self.boxSetup[setupName]["boxes"][boxName]["visable"] = True
        self.boxSetup[setupName]["boxes"][boxName]["wTextIndent"] = 0
        self.boxSetup[setupName]["boxes"][boxName]["hTextIndent"] = 0
        self.boxSetup[setupName]["boxes"][boxName]["boxWidth"] = None
        self.boxSetup[setupName]["boxes"][boxName]["boxHeight"] = None
        self.boxSetup[setupName]["boxes"][boxName]["prevBoxWidth"] = None
        self.boxSetup[setupName]["boxes"][boxName]["prevBoxHeight"] = None
        self.boxSetup[setupName]["boxes"][boxName]["textWidth"] = None
        self.boxSetup[setupName]["boxes"][boxName]["textHeight"] = None
        self.boxSetup[setupName]["boxes"][boxName]["topLeft"] = None
        self.boxSetup[setupName]["boxes"][boxName]["bottomRight"] = None
        self.boxSetup[setupName]["boxes"][boxName]["textStartX"] = 0
        self.boxSetup[setupName]["boxes"][boxName]["textStartY"] = 0
        self.boxSetup[setupName]["boxes"][boxName]["frameAttrUnmerged"] = "white"
        self.boxSetup[setupName]["boxes"][boxName]["frameAttr"] = None
        self.boxSetup[setupName]["boxes"][boxName]["frameChar"] = "singleLine"

        self.boxSetup[setupName]["boxes"][boxName]["textItems"] = list()
        self.boxSetup[setupName]["boxes"][boxName]["prevTextItemsLength"] = 0
        self.boxSetup[setupName]["boxes"][boxName]["lines"] = list()
        self.boxSetup[setupName]["boxes"][boxName]["scrollIndex"] = 0

        self.boxSetup[setupName]["boxes"][boxName]["scrollVisable"] = True
        self.boxSetup[setupName]["boxes"][boxName]["scrollChar"] = "█"


    def reset_info_prompt(self):
        """  """
        startOfInfoPromptX = 0
        startOfInfoPromptY = self.hTerminal - 1 - self.promptHeight
        bg = self.merge_attributes(self.infoPromptBgAttr)
        self.screen.addstr(startOfInfoPromptY, startOfInfoPromptX, self.wTerminal * self.infoPromptBg, bg)


    def get_clipboard(self):
        """ Get system clipboard. """
        clipboard = None

        if self.platform in self.platform_windows:
            win32clipboard.OpenClipboard()
            clipboard = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

        elif self.platform in self.platform_linux:
            pass
        elif self.platform in self.platform_mac:
            pass
        else:
            return False

        return clipboard


    def __info_prompt_text_timeout(self):
        """  """
        self.infoPromptActive = False
        self.reset_info_prompt()
        self.update_visual_cursor()
        self.screen.refresh()


    def resize_timeout(self):
        """  """
        self.resizeDone = True
        self.screen.clear()
        self.screen.refresh()
        self.update()


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
            if item in CHAR_COLOR:
                merged = merged | curses.color_pair(CHAR_COLOR[item])
            elif item in CHAR_ATTR:
                merged = merged | CHAR_ATTR[item]
            else:
                raise Exception(f"Attribute {item} is not available.")

        return merged


    def __check_box_setup_valid(self, setupName, shouldExist=True):
        """ Check to see if the given setupBox exist or does not exist in the self.boxSetup dict. """
        if not isinstance(setupName, str):
            raise Exception("setupName is not of string type.")

        if shouldExist:
            if setupName not in self.boxSetup:
                raise Exception(f"Box setup {name} does not exist.")
        else:
            if setupName in self.boxSetup:
                raise Exception(f"Box setup {name} already exist.")


    def __check_text_box_valid(self, setupName, boxName, shouldExist=True):
        """ Check to see if the given boxName exist or does not exist in the fiven setupName dict. """
        self.__check_box_setup_valid(setupName)

        if not isinstance(boxName, str):
            raise Exception("name is not of string type.")

        if shouldExist:
            if boxName not in self.boxSetup[setupName]["boxes"]:
                raise Exception(f"TextBox {boxName} does not exist.")
        else:
            if boxName in self.boxSetup[setupName]["boxes"]:
                raise Exception(f"TextBox {boxName} already exist.")








class TestTextBox():
    """  """

    def __init__(self):
        """  """
        self.tb = TerminalTextBoxes(self.test_callback)
        self.tb.create_text_box_setup("setup")

        self.tb.create_text_box("setup", "text", frameAttr="green", wTextIndent=1)
        self.tb.create_text_box("setup", "info", 20, frameAttr="red", hOrient=self.tb.H_ORIENT["Right"])

        self.tb.set_focus_box("setup", "text")

        self.tb.start()

    def test_callback(self, message):
        """  """
        if message.startswith("!note"):
            message = message.replace("!note", "NOTE:")
            self.tb.infoPromptTextAttr = ["yellow", "bold"]
            self.tb.set_info_prompt_message(message, 5000)
        elif message.startswith("!error"):
            message = message.replace("!error", "ERROR:")
            self.tb.infoPromptTextAttr = ["red", "bold"]
            self.tb.set_info_prompt_message(message, 5000)
        else:
            self.tb.infoPromptTextAttr = ["white"]
            self.tb.add_text_item("setup", "text", message, attributes=["yellow", "bold"])


if __name__ == "__main__":
    ttb = TestTextBox()
