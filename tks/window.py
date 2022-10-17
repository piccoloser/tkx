from tks.dbg import dbg
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

        self.elements = None
        self.stylesheet = stylesheet
        self.width, self.height, self.x, self.y = re.split("[x+]", self.geometry())

        if stylesheet is not None:
            if stylesheet.get("Window"):
                self.configure(**self.stylesheet.get("Window"))

    @dbg
    def add(self, widget: tk.Widget, **kwargs) -> Element:
        """Add a new child Element to this Window."""
        if self.elements is None:
            self.elements = []

        element = Element(widget, self, **kwargs)
        self.elements.append(element)
        element.widget.pack()
        return element

    def get_style(self, name: str) -> Optional[dict[str, str]]:
        if self.stylesheet is None:
            return None

        return self.stylesheet.get(name)
