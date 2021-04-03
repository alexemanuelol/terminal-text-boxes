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

# Operating system
PLATFORM = sys.platform
PLATFORM_LINUX = ["linux", "linux2"]
PLATFORM_WINDOWS = ["Windows", "win32", "cygwin"]
PLATFORM_MAC = ["Mac", "darwin", "os2", "os2emx"]

# Char color
CHAR_COLOR = {
    "black"                 : 1 if PLATFORM in PLATFORM_LINUX else 1,
    "blue"                  : 5 if PLATFORM in PLATFORM_LINUX else 2,
    "green"                 : 3 if PLATFORM in PLATFORM_LINUX else 3,
    "cyan"                  : 7 if PLATFORM in PLATFORM_LINUX else 4,
    "red"                   : 2 if PLATFORM in PLATFORM_LINUX else 5,
    "magenta"               : 6 if PLATFORM in PLATFORM_LINUX else 6,
    "yellow"                : 4 if PLATFORM in PLATFORM_LINUX else 7,
    "white"                 : 8 if PLATFORM in PLATFORM_LINUX else 8,
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

# wrap if the text item can wrap, single if text item only should be displayed on a single line
LINE_TYPE = {
    "wrap"                  : 0,
    "single"                : 1
}

# Orientations
H_ORIENT = {
    "Left"                  : 0,
    "Right"                 : 1
}
V_ORIENT = {
    "Up"                    : 0,
    "Down"                  : 1
}

# Debug variables
DBG_BOX_PLACEMENT = {
    "Top"                   : 0,
    "Bottom"                : 1
}
DBG_BOX_INFO = {
    "name"                  : 0,
    "textSize"              : 1,
    "boxSize"               : 2
}



class TerminalTextBoxes():
    """ Terminal Text Boxes Class. """

    def __init__(self, charCallback=None, enterCallback=None):
        """ Init. """
        self.__fakeKeyboard = Controller()

        self.__isActive = False

        # Prompt callback function
        self.__promptCharCallbackFunction = charCallback
        self.__promptEnterCallbackFunction = enterCallback

        self.__FRAME_SIZE = 1

        # Resize variables
        self.__resizeDone               = True
        self.__resizeTimer              = threading.Timer(.1, self.__resize_timeout)

        # Terminal Box Setups
        self.__boxSetup                 = dict()
        self.__activeBoxSetup           = None

        # Prompt variables
        self.__promptSign               = "> "
        self.__promptSignSize           = len(self.__promptSign)
        self.__promptWidth              = None # Will be the same as self.__wTerminal
        self.__promptHeight             = 1
        self.__promptLineWidth          = None # Will be self.__wTerminal - (self.__promptSignSize + 1)
        self.__promptString             = ""
        self.__promptCursorPos          = 0
        self.__promptVCursorPos         = 0
        self.__promptVLeftPos           = 0
        self.__promptVRightPos          = 0

        # Prompt info box
        self.__infoPromptChar           = "═"
        self.__infoPromptCharAttr       = "white"
        self.__infoPromptTextAttr       = "yellow"
        self.__infoPromptHeight         = 1
        self.__infoPromptCurrMessage    = ""
        self.__infoPromptActive         = False
        self.__infoPromptTextIndent     = 3
        self.__infoPromptTimer          = threading.Timer(5, self.__reset_info_prompt)

        # Minimum sizes
        self.__PROMPT_MIN_WIDTH         = self.__promptSignSize + 10
        self.__PROMPT_MIN_HEIGHT        = self.__promptHeight
        self.__INFO_PROMPT_MIN_WIDTH    = self.__infoPromptTextIndent * 2 + (2 + 5)
        self.__INFO_PROMPT_MIN_HEIGHT   = self.__infoPromptHeight
        self.__BOX_MIN_WIDTH            = (self.__FRAME_SIZE * 2) + 1
        self.__BOX_MIN_HEIGHT           = (self.__FRAME_SIZE * 2) + 1

        self.debug                      = True
        self.dbgBoxPlacementShow        = 0
        self.dbgBoxInfoShow             = 0


    ###################################################################################################################
    # PUBLIC FUNCTIONS                                                                                                #
    ###################################################################################################################

    def start(self):
        """ Start displaying the terminal text boxes module. """
        # Terminal window initialization
        if not self.__boxSetup:
            raise Exception("There are no setups created.")
        if len(self.__boxSetup[self.__activeBoxSetup]["boxes"]) == 0:
            raise Exception("There are no boxes in the active box setup.")

        self.__isActive = True

        self.__screen = curses.initscr()
        self.__screen.keypad(True)
        curses.noecho()

        self.__init_colors()

        self.__update_boxes_frame_attr()

        self.update()

        event = threading.Event()
        thread = threading.Thread(target=self.__key_handler, args=(event,))
        thread.start()


    def stop(self):
        """ Stop displaying the terminal text boxes module. """
        self.__isActive = False

        self.__fakeKeyboard.press(Key.esc)


    def create_text_box_setup(self, setupName):
        """ Creates a new 'text box setup' in which you can add text boxes to.
            Arguments:
                setupName           - The name of the box setup.        (str)
        """
        self.__check_box_setup_valid(setupName, False)

        self.__boxSetup[setupName]                  = dict()
        self.__boxSetup[setupName]["boxes"]         = dict()
        self.__boxSetup[setupName]["boxOrder"]      = list()
        self.__boxSetup[setupName]["focusedBox"]    = None

        self.__activeBoxSetup = setupName


    def remove_text_box_setup(self, setupName):
        """ Removes a 'text box setup'.
            Arguments:
                setupName           - The name of the box setup.        (str)
        """
        self.__check_box_setup_valid(setupName)

        self.__boxSetup.pop(setupName)

        if len(self.__boxSetup) == 0:
            self.__activeBoxSetup = None
            raise Exception("No more box setups left.")
        else:
            self.__activeBoxSetup = next(iter(self.__boxSetup))


    def create_text_box(self, setupName, boxName, width=None, height=None, hPos=None, vPos=0, hOrient=0, vOrient=0,
                        visable=True, wTextIndent=0, hTextIndent=0, frameChar="singleLine", frameAttr="white",
                        scrollVisable=True):
        """ Creates a text box inside the given text box setup.
            Arguments:
                setupName           - The name of the box setup.                                    (str)
                boxName             - The name of the text box.                                     (str)
                width               - Width of the text box (None if width is not fixed size).      (int)
                height              - Height of the text box (None if height is not fixed size).    (int)
                hPos                - Where this box should be placed horizontally.                 (int)
                vPos                - Where this box should be placed vertically.                   (int)
                hOrient             - Horizontal orientation of the box (0 : Left, 1 : Right).      (int)
                vOrient             - Vertical orientation of the box (0 : Up, 1 : Down).           (int)
                visable             - Should the box be visable or not? (Padding box?).             (bool)
                wTextIndent         - Width indentation of the text in the box.                     (int)
                hTextIndent         - Height indentation of the text in the box.                    (int)
                frameChar           - What frame style should be used (check FRAME_STYLE dict).     (str)
                frameAttr           - What frame attributes should be used (color, text format).    (str/list)
                scrollVisable       - Should the scrollbar be visable or not.                       (bool)
        """
        self.__check_text_box_valid(setupName, boxName, False)
        self.__init_box_default_parameters(setupName, boxName)

        if width != None:
            self.__is_type(width, int)
        if width != None and width < self.__BOX_MIN_WIDTH:
            raise Exception(f"width is too small, must be bigger than or equal to {self.__BOX_MIN_WIDTH}")
        if width != None and width < (self.__BOX_MIN_WIDTH + 2 * wTextIndent):
            raise Exception(f"width is too small, must be bigger than or equal to {self.__BOX_MIN_WIDTH + 2 * wTextIndent}")
        self.__boxSetup[setupName]["boxes"][boxName]["fixedWidth"] = width

        if height != None:
            self.__is_type(height, int)
        if height != None and height < self.__BOX_MIN_HEIGHT:
            raise Exception(f"height is too small, must be bigger than or equal to {self.__BOX_MIN_HEIGHT}")
        if height != None and height < (self.__BOX_MIN_HEIGHT + 2 * hTextIndent):
            raise Exception(f"height is too small, must be bigger than or equal to {self.__BOX_MIN_HEIGHT + 2 * hTextIndent}")
        self.__boxSetup[setupName]["boxes"][boxName]["fixedHeight"] = height

        if not isinstance(hOrient, int) or hOrient not in H_ORIENT.values():
            raise Exception("hOrient is not of integer type or not within acceptable range.")
        self.__boxSetup[setupName]["boxes"][boxName]["hOrient"] = hOrient

        if not isinstance(vOrient, int) or vOrient not in V_ORIENT.values():
            raise Exception("vOrient is not of integer type or not within acceptable range.")
        self.__boxSetup[setupName]["boxes"][boxName]["vOrient"] = vOrient

        if hPos != None:
            self.__is_type(hPos, int)
            self.__boxSetup[setupName]["boxOrder"].insert(hPos, boxName)

            if self.__boxSetup[setupName]["boxOrder"].index(boxName) > 0:
                prevBoxIndex = self.__boxSetup[setupName]["boxOrder"].index(boxName) - 1
            else:
                prevBoxIndex = 0

            self.__boxSetup[setupName]["boxes"][boxName]["hOrient"] = \
                    self.__boxSetup[setupName]["boxes"][self.__boxSetup[setupName]["boxOrder"][prevBoxIndex]]["hOrient"]

            # TODO: fix vPos as well, check how big list is? (How deep vertical is)
        elif hOrient == H_ORIENT["Left"]:
            self.__boxSetup[setupName]["boxOrder"].insert(0, boxName)
        elif hOrient == H_ORIENT["Right"]:
            self.__boxSetup[setupName]["boxOrder"].append(boxName)
        else:
            self.__boxSetup[setupName]["boxOrder"].append(boxName)
        # Sort dict according to boxOrder
        self.__boxSetup[setupName]["boxes"] = \
                {key : self.__boxSetup[setupName]["boxes"][key] for key in self.__boxSetup[setupName]["boxOrder"]}

        self.__is_type(visable, bool)
        self.__boxSetup[setupName]["boxes"][boxName]["visable"] = visable

        self.__is_type(wTextIndent, int)
        self.__is_type(hTextIndent, int)
        self.__boxSetup[setupName]["boxes"][boxName]["wTextIndent"] = wTextIndent
        self.__boxSetup[setupName]["boxes"][boxName]["hTextIndent"] = hTextIndent
        self.__boxSetup[setupName]["boxes"][boxName]["frameChar"] = frameChar
        self.__boxSetup[setupName]["boxes"][boxName]["frameAttrUnmerged"] = frameAttr
        self.__boxSetup[setupName]["boxes"][boxName]["scrollVisable"] = scrollVisable


    def remove_text_box(self, setupName, boxName):
        """ Removes a text box inside the given text box setup.
            Arguments:
                setupName           - The name of the box setup.    (str)
                boxName             - The name of the text box.     (str)
        """
        self.__check_text_box_valid(setupName, boxName)

        self.__boxSetup[setupName]["boxes"].pop(boxName)

        if len(self.__boxSetup[setupName]["boxes"]) == 0:
            self.__boxSetup[setupName]["focusedBox"]= None
            raise Exception("No more text boxes left in the setup.")
        else:
            self.__boxSetup[setupName]["focusedBox"]= next(iter(self.__boxSetup[setupName]["boxes"]))# }}}


    def set_info_prompt_message(self, text, timeout=None):
        """ Sets info message above the prompt.
            Arguments:
                text                - The text to be set in the info prompt.            (str)
                timeout             - Timeout before message disappears (ms).           (int)
        """
        self.__is_type(text, str)
        self.__reset_info_prompt()

        infoPromptY = self.__hTerminal - 1 - self.__promptHeight
        textStartX = self.__infoPromptTextIndent + 1
        textMaxLen = self.__wTerminal - (self.__infoPromptTextIndent * 2) - 2
        textEndX = textStartX + len(text[:textMaxLen])

        self.__infoPromptCurrMessage = text
        bgAttr = self.__merge_attributes(self.__infoPromptCharAttr)
        textAttr = self.__merge_attributes(self.__infoPromptTextAttr)

        self.__screen.addstr(infoPromptY, self.__infoPromptTextIndent," ", bgAttr)
        self.__screen.addstr(infoPromptY, textStartX, text[:textMaxLen], textAttr)
        self.__screen.addstr(infoPromptY, textEndX," ", bgAttr)

        if timeout != None:
            self.__infoPromptTimer.cancel()
            self.__infoPromptTimer = threading.Timer(timeout//1000, self.__info_prompt_text_timeout)
            self.__infoPromptTimer.start()
            self.__infoPromptActive = True
        self.__screen.refresh()


    def add_text_item(self, setupName, boxName, text, attributes="white", lineType="wrap"):
        """ Adds a text item to the textItems list of the given text box.
            Arguments:
                setupName           - The name of the box setup.        (str)
                boxName             - The name of the text box.         (str)
                text                - The text to be added.             (str)
                attributes          - The text attributes.              (str/list)
                lineType            - The line type (wrap/single).      (str)
        """
        self.__check_text_box_valid(setupName, boxName)

        if self.__boxSetup[setupName]["boxes"][boxName]["visable"] == False:
            raise Exception(f"Can not add text item to an invisable box.")

        attributes = self.__merge_attributes(attributes)

        if lineType not in LINE_TYPE:
            raise Exception(f"Line type {lineType} does not exist.")

        self.__boxSetup[setupName]["boxes"][boxName]["prevTextItemsLength"] = \
                len(self.__boxSetup[setupName]["boxes"][boxName]["textItems"])

        self.__boxSetup[setupName]["boxes"][boxName]["textItems"].append([text, attributes, LINE_TYPE[lineType]])


    def remove_text_item(self, setupName, boxName, index):
        """ Removes a text item from the textItems list of the given text box.
            Arguments:
                setupName           - The name of the box setup.            (str)
                boxName             - The name of the text box.             (str)
                index               - The index of the item to be removed.  (int)
        """
        self.__check_text_box_valid(setupName, boxName)

        length = len(self.__boxSetup[setupName]["boxes"][boxName]["textItems"])

        if index >= length or index <= (-length):
            raise Exception("index is out of boundary of textItems.")

        del self.__boxSetup[setupName]["boxes"][boxName]["textItems"][index]


    def clear_text_items(self, setupName, boxName):
        """ Clears the entire textItems list from a given text box.
            Arguments:
                setupName           - The name of the box setup.            (str)
                boxName             - The name of the text box.             (str)
        """
        self.__check_text_box_valid(setupName, boxName)

        self.__boxSetup[setupName]["boxes"][boxName]["textItems"] = list()


    ###################################################################################################################
    # UPDATE FUNCTIONS                                                                                                #
    ###################################################################################################################

    def update(self):
        """ Updates all. """
        # Used to verify that prompt/box sizes doesn't become smaller than min size.
        self.__edgeConditions = list()

        self.__hTerminal, self.__wTerminal = self.__screen.getmaxyx() # Get the terminal size

        # Update the prompt variables (prompt size)
        self.__update_prompt_variables(False)

        # Update box variables (box sizes)
        self.__update_box_variables(False)

        # Update edge conditions
        self.__update_box_edge_conditions()

        if self.__updateConditionsSatisfied and self.__resizeDone:
            # Update text format by re-wrapping text to match new box sizes
            self.__update_text_wrapping()

            # Clear the screen
            self.__screen.clear()

            # Update all the boxes frames
            self.__update_box_frames()

            # Update prompt
            self.__update_prompt()

            # Update all boxes
            self.__update_boxes()

            # Update boxes scrolls
            self.__update_boxes_scrolls()

            # Update the visual cursor
            self.__update_visual_cursor()
        elif not self.__updateConditionsSatisfied and self.__resizeDone:
            self.__screen.addstr(0,0, "Terminal too small.")

        self.__screen.refresh()


    def __update_prompt_variables(self, updateTerminal=True):
        """ Updates prompt variables.
            Arguments:
                updateTerminal          - Should terminal width/height be updated.      (bool)
        """
        if updateTerminal:
            self.__hTerminal, self.__wTerminal = self.__screen.getmaxyx() # Get the terminal size

        self.__promptWidth = self.__wTerminal
        self.__promptLineWidth = self.__wTerminal - (self.__promptSignSize + 1)

        # Edge conditions
        self.__edgeConditions.append(self.__wTerminal >= self.__PROMPT_MIN_WIDTH)
        self.__edgeConditions.append(self.__hTerminal >= self.__PROMPT_MIN_HEIGHT)
        self.__edgeConditions.append(self.__wTerminal >= self.__INFO_PROMPT_MIN_WIDTH)
        self.__edgeConditions.append(self.__hTerminal >= self.__INFO_PROMPT_MIN_HEIGHT)

        self.__updateConditionsSatisfied = all(condition == True for condition in self.__edgeConditions)


    def __update_box_variables(self, updateTerminal=True):
        """ Updates box variables.
            Arguments:
                updateTerminal          - Should terminal width/height be updated.      (bool)
        """
        if updateTerminal:
            self.__hTerminal, self.__wTerminal = self.__screen.getmaxyx() # Get the terminal size

        nbrOfBoxes = len(self.__boxSetup[self.__activeBoxSetup]["boxes"]) # Total amount of current boxes
        nbrOfWUnfixedBoxes = 0      # Number of boxes that does not have fixed width
        nbrOfWFixedBoxes = 0        # Number of boxes that does have fixed width
        wForFixed = 0               # Width of all fixed width boxes together
        for name, attr in self.__boxSetup[self.__activeBoxSetup]["boxes"].items():
            if attr["fixedWidth"] == None:
                nbrOfWUnfixedBoxes = nbrOfWUnfixedBoxes + 1
            else:
                nbrOfWFixedBoxes = nbrOfWFixedBoxes + 1
                wForFixed = wForFixed + attr["fixedWidth"]

        wForUnfixed = 0             # Width of all unfixed width boxes in total
        wForUnused = 0              # Remaining unused width
        if nbrOfWUnfixedBoxes > 0 and nbrOfWFixedBoxes > 0:     # Fixed and Unfixed boxes
            wForUnused = 0
            wForUnfixed = self.__wTerminal - wForFixed
        elif nbrOfWUnfixedBoxes > 0 and nbrOfWFixedBoxes == 0:  # Unfixed boxes
            wForUnused = 0
            wForUnfixed = self.__wTerminal
        elif nbrOfWUnfixedBoxes == 0 and nbrOfWFixedBoxes > 0:  # Fixed boxes
            wForUnused = self.__wTerminal - wForFixed
            wForUnfixed = 0

        # Remaining width that is uneven between the none fixed width boxes.
        # This will be distributed between the wForUnfixed boxes till remainingUnevenWidth == 0
        remainingUnevenWidth = wForUnfixed % (nbrOfWUnfixedBoxes if nbrOfWUnfixedBoxes > 0 else 1)

        wIndex = 0
        hIndex = 0
        wForUnusedUsed = False
        hForUnusedUsed = False
        prevVerticalOrientation = None
        for name, attr in self.__boxSetup[self.__activeBoxSetup]["boxes"].items():
            # Update prev variables
            attr["prevBoxWidth"] = attr["boxWidth"]
            attr["prevHeight"] = attr["boxHeight"]

            # Box Width/ Height
            if attr["fixedWidth"] == None:
                attr["boxWidth"] = (wForUnfixed // nbrOfWUnfixedBoxes) + (1 if remainingUnevenWidth > 0 else 0)
                remainingUnevenWidth = (remainingUnevenWidth - 1) if remainingUnevenWidth > 0 else 0
            else:
                attr["boxWidth"] = attr["fixedWidth"]
            if attr["fixedHeight"] == None:
                attr["boxHeight"] = self.__hTerminal - (self.__promptHeight + self.__FRAME_SIZE)
            else:
                attr["boxHeight"] = attr["fixedHeight"]

            # Text Width/ Height
            frameTotalWidth = self.__FRAME_SIZE * 2
            attr["textWidth"] = attr["boxWidth"] - frameTotalWidth - (attr["wTextIndent"] * 2)
            frameTotalHeight = (self.__FRAME_SIZE * 2) + (2 if self.debug else 0)
            attr["textHeight"] = attr["boxHeight"] - frameTotalHeight - (attr["hTextIndent"] * 2)

            # Box orientation horizontal/ vertical
            if attr["hOrient"] == H_ORIENT["Right"] and attr["fixedWidth"] != None and wForUnusedUsed == False:
                wIndex = wIndex + wForUnused
                wForUnusedUsed = True
            if attr["vOrient"] == V_ORIENT["Down"] and attr["fixedHeight"] != None and hForUnusedUsed == False:
                hIndex = hIndex + (self.__hTerminal - (self.__promptHeight + self.__FRAME_SIZE) - attr["boxHeight"])
                hForUnusedUsed = True

            # topLeft point and bottomRight point of the box
            attr["topLeft"] = {"x" : wIndex, "y" : hIndex}
            attr["bottomRight"] = {"x" : wIndex + attr["boxWidth"] - 1, "y" : hIndex + attr["boxHeight"] - 1}

            # Text start/ end positions
            attr["textStartX"] = wIndex + self.__FRAME_SIZE + attr["wTextIndent"]
            if self.debug and self.dbgBoxPlacementShow == DBG_BOX_PLACEMENT["Top"]:
                attr["textStartY"] = hIndex + 2 + self.__FRAME_SIZE + attr["hTextIndent"]
            else:
                attr["textStartY"] = hIndex + self.__FRAME_SIZE + attr["hTextIndent"]

            hIndex = 0
            wIndex = wIndex + attr["boxWidth"]

            if attr["visable"] == False:
                self.__edgeConditions.append(attr["boxWidth"] >= (self.__BOX_MIN_WIDTH + 2 * attr["wTextIndent"]))
                self.__edgeConditions.append(attr["boxHeight"] >= (self.__BOX_MIN_HEIGHT + 2 * attr["hTextIndent"]))

        self.__updateConditionsSatisfied = all(condition == True for condition in self.__edgeConditions)

        self.__promptLineWidth = self.__wTerminal - (len(self.__promptSign) + 1)


    def __update_box_edge_conditions(self):
        """ Updates box edge conditions. """
        boxesMinWidth = 0
        boxesMinHeight = self.__BOX_MIN_HEIGHT
        for name, attr in self.__boxSetup[self.__activeBoxSetup]["boxes"].items():
            if attr["fixedWidth"] == None:
                boxesMinWidth += (self.__BOX_MIN_WIDTH + 2 * attr["wTextIndent"]) if attr["visable"] else 0
            else:
                boxesMinWidth += attr["boxWidth"] if attr["visable"] else 0

            if attr["fixedHeight"] != None:
                if attr["boxHeight"] > boxesMinHeight:
                    boxesMinHeight = attr["boxHeight"]

        self.__edgeConditions.append(self.__wTerminal >= boxesMinWidth)
        self.__edgeConditions.append(self.__hTerminal >= (boxesMinHeight + self.__INFO_PROMPT_MIN_HEIGHT + self.__PROMPT_MIN_HEIGHT))

        self.__updateConditionsSatisfied = all(condition == True for condition in self.__edgeConditions)


    def __update_text_wrapping(self):
        """ Updates the text format by re-wrapping text to match new box sizes. """
        for name, attr in self.__boxSetup[self.__activeBoxSetup]["boxes"].items():
            if attr["visable"] == False:
                continue

            if not (attr["boxWidth"] != attr["prevBoxWidth"] or \
                    attr["boxHeight"] != attr["prevBoxHeight"] or \
                    len(attr["textItems"]) != attr["prevTextItemsLength"]):
                continue

            self.__boxSetup[self.__activeBoxSetup]["boxes"][name]["lines"] = list()
            for item, txtAttr, lineType in attr["textItems"]:
                if lineType == LINE_TYPE["single"]:
                    self.__boxSetup[self.__activeBoxSetup]["boxes"][name]["lines"].append(
                            [item[:attr["textWidth"]], txtAttr])
                else:
                    lines = wrap(item, attr["textWidth"])
                    for line in lines:
                        self.__boxSetup[self.__activeBoxSetup]["boxes"][name]["lines"].append([line, txtAttr])


    def __update_box_frames(self):
        """ Updates the frames for all the boxes as well as the bottom line that separate input bar from boxes. """
        for name, attr in self.__boxSetup[self.__activeBoxSetup]["boxes"].items():
            if attr["visable"] == False:
                continue

            boxTLX = attr["topLeft"]["x"]
            boxTLY = attr["topLeft"]["y"]
            boxBRX = attr["bottomRight"]["x"]
            boxBRY = attr["bottomRight"]["y"]

            style = self.get_box_frame_char_dict(self.__activeBoxSetup, name)

            if name == self.__boxSetup[self.__activeBoxSetup]["focusedBox"] and self.debug:
                self.__screen.addstr(boxTLY + 1, boxBRX - 1, "*", curses.color_pair(CHAR_COLOR["red"]))

            for row in range(self.__hTerminal):
                for column in range(self.__wTerminal):
                    # DEBUG BOX ON THE TOP OF EVERY BOX
                    if (boxTLY + 2) == row and boxTLX == column and self.debug and \
                            self.dbgBoxPlacementShow == DBG_BOX_PLACEMENT["Top"]:
                        self.__screen.addstr(row, column, style["verticalRight"], attr["frameAttr"])
                    elif (boxTLY + 2) == row and boxBRX == column and self.debug and \
                            self.dbgBoxPlacementShow == DBG_BOX_PLACEMENT["Top"]:
                        self.__screen.addstr(row, column, style["verticalLeft"], attr["frameAttr"])
                    elif (boxTLY + 2) == row and boxTLX < column and boxBRX > column and self.debug and \
                            self.dbgBoxPlacementShow == DBG_BOX_PLACEMENT["Top"]:
                        self.__screen.addstr(row, column, style["horizontal"], attr["frameAttr"])

                    # DEBUG BOX ON THE BOTTOM OF EVERY BOX
                    elif (boxBRY - 2) == row and boxTLX == column and self.debug and \
                            self.dbgBoxPlacementShow == DBG_BOX_PLACEMENT["Bottom"]:
                        self.__screen.addstr(row, column, style["verticalRight"], attr["frameAttr"])
                    elif (boxBRY - 2) == row and boxBRX == column and self.debug and \
                            self.dbgBoxPlacementShow == DBG_BOX_PLACEMENT["Bottom"]:
                        self.__screen.addstr(row, column, style["verticalLeft"], attr["frameAttr"])
                    elif (boxBRY - 2) == row and boxTLX < column and boxBRX > column and self.debug \
                            and self.dbgBoxPlacementShow == DBG_BOX_PLACEMENT["Bottom"]:
                        self.__screen.addstr(row, column, style["horizontal"], attr["frameAttr"])

                    # NORMAL BOX FRAME
                    elif boxTLY == row and boxTLX == column:
                        self.__screen.addstr(row, column, style["rightDown"], attr["frameAttr"])
                    elif boxTLY == row and boxBRX == column:
                        self.__screen.addstr(row, column, style["leftDown"], attr["frameAttr"])
                    elif boxBRY == row and boxTLX == column:
                        self.__screen.addstr(row, column, style["rightUp"], attr["frameAttr"])
                    elif boxBRY == row and boxBRX == column:
                        self.__screen.addstr(row, column, style["leftUp"], attr["frameAttr"])
                    elif (boxTLY == row or boxBRY == row) and boxTLX < column and boxBRX > column:
                        self.__screen.addstr(row, column, style["horizontal"], attr["frameAttr"])
                    elif boxTLY < row and boxBRY > row and (boxTLX == column or boxBRX == column):
                        self.__screen.addstr(row, column, style["vertical"], attr["frameAttr"])

            if self.debug:
                x = boxTLX + 1
                y = (boxTLY + 1) if self.dbgBoxPlacementShow == DBG_BOX_PLACEMENT["Top"] else (boxBRY - 1)
                if self.dbgBoxInfoShow == DBG_BOX_INFO["name"]:
                    self.__screen.addstr(y, x, name[:(attr["boxWidth"] - 1 - self.__FRAME_SIZE)])
                elif self.dbgBoxInfoShow == DBG_BOX_INFO["textSize"]:
                    textSize = f'txt: w = {attr["textWidth"]}, h = {attr["textHeight"]}'
                    self.__screen.addstr(y, x, textSize[:(attr["boxWidth"] - 1 - self.__FRAME_SIZE)])
                elif self.dbgBoxInfoShow == DBG_BOX_INFO["boxSize"]:
                    boxSize = f'box: w = {attr["boxWidth"]}, h = {attr["boxHeight"]}'
                    self.__screen.addstr(y, x, boxSize[:(attr["boxWidth"] - 1 - self.__FRAME_SIZE)])

        if not self.__infoPromptActive:
            self.__reset_info_prompt()
        else:
            self.set_info_prompt_message(self.__infoPromptCurrMessage)


    def __update_prompt(self):
        """ Updates the prompt. """
        self.__promptVLeftPos = self.__promptCursorPos - self.__promptVCursorPos
        self.__promptVRightPos = self.__promptVLeftPos + self.__promptLineWidth

        # Clear prompt
        txt = " " * (self.__wTerminal - 1)
        for i in range(self.__promptHeight):
            self.__screen.addstr(self.__hTerminal - self.__promptHeight - i, 0, txt)

        displayedString = ""
        if len(self.__promptString) >= self.__promptLineWidth:
            displayedString = self.__promptString[self.__promptVLeftPos:self.__promptVRightPos]
        else:
            displayedString = self.__promptString
        self.__screen.addstr(self.__hTerminal - self.__promptHeight, 0, self.__promptSign + displayedString)


    def __update_boxes(self):
        """ Updates all the boxes. """
        for name, attr in self.__boxSetup[self.__activeBoxSetup]["boxes"].items():
            if attr["visable"] == False:
                continue

            displayedText = list()
            if len(attr["lines"]) >= attr["textHeight"]:
                displayedText = attr["lines"][-attr["textHeight"] + attr["scrollIndex"]:][:attr["textHeight"]]
            else:
                displayedText = attr["lines"]

            for i, line in enumerate(displayedText):
                self.__screen.addstr(attr["textStartY"] + i, attr["textStartX"], line[0], line[1])


    def __update_boxes_scrolls(self):
        """ Updates the scroll wheel for all boxes. """
        for name, attr in self.__boxSetup[self.__activeBoxSetup]["boxes"].items():
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
                    self.__screen.addstr(row, attr["bottomRight"]["x"], attr["scrollChar"], attr["frameAttr"])


    def __update_visual_cursor(self):
        """ Updates the visual cursor in the prompt. """
        self.__screen.move(self.__hTerminal - self.__promptHeight, self.__promptVCursorPos + len(self.__promptSign))


    def __update_boxes_frame_attr(self):
        """ Updates all the boxes frame attributes from unmerged to merged. """
        for setupName, setupAttr in self.__boxSetup.items():
            for boxName, boxAttr in setupAttr["boxes"].items():
                boxAttr["frameAttr"] = self.__merge_attributes(boxAttr["frameAttrUnmerged"])


    ###################################################################################################################
    # GET/SET FUNCTIONS                                                                                               #
    ###################################################################################################################

    def get_prompt_sign(self):
        """ Get the prompt sign. """
        return self.__promptSign


    def set_prompt_sign(self, sign):
        """ Set the prompt sign.
            Arguments:
                sign        - The sign variable for the prompt.     (str)
        """
        self.__is_type(sign, str)

        self.__promptSign = sign
        self.__promptSignSize = len(self.__promptSign)
        self.__PROMPT_MIN_WIDTH = self.__promptSignSize + 10


    def get_prompt_string(self):
        """ Get the prompt string. """
        return self.__promptString


    def set_prompt_string(self, string):
        """ Set the prompt string.
            Arguments:
                string          - The string displayed in the prompt.   (str)
        """
        self.__is_type(string, str)

        self.__promptString = string

        self.__promptCursorPos = len(string)
        if self.__promptCursorPos >= self.__promptLineWidth:
            self.__promptVCursorPos = self.__promptLineWidth
        else:
            self.__promptVCursorPos = len(string)


    def get_info_prompt_char(self):
        """ Get the info prompt character. """
        return self.__infoPromptChar


    def set_info_prompt_char(self, char):
        """ Set the info prompt character.
            Arguments:
                char        - The character for the info prompt line.       (str)
        """
        self.__is_type(char, str)
        if len(char) != 1:
            raise Exception("Char can only be of length 1.")

        self.__infoPromptChar = char


    def get_info_prompt_char_attr(self):
        """ Get the info prompt character attributes. """
        return self.__infoPromptCharAttr


    def set_info_prompt_char_attr(self, attributes):
        """ Set the info prompt character attributes.
            Arguments:
                attributes      - The info prompt line attributes.      (str/list)
        """
        self.__check_attributes_valid(attributes)

        self.__infoPromptCharAttr = attributes


    def get_info_prompt_text_attr(self):
        """ Get the info prompt text attributes. """
        return self.__infoPromptTextAttr


    def set_info_prompt_text_attr(self, attributes):
        """ Set the info prompt text attributes.
            Arguments:
                attributes      - The info prompt text attributes.      (str/list)
        """
        self.__check_attributes_valid(attributes)

        self.__infoPromptTextAttr = attributes


    def get_info_prompt_text_indent(self):
        """ Get the info prompt text indentation. """
        return self.__infoPromptTextIndent


    def set_info_prompt_text_indent(self, indent):
        """ Set the info prompt text indentation.
            Arguments:
                indent          - The indentation of the info prompt text.      (int)
        """
        self.__is_type(char, int)
        if indent < 0:
            raise Exception("indent can't be lower than 0.")

        self.__infoPromptTextIndent = indent
        self.__INFO_PROMPT_MIN_WIDTH = self.__infoPromptTextIndent * 2 + (2 + 5)


    def get_box_width(self, setupName, boxName):
        """ Get the fixed width of a given box.
            Arguments:
                setupName           - The name of the box setup.            (str)
                boxName             - The name of the text box.             (str)
        """
        self.__check_text_box_valid(setupName, boxName)

        return self.__boxSetup[setupName]["boxes"][boxName]["fixedWidth"]


    def set_box_width(self, setupName, boxName, width):
        """ Set the fixed width of a given box.
            Arguments:
                setupName           - The name of the box setup.            (str)
                boxName             - The name of the text box.             (str)
                width               - Width of the text box.                (int)
        """
        self.__check_text_box_valid(setupName, boxName)

        self.__is_type(width, int)

        self.__boxSetup[setupName]["boxes"][boxName]["fixedWidth"] = width


    def get_box_height(self, setupName, boxName):
        """ Get the fixed height of a given box.
            Arguments:
                setupName           - The name of the box setup.            (str)
                boxName             - The name of the text box.             (str)
        """
        self.__check_text_box_valid(setupName, boxName)

        return self.__boxSetup[setupName]["boxes"][boxName]["fixedHeight"]


    def set_box_height(self, setupName, boxName, height):
        """ Set the fixed height of a given box.
            Arguments:
                setupName           - The name of the box setup.            (str)
                boxName             - The name of the text box.             (str)
                height              - The height of the text box.           (int)
        """
        self.__check_text_box_valid(setupName, boxName)

        self.__is_type(height, int)

        self.__boxSetup[setupName]["boxes"][boxName]["fixedHeight"] = height


    def get_box_horizontal_orient(self, setupName, boxName):
        """ Get a given box horizontal orientation.
            Arguments:
                setupName           - The name of the box setup.            (str)
                boxName             - The name of the text box.             (str)
        """
        self.__check_text_box_valid(setupName, boxName)

        return self.__boxSetup[setupName]["boxes"][boxName]["hOrient"]


    def set_box_horizontal_orient(self, setupName, boxName,  orient):
        """ Set a given box horizontal orientation.
            Arguments:
                setupName           - The name of the box setup.                                    (str)
                boxName             - The name of the text box.                                     (str)
                orient              - Horizontal orientation of the box (0 : Left, 1 : Right).      (int)
        """
        self.__check_text_box_valid(setupName, boxName)

        if not isinstance(orient, int) or orient not in H_ORIENT.values():
            raise Exception("orient is not of integer type or not within acceptable range.")

        self.__boxSetup[setupName]["boxes"][boxName]["hOrient"] = orient


    def get_box_vertical_orient(self, setupName, boxName):
        """ Get a given box vertical orientation.
            Arguments:
                setupName           - The name of the box setup.            (str)
                boxName             - The name of the text box.             (str)
        """
        self.__check_text_box_valid(setupName, boxName)

        return self.__boxSetup[setupName]["boxes"][boxName]["vOrient"]


    def set_box_vertical_orient(self, setupName, boxName, orient):
        """ Set a given box vertical orientation.
            Arguments:
                setupName           - The name of the box setup.                                    (str)
                boxName             - The name of the text box.                                     (str)
                orient              - Vertical orientation of the box (0 : Up, 1 : Down).           (int)
        """
        self.__check_text_box_valid(setupName, boxName)

        if not isinstance(orient, int) or orient not in V_ORIENT.values():
            raise Exception("orient is not of integer type or not within acceptable range.")

        self.__boxSetup[setupName]["boxes"][boxName]["vOrient"] = orient


    def get_box_text_width_indent(self, setupName, boxName):
        """ Get a given box text width indentation.
            Arguments:
                setupName           - The name of the box setup.            (str)
                boxName             - The name of the text box.             (str)
        """
        self.__check_text_box_valid(setupName, boxName)

        return self.__boxSetup[setupName]["boxes"][boxName]["wTextIndent"]


    def set_box_text_width_indent(self, setupName, boxName, indent):
        """ Set a given box text width indentation.
            Arguments:
                setupName           - The name of the box setup.                    (str)
                boxName             - The name of the text box.                     (str)
                indent              - Width indentation of the text in the box.     (int)
        """
        self.__check_text_box_valid(setupName, boxName)
        self.__is_type(indent, int)

        self.__boxSetup[setupName]["boxes"][boxName]["wTextIndent"] = indent


    def get_box_text_height_indent(self, setupName, boxName):
        """ Get a given text height indentation.
            Arguments:
                setupName           - The name of the box setup.            (str)
                boxName             - The name of the text box.             (str)
        """
        self.__check_text_box_valid(setupName, boxName)

        return self.__boxSetup[setupName]["boxes"][boxName]["hTextIndent"]


    def set_box_text_height_indent(self, setupName, boxName, indent):
        """ Set a given box height indentation.
            Arguments:
                setupName           - The name of the box setup.                    (str)
                boxName             - The name of the text box.                     (str)
                indent              - Height indentation of the text in the box.    (int)
        """
        self.__check_text_box_valid(setupName, boxName)
        self.__is_type(indent, int)

        self.__boxSetup[setupName]["boxes"][boxName]["hTextIndent"] = indent


    def get_box_frame_char(self, setupName, boxName):
        """ Get a given box frame character.
            Arguments:
                setupName           - The name of the box setup.            (str)
                boxName             - The name of the text box.             (str)
        """
        self.__check_text_box_valid(setupName, boxName)

        return self.__boxSetup[setupName]["boxes"][boxName]["frameChar"]


    def get_box_frame_char_dict(self, setupName, boxName):
        """ Get a given box frame character dictionary.
            Arguments:
                setupName           - The name of the box setup.            (str)
                boxName             - The name of the text box.             (str)
        """
        self.__check_text_box_valid(setupName, boxName)

        style = self.__boxSetup[setupName]["boxes"][boxName]["frameChar"]

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


    def set_box_frame_char(self, setupName, boxName, char):
        """ Set a given box frame character.
            Arguments:
                setupName           - The name of the box setup.                                    (str)
                boxName             - The name of the text box.                                     (str)
                char                - What frame style should be used (check FRAME_STYLE dict).     (str)
        """
        self.__check_text_box_valid(setupName, boxName)
        self.__is_type(char, str)

        if char not in FRAME_STYLE:
            raise Exception(f"{char} is not in FRAME_STYLE.")

        self.__boxSetup[setupName]["boxes"][boxName]["frameChar"] = char


    def get_box_frame_attr(self, setupName, boxName):
        """ Get a given box frame attributes.
            Arguments:
                setupName           - The name of the box setup.            (str)
                boxName             - The name of the text box.             (str)
        """
        self.__check_text_box_valid(setupName, boxName)

        return self.__boxSetup[setupName]["boxes"][boxName]["frameAttrUnmerged"]


    def set_box_frame_attr(self, setupName, boxName, attributes):
        """ Set a given box frame attribute.
            Arguments:
                setupName           - The name of the box setup.                                    (str)
                boxName             - The name of the text box.                                     (str)
                attributes          - What frame attributes should be used (color, text format).    (str/list)
        """
        self.__check_text_box_valid(setupName, boxName)
        self.__check_attributes_valid(attributes)

        self.__boxSetup[setupName]["boxes"][boxName]["frameAttrUnmerged"] = attributes

        self.__update_boxes_frame_attr()


    def get_box_visable(self, setupName, boxName):
        """ Get a given box visable.
            Arguments:
                setupName           - The name of the box setup.            (str)
                boxName             - The name of the text box.             (str)
        """
        self.__check_text_box_valid(setupName, boxName)

        return self.__boxSetup[setupName]["boxes"][boxName]["visable"]


    def set_box_visable(self, setupName, boxName, visable):
        """ Set a given box visable.
            Arguments:
                setupName           - The name of the box setup.            (str)
                boxName             - The name of the text box.             (str)
                visable             - Should the box be visable or not.     (bool)
        """
        self.__check_text_box_valid(setupName, boxName)
        self.__is_type(visable, bool)

        self.__boxSetup[setupName]["boxes"][boxName]["visable"] = visable


    def get_box_horizontal_pos(self, setupName, boxName):
        """ Get a given box horizontal position.
            Arguments:
                setupName           - The name of the box setup.            (str)
                boxName             - The name of the text box.             (str)
        """
        self.__check_text_box_valid(setupName, boxName)

        return self.__boxSetup[setupName]["boxOrder"].index(boxName)


    def set_box_horizontal_pos(self, setupName, boxName, pos):
        """ Set a given box horizontal position.
            Arguments:
                setupName           - The name of the box setup.                        (str)
                boxName             - The name of the text box.                         (str)
                pos                 - Where this box should be placed horizontally.     (int)
        """
        self.__check_text_box_valid(setupName, boxName)
        self.__is_type(pos, int)

        self.__boxSetup[setupName]["boxOrder"].pop(self.__boxSetup[setupName]["boxOrder"].index(boxName))
        self.__boxSetup[setupName]["boxOrder"].insert(pos, boxName)
        self.__boxSetup[setupName]["boxes"] = \
                {key : self.__boxSetup[setupName]["boxes"][key] for key in self.__boxSetup[setupName]["boxOrder"]}


    def get_box_vertical_pos(self, setupName, boxName):
        """ Get a given box vertical position.
            Arguments:
                setupName           - The name of the box setup.            (str)
                boxName             - The name of the text box.             (str)
        """
        self.__check_text_box_valid(setupName, boxName)

        # TBD


    def get_box_vertical_pos(self, setupName, boxName, pos):
        """ Set a given box vertical position.
            Arguments:
                setupName           - The name of the box setup.                    (str)
                boxName             - The name of the text box.                     (str)
                pos                 - Where this box should be placed vertically.   (int)
        """
        self.__check_text_box_valid(setupName, boxName)

        # TBD


    def set_active_box_setup(self, setupName):
        """ Set the active box setup.
            Arguments:
                setupName           - The name of the box setup.            (str)
                boxName             - The name of the text box.             (str)
        """
        self.__check_box_setup_valid(setupName)

        self.__activeBoxSetup = setupName


    def set_focus_box(self, setupName, boxName):
        """ Set a box in focus i.e. make it scrollable.
            Arguments:
                setupName           - The name of the box setup.            (str)
                boxName             - The name of the text box.             (str)
        """
        self.__check_text_box_valid(setupName, boxName)

        if self.__boxSetup[setupName]["boxes"][boxName]["visable"] == False:
            raise Exception(f"Can not set focus on an invisible box.")

        self.__boxSetup[setupName]["focusedBox"] = boxName


    def get_box_scroll_visable(self, setupName, boxName):
        """ Get a given box scroll visable.
            Arguments:
                setupName           - The name of the box setup.            (str)
                boxName             - The name of the text box.             (str)
        """
        self.__check_text_box_valid(setupName, boxName)

        return self.__boxSetup[setupName]["boxes"][boxName]["scrollVisable"]


    def set_box_scroll_visable(self, setupName, boxName, visable):
        """ Set a given box scroll visable.
            Arguments:
                setupName           - The name of the box setup.                (str)
                boxName             - The name of the text box.                 (str)
                visable             - Should the scrollbar be visable or not.   (bool)
        """
        self.__check_text_box_valid(setupName, boxName)

        self.__boxSetup[setupName]["boxes"][boxName]["scrollVisable"] = visable


    def set_prompt_callback_function(self, function):
        """ Set the prompt callback function every time <ENTER> is pressed.
            Arguments:
                function            - The callback function.        (Function)
        """
        self.__promptCallbackFunction = function


    ###################################################################################################################
    # KEY HANDLER FUNCTION                                                                                            #
    ###################################################################################################################

    def __key_handler(self, event):
        """ Handler of key presses.
            Arguments:
                event           - Event argument (Not used).
        """
        while True:
            char = self.__screen.get_wch()

            focusedBox = self.__boxSetup[self.__activeBoxSetup]["focusedBox"]


            if self.__promptCharCallbackFunction != None:
                self.__promptCharCallbackFunction(char)

            # GENERAL KEY EVENTS --------------------------------------------------------------------------------------
            if char == "\x1b":                  # <ESC> KEY (Exit)
                break

            elif char == "\x00":                # "WINDOWS" KEY
                pass

            elif char == curses.KEY_RESIZE:     # RESIZE EVENT
                self.__promptCursorPos = 0
                self.__promptVCursorPos = 0

                if self.__resizeDone:
                    self.__screen.clear()

                self.__resizeDone = False
                self.__resizeTimer.cancel()
                self.__resizeTimer = threading.Timer(.1, self.__resize_timeout)
                self.__resizeTimer.start()


            # PROMPT KEY EVENTS ---------------------------------------------------------------------------------------
            elif char == 260:                   # <ARROW-LEFT> KEY (Scroll left)
                if self.__promptVCursorPos != 0:
                    self.__promptVCursorPos -= 1
                if self.__promptCursorPos != 0:
                    self.__promptCursorPos -= 1

                if self.__resizeDone:
                    self.__update_prompt()
                    self.__update_visual_cursor()
                    continue

            elif char == 261:                   # <ARROW-RIGHT> KEY (Scroll right)
                if self.__promptVCursorPos < len(self.__promptString) and \
                   self.__promptVCursorPos != self.__promptLineWidth:
                    self.__promptVCursorPos += 1
                if self.__promptCursorPos < len(self.__promptString):
                    self.__promptCursorPos += 1

                if self.__resizeDone:
                    self.__update_prompt()
                    self.__update_visual_cursor()
                    continue

            elif char == 262:                   # HOME KEY
                self.__promptVCursorPos = 0
                self.__promptCursorPos = 0

                if self.__resizeDone:
                    self.__update_prompt()
                    self.__update_visual_cursor()
                    continue

            elif char == 358 or char == 360:    # END KEY
                if len(self.__promptString) >= self.__promptLineWidth:
                    self.__promptVCursorPos = self.__promptLineWidth
                else:
                    self.__promptVCursorPos = len(self.__promptString)
                self.__promptCursorPos = len(self.__promptString)

                if self.__resizeDone:
                    self.__update_prompt()
                    self.__update_visual_cursor()
                    continue

            elif char == 330:                   # DELETE KEY
                self.__promptString = self.__promptString[:self.__promptCursorPos] + \
                    self.__promptString[self.__promptCursorPos:][1:]

                if len(self.__promptString) >= self.__promptLineWidth:
                    if len(self.__promptString) == (self.__promptVRightPos - 1) and \
                       self.__promptVCursorPos != self.__promptLineWidth:
                        self.__promptVCursorPos += 1

                if self.__resizeDone:
                    self.__update_prompt()
                    self.__update_visual_cursor()
                    continue

            elif char == "\x08" or char == 263: # BACKSPACE KEY
                self.__promptString = self.__promptString[:self.__promptCursorPos][:-1] + \
                    self.__promptString[self.__promptCursorPos:]

                if self.__promptVCursorPos != 0 and len(self.__promptString) <= self.__promptLineWidth and \
                   self.__promptVLeftPos == 0:
                    self.__promptVCursorPos -= 1
                elif self.__promptVCursorPos != 0 and len(self.__promptString) >= self.__promptLineWidth and \
                     self.__promptVLeftPos == 0:
                    self.__promptVCursorPos -= 1
                if self.__promptCursorPos != 0:
                    self.__promptCursorPos -= 1

                if self.__resizeDone:
                    self.__update_prompt()
                    self.__update_visual_cursor()
                    continue

            elif char == "\x16":                # CTRL + V (paste)
                copy = self.__get_clipboard()
                if copy != None and copy != False:
                    self.__promptString = self.__promptString[:self.__promptCursorPos] + copy + self.__promptString[self.__promptCursorPos:]
                    self.__promptCursorPos += len(copy)
                    if (self.__promptVCursorPos + len(copy)) >= self.__promptLineWidth:
                        self.__promptVCursorPos = self.__promptLineWidth
                    else:
                        self.__promptVCursorPos += len(copy)

                if self.__resizeDone:
                    self.__update_prompt()
                    self.__update_visual_cursor()
                    continue

            elif char == "\n": # <ENTER>
                if self.__promptString != "" and self.__promptEnterCallbackFunction != None:
                    self.__promptEnterCallbackFunction(self.__promptString)
                self.__promptString = ""
                self.__promptCursorPos = 0
                self.__promptVCursorPos = 0
                self.__boxSetup[self.__activeBoxSetup]["boxes"][focusedBox]["scrollIndex"] = 0


            # BOX KEY EVENTS ------------------------------------------------------------------------------------------
            elif char == 259:                   # <ARROW-UP> KEY (Scroll up)
                lines = self.__boxSetup[self.__activeBoxSetup]["boxes"][focusedBox]["lines"]
                scrollIndex = self.__boxSetup[self.__activeBoxSetup]["boxes"][focusedBox]["scrollIndex"]
                textHeight = self.__boxSetup[self.__activeBoxSetup]["boxes"][focusedBox]["textHeight"]
                if len(lines) + scrollIndex > textHeight:
                    self.__boxSetup[self.__activeBoxSetup]["boxes"][focusedBox]["scrollIndex"] -= 1

            elif char == 258:                   # <ARROW-DOWN> KEY (Scroll down)
                if self.__boxSetup[self.__activeBoxSetup]["boxes"][focusedBox]["scrollIndex"] != 0:
                    self.__boxSetup[self.__activeBoxSetup]["boxes"][focusedBox]["scrollIndex"] += 1

            elif char == 339:                   # PAGE UP (Scroll up)
                lines = self.__boxSetup[self.__activeBoxSetup]["boxes"][focusedBox]["lines"]
                textHeight = self.__boxSetup[self.__activeBoxSetup]["boxes"][focusedBox]["textHeight"]
                self.__boxSetup[self.__activeBoxSetup]["boxes"][focusedBox]["scrollIndex"] -= textHeight
                scrollIndex = self.__boxSetup[self.__activeBoxSetup]["boxes"][focusedBox]["scrollIndex"]
                if scrollIndex < -(len(lines) - textHeight):
                    self.__boxSetup[self.__activeBoxSetup]["boxes"][focusedBox]["scrollIndex"] = -(len(lines) - textHeight)

            elif char == 338:                   # PAGE DOWN (Scroll down)
                textHeight = self.__boxSetup[self.__activeBoxSetup]["boxes"][focusedBox]["textHeight"]
                self.__boxSetup[self.__activeBoxSetup]["boxes"][focusedBox]["scrollIndex"] += textHeight
                if self.__boxSetup[self.__activeBoxSetup]["boxes"][focusedBox]["scrollIndex"] > 0:
                    self.__boxSetup[self.__activeBoxSetup]["boxes"][focusedBox]["scrollIndex"] = 0


            # REGULAR ASCII KEY EVENTS --------------------------------------------------------------------------------
            else: # Append characters to self.__promptString
                if isUnicode(char):
                    self.__promptString =   self.__promptString[:self.__promptCursorPos] + str(char) + \
                        self.__promptString[self.__promptCursorPos:]
                    if self.__promptVCursorPos != self.__promptLineWidth:
                        self.__promptVCursorPos += 1
                    self.__promptCursorPos += 1

                if self.__resizeDone:
                    self.__update_prompt()
                    self.__update_visual_cursor()
                    continue

            self.update()

        curses.endwin() # Close curses terminal}}}


    ###################################################################################################################
    # OTHER FUNCTIONS                                                                                                 #
    ###################################################################################################################

    def __init_colors(self):
        """ Initialize curses colors. """
        curses.start_color()
        curses.use_default_colors()

        for color, value in CHAR_COLOR.items():
            curses.init_pair(value, value - 1, -1)


    def __init_box_default_parameters(self, setupName, boxName):
        """ Initialize a given box with default parameters.
            Arguments:
                setupName           - The name of the box setup.            (str)
                boxName             - The name of the text box.             (str)
        """
        self.__boxSetup[setupName]["boxes"][boxName]                        = dict()
        self.__boxSetup[setupName]["focusedBox"]                            = boxName

        self.__boxSetup[setupName]["boxes"][boxName]["fixedWidth"]          = None
        self.__boxSetup[setupName]["boxes"][boxName]["fixedHeight"]         = None
        self.__boxSetup[setupName]["boxes"][boxName]["hOrient"]             = H_ORIENT["Left"]
        self.__boxSetup[setupName]["boxes"][boxName]["vOrient"]             = V_ORIENT["Up"]
        self.__boxSetup[setupName]["boxes"][boxName]["visable"]             = True
        self.__boxSetup[setupName]["boxes"][boxName]["wTextIndent"]         = 0
        self.__boxSetup[setupName]["boxes"][boxName]["hTextIndent"]         = 0
        self.__boxSetup[setupName]["boxes"][boxName]["boxWidth"]            = None
        self.__boxSetup[setupName]["boxes"][boxName]["boxHeight"]           = None
        self.__boxSetup[setupName]["boxes"][boxName]["prevBoxWidth"]        = None
        self.__boxSetup[setupName]["boxes"][boxName]["prevBoxHeight"]       = None
        self.__boxSetup[setupName]["boxes"][boxName]["textWidth"]           = None
        self.__boxSetup[setupName]["boxes"][boxName]["textHeight"]          = None
        self.__boxSetup[setupName]["boxes"][boxName]["topLeft"]             = None
        self.__boxSetup[setupName]["boxes"][boxName]["bottomRight"]         = None
        self.__boxSetup[setupName]["boxes"][boxName]["textStartX"]          = 0
        self.__boxSetup[setupName]["boxes"][boxName]["textStartY"]          = 0
        self.__boxSetup[setupName]["boxes"][boxName]["frameAttrUnmerged"]   = "white"
        self.__boxSetup[setupName]["boxes"][boxName]["frameAttr"]           = None
        self.__boxSetup[setupName]["boxes"][boxName]["frameChar"]           = "singleLine"

        self.__boxSetup[setupName]["boxes"][boxName]["textItems"]           = list()
        self.__boxSetup[setupName]["boxes"][boxName]["prevTextItemsLength"] = 0
        self.__boxSetup[setupName]["boxes"][boxName]["lines"]               = list()
        self.__boxSetup[setupName]["boxes"][boxName]["scrollIndex"]         = 0

        self.__boxSetup[setupName]["boxes"][boxName]["scrollVisable"]       = True
        self.__boxSetup[setupName]["boxes"][boxName]["scrollChar"]          = "█"


    def __reset_info_prompt(self):
        """ Resets the info prompt (Removes potential info messages). """
        startOfInfoPromptX = 0
        startOfInfoPromptY = self.__hTerminal - 1 - self.__promptHeight
        bg = self.__merge_attributes(self.__infoPromptCharAttr)
        self.__screen.addstr(startOfInfoPromptY, startOfInfoPromptX, self.__wTerminal * self.__infoPromptChar, bg)


    def __get_clipboard(self):
        """ Get system clipboard. """
        clipboard = None

        if PLATFORM in PLATFORM_WINDOWS:
            win32clipboard.OpenClipboard()
            clipboard = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

        elif PLATFORM in PLATFORM_LINUX:
            pass
        elif PLATFORM in PLATFORM_MAC:
            pass
        else:
            return False

        return clipboard


    def __info_prompt_text_timeout(self):
        """ Timeout function for when info prompt should be cleared. """
        self.__infoPromptActive = False
        self.__reset_info_prompt()
        self.__update_visual_cursor()
        self.__screen.refresh()


    def __resize_timeout(self):
        """ Timeout function for when setup is ready to be refreshed. """
        self.__resizeDone = True
        self.__screen.clear()
        self.__screen.refresh()
        self.update()


    def __merge_attributes(self, attributes):
        """ Merges all attribute values to a single attribute and returns it.
            Raises exception if invalid attribute exist.
            Arguments:
                attributes          - What frame attributes should be used (color, text format).    (str/list)
        """
        self.__check_attributes_valid(attributes)

        if isinstance(attributes, str):
            attributes = [attributes]

        merged = 0
        for item in attributes:
            if item in CHAR_COLOR:
                merged = merged | curses.color_pair(CHAR_COLOR[item])
            elif item in CHAR_ATTR:
                merged = merged | CHAR_ATTR[item]

        return merged


    ###################################################################################################################
    # CHECK FUNCTIONS                                                                                                 #
    ###################################################################################################################

    def __check_box_setup_valid(self, setupName, shouldExist=True):
        """ Check to see if a given setupBox exist or does not exist.
            Arguments:
                setupName           - The name of the box setup.            (str)
                boxName             - The name of the text box.             (str)
                shouldExist         - Should the setup exist.               (bool)
        """
        self.__is_type(setupName, str)

        if shouldExist:
            if setupName not in self.__boxSetup:
                raise Exception(f"Box setup {name} does not exist.")
        else:
            if setupName in self.__boxSetup:
                raise Exception(f"Box setup {name} already exist.")

        return True


    def __check_text_box_valid(self, setupName, boxName, shouldExist=True):
        """ Check to see if a given boxName exist or does not exist.
            Arguments:
                setupName           - The name of the box setup.            (str)
                boxName             - The name of the text box.             (str)
                shouldExist         - Should the text box exist.            (bool)
        """
        self.__check_box_setup_valid(setupName)

        self.__is_type(boxName, str)

        if shouldExist:
            if boxName not in self.__boxSetup[setupName]["boxes"]:
                raise Exception(f"TextBox {boxName} does not exist.")
        else:
            if boxName in self.__boxSetup[setupName]["boxes"]:
                raise Exception(f"TextBox {boxName} already exist.")

        return True


    def __check_attributes_valid(self, attributes):
        """ Checks if the given attributes are valid.
            Arguments:
                attributes          - What frame attributes should be used (color, text format).    (str/list)
        """
        if attributes == None:
            return None

        if not (isinstance(attributes, list) or isinstance(attributes, str)):
            raise Exception("Attributes needs to be either string or list.")

        if isinstance(attributes, str):
            attributes = [attributes]

        for item in attributes:
            if not (item in CHAR_COLOR or item in CHAR_ATTR):
                raise Exception(f"{item} is not a valid attribute.")


    def __is_type(self, value, ttype):
        """ Checks if a given value is of the expected type.
            Arguments:
                value           - The variable to be checked.       (Any type)
                ttype           - The type that 'value' should be   (Any type)
        """
        if not isinstance(value, ttype):
            raise Exception("Value is not of {ttype} type.")
        return True





class TestTextBox():
    """  """

    def __init__(self):
        """  """
        self.tb = TerminalTextBoxes(self.test_callback)
        self.tb.create_text_box_setup("setup")

        self.tb.create_text_box("setup", "text", frameAttr="green", wTextIndent=1)
        self.tb.create_text_box("setup", "info", 20, frameAttr="red", hOrient=H_ORIENT["Right"])

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
            self.tb.add_text_item("setup", "text", message, attributes=["white", "bold"])


if __name__ == "__main__":
    ttb = TestTextBox()
