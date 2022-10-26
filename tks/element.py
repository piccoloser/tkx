from __future__ import annotations
from typing import Generator
from tks.core import TksElement, update_style
from tks.error import DuplicateIdError
import tkinter as tk


class Element(TksElement):
    def __init__(self, widget: tk.Widget, parent: tk.Widget, **kwargs):

        # CSS id and class values. None if not provided.
        self.id = kwargs.pop("id", None)
        self.cl = kwargs.pop("cl", None)

        # List of child Elements of this Element.
        self.elements: list[Element] | None = None

        # Object to which this Element is added.
        self.parent = parent

        # If self.parent is an Element, use its widget attribute
        # as the parent of self.widget. Elements by themselves do
        # not have the tk attribute which tkinter requires for a
        # widget to be added to another object.
        if isinstance(parent, Element):
            self.widget = widget(self.parent.widget, **kwargs)

        # If self.parent is not an Element, it is assumed that it
        # is a Window, which directly inherits the tk attribute
        # from its superclass (tk.Tk).
        else:
            self.widget = widget(self.parent, **kwargs)

        if self.id is not None:
            # Raise an error if an element with this id already exists.
            if self.root.ids.get(self.id):
                raise DuplicateIdError(f'An element with id "{self.id}" already exists.')

            # If no error is raised, add this id and Element.
            self.root.ids[self.id] = self

            # Style the element from its id selector.
            self.style = self.get_style_of(f"#{self.id}", widget.__name__)

        elif self.cl is not None:
            # If this CSS class hasn't been defined, create a new set.
            if self.root.cls.get(self.cl) is None:
                self.root.cls[self.cl] = set()

            # Add this Element to the CSS class.
            self.root.cls[self.cl].add(self)

            # Style the element from its class selector.
            self.style = self.get_style_of(f".{self.cl}", widget.__name__)

        else:
            fallback: str | None = None
            if widget.__name__ == "Frame":
                self.widget.pack_propagate(0)

            # Style the element from its selector or the fallback.
            self.style = self.get_style_of(widget.__name__, fallback)

        # Configure with values from CSS stylesheet.
        self.inherit_style()
        self.configure(self.style)

        # Reconfigure the widget with any provided keyword arguments.
        if kwargs:
            self.configure(kwargs)

    def bind(self, *args):
        """Bind an event and handler to an `Element`'s widget."""
        self.widget.bind(*args)

    @update_style
    def configure(self, **kwargs):
        """Configure properties of an `Element` and its widget."""
        for p in ("cl", "id"):
            self.__dict__[p] = kwargs.pop(p, None)

        if "frame" in self.widget_name:
            kwargs.pop("fg", None)

        self.widget.configure(**kwargs)

    def parents(self) -> Generator[Element]:
        parent = self.parent

        if parent.parent is not None:
            yield parent.parent

        else:
            yield parent
