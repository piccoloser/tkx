from tks.constants import NON_STYLE_CONFIG_OPTIONS
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

        # Prevent child elements from resizing the main window.
        self.pack_propagate(0)

        self.elements = None
        self.stylesheet = stylesheet
        self.width, self.height, self.x, self.y = re.split("[x+]", self.geometry())
        self.style = None

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

        # This will likely change in the future.
        element.widget.pack()

        return element

    def configure(self, **kwargs):
        if self.style is None:
            self.style = dict()

        kwargs = self.stylesheet.format_properties(kwargs)
        self.style.update(kwargs)

        # Remove keys not associated with style from `self.style`.
        self.style = dict(
            filter(
                lambda i: i[0] not in NON_STYLE_CONFIG_OPTIONS,
                self.style.items(),
            )
        )

        # Apply window properties.
        super().configure(**kwargs)
        
    def get_style_of(self, name: str) -> Optional[dict[str, str]]:
        """
        Return the CSS block associated with `name` or `None` if
        either the CSS block or the stylesheet does not exist.
        """
        if self.stylesheet is None:
            return None

        return self.stylesheet.get(name)

    def root(self):
        return self
