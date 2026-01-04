# Intermezzo!

Let's have a little fun before going on with the regular lessons. I have this MAX7219 module that features 64 red LEDs, 8 by 8. No choice of colour (except when buying it) so it's not an RGB LED thing, but these can be chained too, and each LED is addressable separately.

Fortunately, there's a library for this – there always is! – and it uses MicroPython's `framebuffer`, which is the internal library for basic screen drawing (also used for OLEDs). So it gives us a lot of graphic basic functions:

```python
  self.framebuf = fb
  # Provide methods for accessing FrameBuffer graphics primitives. This is a workround
  # because inheritance from a native class is currently unsupported.
  # http://docs.micropython.org/en/latest/pyboard/library/framebuf.html
  self.fill = fb.fill  # (col)
  self.pixel = fb.pixel # (x, y[, c])
  self.hline = fb.hline  # (x, y, w, col)
  self.vline = fb.vline  # (x, y, h, col)
  self.line = fb.line  # (x1, y1, x2, y2, col)
  self.rect = fb.rect  # (x, y, w, h, col)
  self.fill_rect = fb.fill_rect  # (x, y, w, h, col)
  self.text = fb.text  # (string, x, y, col=1)
  self.scroll = fb.scroll  # (dx, dy)
  self.blit = fb.blit  # (fbuf, x, y[, key])
```

So the max7129 library itself only takes care of turning "pixels" (ie individual LEDs) on and off, which is done in the `show()` function. Everything else is done by the framebuffer library.

We are going to display a string, here `Kongduino` of course! scrolling it left. the `display.text()`, which we already saw in the code for the OLED, takes a string, a left position, a top position, and wrap (which here isn't necessary). So the easiest way to scroll the string is to decrease the X index, 72 times (9 characters for `Kongduino` times 8 columns), and display the string at an increasingly negative offset. We start at 0 and will end up at -71.


```python
start = 0
for x in range(72):
    display.fill(0)
    display.text("Kongduino", start, 0, 1)
    display.show()
    time.sleep(0.1)
    start -= 1
```

![MAX7219_Demo](../Assets/MAX7219_Demo.gif)