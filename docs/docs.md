# Terminal Text Box Documentation

## Public Dictionaries

### Character colors
- black
- blue
- green
- cyan
- red
- magenta
- yellow
- white

Example usage:

    CHAR_COLOR["green"]

### Character attributes
- altCharset
- blink
- bold
- dim
- invisible
- italic
- normal
- protect
- reverse
- standout
- underline
- horizontal
- left
- low
- right
- top
- vertical
- chartext

Example usage:

    CHAR_ATTR["standout"]

### Frame styles
- singleLine
- doubleLine
- hash
- at
- star
- blockFull
- blockVague0
- blockVague1
- blockVague2
- invisible

Example usage:

    FRAME_STYLE["singleLine"]

### Lines types
- wrap
- single

Example usage:

    LINE_TYPE["wrap"]

### Horizontal orientations
- left
- right

Example usage:

    H_ORIENT["left"]

### Vertical orientations
- up
- down

Example usage:

    V_ORIENT["up"]

### Debug box placement
- top
- bottom

Example usage:

    DBG_BOX_PLACEMENT["top"]

### Debug box information
- name
- textSize
- boxSize

Example usage:

    DBG_BOX_INFO["textSize"]


## Text box parameters

    fixedWidth              The fixed width of the box, None if width is dynamic. boxWidth is the same as fixedWidth
                            if fixedWith is not None.

    fixedHeight             The fixed height of the box, None if height is dynamic. boxHeight is the same as
                            fixedHeight if fixedWidth is not None.

    hOrient                 The horizontal orientation of the box (0 : left, 1 : right).

    vOrient                 The vertical orientation of the box (0 : up, 1 : down).

    visable                 Should the box be visable or not? If invisible, it acts as a padding box and share the
                            dynamic space pool.

    wTextIndent             Width indentation of the text in the box.

    hTextIndent             Height indentation of the text in the box.

    boxWidth                Same as fixedWidth if fixedWidth is not None. If fixedWidth is None then boxWidth
                            will share the dynamic width with other dymanic boxes.

    boxHeight               Same as fixedHeight if fixedHeight is not None. If fixedHeight is None then boxHeight
                            will share the dynamic height with other dynamic boxes.

    prevBoxWidth            Stores the previous box Width (for keeping track of box size change).

    prevBoxHeight           Store the previous box height (for keeping track of box size change).

    textWidth               The maximum text width of the box.

    textHeight              The maximum text height of the box.

    topLeft                 The top left corner coordinate of the box (x and y).

    bottomRight             The bottom right corner coordinate of the box (x and y).

    textStartX              The start of the text in the box (The x-coordinate).

    textStartY              The start of the text in the box (The y coordinate).

    frameAttrUnmerged       The unmerged frame attributes. Once the function start() is run, frameAttrUnmerged will be
                            merged and set in frameAttr parameter.

    frameAttr               The merged frame attributes.

    frameChar               The frame character, check frame styles.

    textItems               A list of text items that should be printed in the box. every item contain the text, text
                            attributes and line type.

    prevTextItemsLength     The previous text items length (for keeping track of box size change).

    lines                   The textItems but in a formatted way so that fits inside the box.

    scrollIndex             The scroll index of the box.

    scrollVisable           If the scrollbar should be visable for the box.

    scrollChar              What scrollbar character that should be used.


## Public Functions

### create_text_box_setup(*setupName*)
Creates a new 'text box setup' in which you can add text boxes to.

Arguments:
- **setupName** : The name of the box setup. (**str**)


### remove_text_box_setup(*setupName*)
Removes a 'text box setup'.

Arguments:
- **setupName** : The name of the box setup. (**str**)


### create_text_box(*setupName*, *boxName*, *width=None*, *height=None*, *hPos=None*, *vPos=None*, *hOrient=0*, *vOrient=0*, *visable=True*, *wTextIndent=0*, *hTextIndent=0*, *frameChar="singleLine"*, *frameAttr="white"*, *scrollVisable=True*)
Creates a text box inside the given text box setup.

