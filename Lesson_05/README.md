# Lesson 05: Menus and Joystick

This lesson will be a little more complex, and will have two steams, `Josytick` and `Menus`, which you can do in any order, to merge into `05_c_Menus_Joystick` at the end. And possibly a `05_d_Menus_Joystick` down the line.

## Menus

Let's start small. We want to have several pages of menus, 3 items (and late more) per page. And show which item on the current page is selected, with a `>`. `05_a_Menus.py` does the basics.

### PageX functions

There are two `drawPage_()` functions that each display the page number and 3 menu items. Based on the `menuItem` variable it shows which menu item is displayed. It's a bit fragile (since there should be a `menuItem` per page), but for now it works.

### Main loop

The main loop displays the current page, based on `pageNum` and `menuItem`. It then increments `menuItem`, and when it goes above 2, the maximum for now, it increments `pageNum` and resets `menuItem` to zero. And when `pageNum` reaches 2, it loops back to 0. A 5-second delay shows each step.

```python
pageNum = 0
menuItem = 0
while True:
    pages[pageNum]()
    time.sleep(5)
    menuItem += 1
    if menuItem == 3:
        pageNum += 1
        menuItem = 0
        if pageNum == 2:
            pageNum = 0
```

No user input for now. And no more than 3 items per page. We'll improve on that.