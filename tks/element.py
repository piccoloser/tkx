from __future__ import annotations
from tks.dbg import dbg
from tks.stylesheet import Stylesheet
from typing import Optional
import tkinter as tk


class Element:
    def __init__(
        self,
        widget: tk.Widget,
        parent: tk.Widget,
        **kwargs,
    ):
        self.id = kwargs.pop("id", None)
        self.cl = kwargs.pop("cl", None)

        self.elements = None
        self.parent = parent

        if isinstance(parent, Element):
            self.widget = widget(self.parent.widget, **kwargs)
        else:
            self.widget = widget(self.parent, **kwargs)

        fallback: Optional[str] = None
        match widget.__name__:
            case "Frame":
                fallback = "Window"

        self.configure(**self.get_style(widget.__name__, fallback))

    @dbg
    def add(self, widget: tk.Widget, **kwargs) -> Element:
        """Add a new child Element to this Element."""
        if self.elements is None:
            self.elements = []

        element = Element(widget, self, **kwargs)
        self.elements.append(element)
        element.widget.pack()
        return element

    @dbg
    def bind(self, *args):
        self.widget.bind(*args)

    @dbg
    def configure(self, **kwargs):
        for p in ("cl", "id"):
            if kwargs.get(p, None) is not None:
                self.__dict__[p] = kwargs[p]

        if kwargs:
            self.widget.configure(**kwargs)

    @dbg
    def get_style(
        self, name: str, fallback: Optional[str] = None
    ) -> Optional[Stylesheet]:
        return self.parent.get_style(name) or self.parent.get_style(fallback)

    @property
    def parent(self) -> tk.Widget or Element:
        return self.__parent

    @parent.setter
    def parent(self, item: tk.Widget or Element) -> None:
        self.__parent = item
