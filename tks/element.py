from __future__ import annotations
from tks.core import update_style, tks_element
from typing import Optional
import tkinter as tk


@tks_element
class Element:
    def __init__(self, widget: tk.Widget, parent: tk.Widget, **kwargs):
        self.id = kwargs.pop("id", None)
        self.cl = kwargs.pop("cl", None)

        self.elements: Optional[list[Element]] = None
        self.parent = parent

        if self.id is not None:
            self.root.ids[self.id] = self

        if isinstance(parent, Element):
            self.widget = widget(self.parent.widget, **kwargs)
        else:
            self.widget = widget(self.parent, **kwargs)

        fallback: Optional[str] = None
        if widget.__name__ == "Frame":
            fallback = "Window"

        # Create a new copy of the stylesheet associated with
        # this Element or some fallback Element, then configure
        # the element.
        self.style = dict(self.get_style_of(widget.__name__, fallback))
        if self.style is not None:
            self.configure(**self.style)

        # Reconfigure the widget with any provided keyword arguments.
        if kwargs:
            self.configure(**kwargs)

    def bind(self, *args):
        """Bind an event and handler to an `Element`'s widget."""
        self.widget.bind(*args)

    @update_style
    def configure(self, **kwargs):
        """Configure properties of an `Element` and its widget."""
        for p in ("cl", "id"):
            self.__dict__[p] = kwargs.pop(p, None)

        self.widget.configure(**kwargs)