Arguments:
- **setupName** : The name of the box setup. (**str**)
- **boxName** : The name of the text box. (**str**)
- **width** : Width of the text box (None if width is not fixed size). (**int**)
- **height** : Height of the text box (None if height is not fixed size). (**int**)
- **hPos** : Where this box should be placed horizontally. (**int**)
- **vPos** : Where this box should be placed vertically. (**int**)
- **hOrient** : Horizontal orientation of the box (0 ( Left, 1 : Right). (**int**)
- **vOrient** : Vertical orientation of the box (0 ( Up, 1 : Down). (**int**)
- **visable** : Should the box be visable or not? (Padding box?). (**bool**)
- **wTextIndent** : Width indentation of the text in the box. (**int**)
- **hTextIndent** : Height indentation of the text in the box. (**int**)
- **frameChar** : What frame style should be used (check FRAME_STYLE dict). (**str**)
- **frameAttr** : What frame attributes should be used (color, text format). (**str/list**)
- **scrollVisable** : Should the scrollbar be visable or not. (**bool**)


### remove_text_box(*setupName*, *boxName*)
Removes a text box inside the given text box setup.

Arguments:
- **setupName** : The name of the box setup. (**str**)
- **boxName** : The name of the text box. (**str**)


### start()
Start displaying the terminal text boxes module.


### stop()
Stop displaying the terminal text boxes module.


### set_info_prompt_text(*text*, *timeout=None*)
Sets info text above the prompt.

Arguments:
- **text** : The text to be set in the info prompt. (**str**)
- **timeout** : Timeout before message disappears (ms). (**int**)


### add_text_item(*setupName*, *boxName*, *text*, *attributes="white"*, *lineType="wrap"*)
Adds a text item to the textItems list of the given text box.

Arguments:
- **setupName** :  The name of the box setup. (**str**)
- **boxName** : The name of the text box. (**str**)
- **text** : The text to be added. (**str**)
- **attributes** : The text attributes. (**str/list**)
- **lineType** : The line type (wrap/single). (**str**)


### remove_text_item(*setupName*, *boxName*, *index*)
Removes a text item from the textItems list of the given text box.

Arguments:
- **setupName** : The name of the box setup. (**str**)
- **boxName** : The name of the text box. (**str**)
- **index** : The index of the item to be removed. (**int**)


### clear_text_items(*setupName*, *boxName*)
Clears the entire textItems list from a given text box.

Arguments:
- **setupName** : The name of the box setup. (**str**)
- **boxName** : The name of the text box. (**str**)


### update()
Updates all.


### get_prompt_sign()
Get the prompt sign.


### set_prompt_sign(*sign*)
Set the prompt sign.

Arguments:
- **sign** :  The sign variable for the prompt. (**str**)


### get_prompt_string()
Get the prompt string.


### set_prompt_string(*string*)
Set the prompt string.

Arguments:
- **string** : The string displayed in the prompt. (**str**)


### get_prompt_cursor_pos()
Get the prompt cursor position.


### get_info_prompt_char()
Get the info prompt character.


### set_info_prompt_char(*char*)
Set the info prompt character.

Arguments:
- **char** : The character for the info prompt line. (**str**)


### get_info_prompt_char_attr()
Get the info prompt character attributes.


### set_info_prompt_char_attr(*attributes*)
Set the info prompt character attributes.

Arguments:
- **attributes** : The info prompt line attributes. (**str/list**)


### get_info_prompt_text_attr()
Get the info prompt text attributes.


### set_info_prompt_text_attr(*attributes*)
Set the info prompt text attributes.

Arguments:
- **attributes** : The info prompt text attributes. (**str/list**)


### get_info_prompt_text_indent()
Get the info prompt text indentation.


### set_info_prompt_text_indent(*indent*)
Set the info prompt text indentation.

Arguments:
- **indent** : The indentation of the info prompt text. (**int**)


### get_box_width(*setupName*, *boxName*)
Get the fixed width of a given box.

Arguments:
- **setupName** : The name of the box setup. (**str**)
- **boxName** : The name of the text box. (**str**)


### set_box_width(*setupName*, *boxName*, *width*)
Set the fixed width of a given box.

Arguments:
- **setupName** : The name of the box setup. (**str**)
- **boxName** : The name of the text box. (**str**)
- **width** : Width of the text box. (**int**)


### get_box_height(*setupName*, *boxName*)
Get the fixed height of a given box.

Arguments:
- **setupName** : The name of the box setup. (**str**)
- **boxName** : The name of the text box. (**str**)


### set_box_height(*setupName*, *boxName*, *height*)
Set the fixed height of a given box.

Arguments:
- **setupName** : The name of the box setup. (**str**)
- **boxName** : The name of the text box. (**str**)
- **height** : The height of the text box. (**int**)


### get_box_horizontal_orient(*setupName*, *boxName*)
Get a given box horizontal orientation.

Arguments:
- **setupName** :  The name of the box setup. (**str**)
- **boxName** : The name of the text box. (**str**)


### set_box_horizontal_orient(*setupName*, *boxName*, *orient*)
Set a given box horizontal orientation.

Arguments:
- **setupName** : The name of the box setup. (**str**)
- **boxName** : The name of the text box. (**str**)
- **orient** : Horizontal orientation of the box (0 ( Left, 1 : Right). (**int**)


### get_box_vertical_orient(*setupName*, *boxName*)
Get a given box vertical orientation.

Arguments:
- **setupName** : The name of the box setup. (**str**)
- **boxName** : The name of the text box. (**str**)


### set_box_vertical_orient(*setupName*, *boxName*, *orient*)
Set a given box vertical orientation.

Arguments:
- **setupName** : The name of the box setup. (**str**)
- **boxName** : The name of the text box. (**str**)
- **orient** : Vertical orientation of the box (0 ( Up, 1 : Down). (**int**)


### get_box_text_width_indent(*setupName*, *boxName*)
Get a given box text width indentation.

Arguments:
- **setupName** : The name of the box setup. (**str**)
- **boxName** : The name of the text box. (**str**)


### set_box_text_width_indent(*setupName*, *boxName*, *indent*)
Set a given box text width indentation.

Arguments:
- **setupName** : The name of the box setup. (**str**)
- **boxName** : The name of the text box. (**str**)
- **indent** : Width indentation of the text in the box. (**int**)


### get_box_text_height_indent(*setupName*, *boxName*)
Get a given text height indentation.

Arguments:
- **setupName** : The name of the box setup. (**str**)
- **boxName** : The name of the text box. (**str**)


### set_box_text_height_indent(*setupName*, *boxName*, *indent*)
Set a given box height indentation.

Arguments:
- **setupName** : The name of the box setup. (**str**)
- **boxName** : The name of the text box. (**str**)
- **indent** : Height indentation of the text in the box. (**int**)


### get_box_frame_char(*setupName*, *boxName*)
Get a given box frame character.

Arguments:
- **setupName** : The name of the box setup. (**str**)
- **boxName** : The name of the text box. (**str**)


### get_box_frame_char_dict(*setupName*, *boxName*)
Get a given box frame character dictionary.

Arguments:
- **setupName** : The name of the box setup. (**str**)
- **boxName** : The name of the text box. (**str**)


### set_box_frame_char(*setupName*, *boxName*, *char*)
Set a given box frame character.

Arguments:
- **setupName** : The name of the box setup. (**str**)
- **boxName** : The name of the text box. (**str**)
- **char** : What frame style should be used (check FRAME_STYLE dict). (**str**)


### get_box_frame_attr(*setupName*, *boxName*)
Get a given box frame attributes.

Arguments:
- **setupName** : The name of the box setup. (**str**)
- **boxName** : The name of the text box. (**str**)


### set_box_frame_attr(*setupName*, *boxName*, *attributes*)
Set a given box frame attribute.

Arguments:
- **setupName** : The name of the box setup. (**str**)
- **boxName** : The name of the text box. (**str**)
- **attributes** : What frame attributes should be used (color, text format). (**str/list**)


### get_box_visable(*setupName*, *boxName*)
Get a given box visable.

Arguments:
- **setupName** : The name of the box setup. (**str**)
- **boxName** : The name of the text box. (**str**)


### set_box_visable(*setupName*, *boxName*, *visable*)
Set a given box visable.

Arguments:
- **setupName** : The name of the box setup. (**str**)
- **boxName** : The name of the text box. (**str**)
- **visable** : Should the box be visable or not. (**bool**)


### get_box_horizontal_pos(*setupName*, *boxName*)
Get a given box horizontal position.

Arguments:
- **setupName** : The name of the box setup. (**str**)
- **boxName** : The name of the text box. (**str**)


### set_box_horizontal_pos(*setupName*, *boxName*, *pos*)
Set a given box horizontal position.

Arguments:
- **setupName** : The name of the box setup. (**str**)
- **boxName** : The name of the text box. (**str**)
- **pos** : Where this box should be placed horizontally. (**int**)


### get_box_vertical_pos(*setupName*, *boxName*)
Get a given box vertical position.

Arguments:
- **setupName** : The name of the box setup. (**str**)
- **boxName** : The name of the text box. (**str**)


### get_box_vertical_pos(*setupName*, *boxName*, *pos*)
Set a given box vertical position.

Arguments:
- **setupName** : The name of the box setup. (**str**)
- **boxName** : The name of the text box. (**str**)
- **pos** : Where this box should be placed vertically. (**int**)


### set_active_box_setup(*setupName*)
Set the active box setup.

Arguments:
- **setupName** : The name of the box setup. (**str**)


### set_focus_box(*setupName*, *boxName*)
Set a box in focus i.e. make it scrollable.

Arguments:
- **setupName** : The name of the box setup. (**str**)
- **boxName** : The name of the text box. (**str**)


### get_box_scroll_visable(*setupName*, *boxName*)
Get a given box scroll visable.

Arguments:
- **setupName** : The name of the box setup. (**str**)
- **boxName** : The name of the text box. (**str**)


### set_box_scroll_visable(*setupName*, *boxName*, *visable*)
Set a given box scroll visable.

Arguments:
- **setupName** : The name of the box setup. (**str**)
- **boxName** : The name of the text box. (**str**)
- **visable** : Should the scrollbar be visable or not. (**bool**)


### set_prompt_callback_function(*function*)
Set the prompt callback function every time <ENTER> is pressed.

Arguments:
- **function** : The callback function. (**Function**)



