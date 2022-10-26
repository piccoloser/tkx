from __future__ import annotations
from tks.core import TksElement, update_style
from tks.error import DuplicateIdError
import tkinter as tk


class Element(TksElement):
    def __init__(self, widget: tk.Widget, parent: tk.Widget, **kwargs):
        self.id = kwargs.pop("id", None)
        self.cl = kwargs.pop("cl", None)

        self.elements: list[Element] | None = None
        self.parent = parent

        if isinstance(parent, Element):
            self.widget = widget(self.parent.widget, **kwargs)
        else:
            self.widget = widget(self.parent, **kwargs)

        if self.id is not None:
            # Raise an error if an element with this id already exists.
            if self.root.ids.get(self.id):
                raise DuplicateIdError(f'An element with id "{self.id}" already exists.')

            self.root.ids[self.id] = self

            # Type cast here to copy the output to a new instance variable.
            # TODO: Check if this type cast can be moved to tks.core.tks_element
            self.style = dict(self.get_style_of(f"#{self.id}", widget.__name__))

        elif self.cl is not None:
            if self.root.cls.get(self.cl) is None:
                self.root.cls[self.cl] = set()
            self.root.cls[self.cl].add(self)
            self.style = dict(self.get_style_of(f".{self.cl}", widget.__name__))

        else:
            fallback: str | None = None
            if widget.__name__ == "Frame":
                fallback = "Window"

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
