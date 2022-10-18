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

        self.elements: Optional[list[Element]] = None
        self.parent = parent

        if isinstance(parent, Element):
            self.widget = widget(self.parent.widget, **kwargs)
        else:
            self.widget = widget(self.parent, **kwargs)

        fallback: Optional[str] = None
        match widget.__name__:
            case "Frame":
                fallback = "Window"

        # Create a new copy of the stylesheet associated with
        # this Element or some fallback Element, then configure
        # the element.
        self.style = dict(self.get_style_of(widget.__name__, fallback))
        if self.style is not None:
            self.configure(**self.style)

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
        """Bind an event and handler to an `Element`'s widget."""
        self.widget.bind(*args)

    @dbg
    def configure(self, **kwargs):
        """Configure properties of an `Element` and its widget."""
        print(self.widget)
        for p in ("cl", "id"):
            if kwargs.get(p, None) is not None:
                self.__dict__[p] = kwargs.pop(p)

        if kwargs:
            self.style.update(kwargs)
            self.widget.configure(**kwargs)

    @dbg
    def get_style_of(
        self, name: str, fallback: Optional[str] = None
    ) -> Optional[dict[str, str]]:
        """
        Return the CSS block associated with `name` or `None`
        if it does not exist. An optional `fallback` selector
        can be provided in order to borrow another `Element`'s
        style block instead.
        """
        return self.parent.get_style_of(name) or self.parent.get_style_of(fallback)
