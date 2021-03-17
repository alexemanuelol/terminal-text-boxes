# terminal-text-boxes
A framework for terminal text box functionality used for chat applications, general text flow applications and more...

## TODOs
- Fix clipboard functionality for cross platform
- Fix dynamic creation of boxes. Each box should have name, size, fixed, etc...
- Fix functionality for inputBox callback function
- Add delay in refresh to avoid flipping out when resizing
- Add "isChanged" as box variable to say if the box size is changed
- Add a 'info box' above prompt? to display information
- Re-think attr["textItems"], maybe have [textItem, color, attributes]?
- Add append functions to box textItems
- FIX EDGE CONDITIONS
- Create 'box-sets' to say like "Hey, display this box-set now! Change to "prompt-user box-set"'
- Put frame_style and text_attr into class again?
- Fix the freaking slow update of prompt box, do you really have to update every single module?! like wtf man
- Think of a solution for scroll issue, which box to scroll? How to switch?
- Scroll icon on the side of the box? Some sort of relation with scrollIndex to indicate where it is
- Add some sort of indicator which window is active (scrollable)
