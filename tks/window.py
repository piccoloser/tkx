from tks.element import Element
from tks.stylesheet import Stylesheet
from typing import Optional

import re
import tkinter as tk


class Window(tk.Tk):
    def __init__(self, title: str = "", stylesheet: Optional[Stylesheet] = None):
        super().__init__()
        super().update()
        super().title(title)

        # # Prevent child elements from resizing main window.
        self.pack_propagate(0)

        self.elements = list()
        self.stylesheet = stylesheet
        self.width, self.height, self.x, self.y = re.split("[x+]", self.geometry())

        if stylesheet is not None:
            if stylesheet.get("Window"):
                self.configure(**self.stylesheet.get("Window"))

    def add(self, widget: tk.Widget, **kwargs) -> Element:
        """Add a new child element to this window."""
        element = Element(widget, self, **kwargs)
        self.elements.append(element)
        element.widget.pack()
        return element
