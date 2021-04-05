#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import terminalTextBoxes as ttb


class Chat():
    """  """

    def __init__(self):
        """  """
        self.tb = ttb.TerminalTextBoxes(self.character_callback, self.enter_callback)
        self.tb.create_text_box_setup("setup")

        self.tb.create_text_box("setup", "text", frameAttr="green", wTextIndent=1)
        self.tb.create_text_box("setup", "info", 20, frameAttr="red", hOrient=ttb.H_ORIENT["right"])

        self.tb.set_focus_box("setup", "text")

        self.tb.start()


    def character_callback(self, char):
        """  """

    def enter_callback(self, message):
        """  """
        if message.startswith("!note"):
            message = message.replace("!note", "NOTE:")
            self.tb.infoPromptTextAttr = ["yellow", "bold"]
            self.tb.set_info_prompt_text(message, 5000)
        elif message.startswith("!error"):
            message = message.replace("!error", "ERROR:")
            self.tb.infoPromptTextAttr = ["red", "bold"]
            self.tb.set_info_prompt_text(message, 5000)
        else:
            self.tb.infoPromptTextAttr = ["white"]
            self.tb.add_text_item("setup", "text", message, attributes=["white", "bold"])


if __name__ == "__main__":
    chat = Chat()
