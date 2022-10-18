from tks.core import parse_css_vars, tks_element
from tks.stylesheet import Stylesheet
from typing import Optional
import re
import tkinter as tk


@tks_element
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

    @parse_css_vars
    def configure(self, **kwargs):
        super().configure(**kwargs)
