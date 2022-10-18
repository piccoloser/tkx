from __future__ import annotations
from tks.core import parse_css_vars, tks_element
from tks.dbg import dbg
from typing import Optional
import tkinter as tk


@tks_element
class Element:
    def __init__(self, widget: tk.Widget, parent: tk.Widget, **kwargs):
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
    def bind(self, *args):
        """Bind an event and handler to an `Element`'s widget."""
        self.widget.bind(*args)

    @parse_css_vars
    def configure(self, **kwargs):
        """Configure properties of an `Element` and its widget."""
        for p in ("cl", "id"):
            if kwargs.get(p, None) is not None:
                self.__dict__[p] = kwargs.pop(p)

        self.widget.configure(**kwargs)
