from tkx.core import update_style, TkxElement
from tkx.element import Element
from tkx.stylesheet import Stylesheet
import re
import tkinter as tk


class Window(TkxElement, tk.Tk):
    def __init__(self, title: str = "", stylesheet: Stylesheet | None = None):
        super().__init__()

        # Update window geometry.
        super().update()

        # Set the window title.
        super().title(title)

        # Prevent child elements from resizing the main window.
        self.pack_propagate(0)

        # @property self.cls is a dictionary where the key is
        # the class name and the value is a set containing all
        # Elements with that class.
        self.__cls: dict[str, set[Element]] = None

        # @property self.ids is a dictionary where the key is
        # the id and the value is the one Element with that id.
        self.__ids: dict[str, Element] = None

        # List of direct children of this window.
        self.elements: list[Element] = None

        # Style dictionary associated with this window.
        self.stylesheet: Stylesheet | None = stylesheet

        # tk.Tk().geometry returns a str = "{width}x{height}+{x}+{y}".
        # Split the string along "x" and "+", then assign those values.
        self.width, self.height, self.x, self.y = re.split("[x+]", self.geometry())

        if stylesheet is not None:
            self.configure(self.stylesheet.get("Window"))

    @property
    def ids(self) -> dict[str, Element] | None:
        if self.__ids is None:
            self.__ids = dict()
        return self.__ids

    @property
    def cls(self) -> dict[str, list[Element]] | None:
        if self.__cls is None:
            self.__cls = dict()
        return self.__cls

    @update_style
    def configure(self, **kwargs):
        kwargs.pop("fg", None)
        super().configure(**kwargs)
