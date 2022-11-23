from tkinter import Tk
from tkx.core import TkxElement
from tkx.element import Element
from tkx.stylesheet import Stylesheet
import re


class Window(TkxElement, Tk):
    def __init__(self, title: str = "", stylesheet: Stylesheet | None = None):
        super().__init__()
        super().update()
        super().title(title)

        self.__cls: dict[str, set[Element]] = dict()
        self.__ids: dict[str, Element] = dict()
        self.elements: list[Element] | None = None
        self.stylesheet: Stylesheet | None = stylesheet

        # Prevent child elements from resizing the main window.
        self.pack_propagate(0)

        self.width, self.height, self.x, self.y = re.split(r"[x+]", self.geometry())

    @property
    def ids(self) -> dict[str, Element]:
        """IDs defined for elements within this `Window`."""
        return self.__ids

    @property
    def cls(self) -> dict[str, list[Element]]:
        """CSS class names and lists of `Element` instances to which they are assigned."""
        return self.__cls

    def configure(self, **kwargs):
        super().configure(**kwargs)
