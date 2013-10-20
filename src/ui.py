#!/usr/bin/env python

"""
Simple UI
"""

import assets
import inputs

class Widget(object):
    def __init__(self, x, y):
        super(Widget, self).__init__()
        self.x = x
        self.y = y
        self.interactive = False

    def update(self, td):
        pass

    def draw(self, surface, x, y):
        pass

    def interact(self):
        pass


class Text(Widget):
    def __init__(self, x, y, text, font=None):
        super(Text, self).__init__(x, y)
        self.interactive = False
        if font is None:
            font = assets.getFont(None, 10)
        self.font = font
        self.setText(text)

    def setText(self, text, color=(255,255,255)):
        self.text = text
        self.text_image = self.font.render(text, False, color)

    def draw(self, surface, x, y):
        surface.blit(self.text_image, (x + self.x, y + self.y))


class Button(Text):
    def __init__(self, x, y, text, command, font=None):
        super(Button, self).__init__(x, y, text, font)
        self.command = command
        self.interactive = True

    def interact(self):
        self.command()


class UI:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.widgets = []
        self.selected = 0
        self.pointer = assets.getImage("graphics/pointer.png")

    def add(self, widget):
        self.widgets.append(widget)
        if not self.widgets[self.selected].interactive:
            self.selected += 1

    def update(self, td):
        v = inputs.getVerticalPress()

        if v < -0.01:
            self.selected = (self.selected - 1) % len(self.widgets)
            while not self.widgets[self.selected].interactive:
                self.selected = (self.selected - 1) % len(self.widgets)

        if v > 0.01:
            self.selected = (self.selected + 1) % len(self.widgets)
            while not self.widgets[self.selected].interactive:
                self.selected = (self.selected + 1) % len(self.widgets)

        if inputs.getFirePress() or inputs.getJumpPress() or inputs.getPausePress():
            self.widgets[self.selected].interact()

        for widget in self.widgets:
            widget.update(td)

    def draw(self, surface):
        for widget in self.widgets:
            widget.draw(surface, self.x, self.y)

        selected = self.widgets[self.selected]
        surface.blit(self.pointer, (self.x + selected.x - 10, self.y + selected.y + 1))
