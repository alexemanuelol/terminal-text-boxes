## TODOs
- Add functionality for stackable boxes in height.
- Test the framework on all OS, Linux, Windows, MacOS.

- Fix Linux curses resize does not occur when terminal size change (KEY_RESIZE). UPDATE: Seems like this is because the key handler function is called as a seperate thread. When running the key handler function as a regular function, resize is possible.
