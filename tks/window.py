from tks.class_list import ClassList
from tks.core import update_style, tks_element
from tks.element import Element
from tks.stylesheet import Stylesheet
import re
import tkinter as tk


@tks_element
class Window(tk.Tk):
    def __init__(self, title: str = "", stylesheet: Stylesheet | None = None):
        super().__init__()
        super().update()
        super().title(title)

        # Prevent child elements from resizing the main window.
        self.pack_propagate(0)

        self.__cls = None
        self.__ids = None
        self.elements = None

        self.stylesheet = stylesheet
        self.width, self.height, self.x, self.y = re.split("[x+]", self.geometry())
        self.style = None

        if stylesheet is not None:
            if stylesheet.get("Window"):
                self.configure(**self.stylesheet.get("Window"))

    @property
    def ids(self) -> dict[str, Element] | None:
        if self.__ids is None:
            self.__ids = dict()
        return self.__ids

    @property
    def cls(self) -> dict[str, list[Element]] | None:
        if self.__cls is None:
            self.__cls = ClassList()
        return self.__cls

    @update_style
    def configure(self, **kwargs):
        super().configure(**kwargs)
