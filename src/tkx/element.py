from __future__ import annotations
from typing import Generator
from tkx.constants import ELEMENT_ONLY_PROPERTIES, INVALID_CONTAINER_PROPERTIES
from tkx.core import TkxElement, update_element, update_style
from tkx.error import DuplicateIdError
import tkinter as tk


class Element(TkxElement):
    def __init__(self, widget: tk.Widget, parent: tk.Widget, **kwargs):
        kwargs = update_element(self, **kwargs)
        parsed_kwargs = self.parse_kwargs(kwargs)

        # List of direct children of this Element.
        self.elements: list[Element] | None = None

        # Object to which this Element is added.
        self.parent = parent
        self.__iter_parent = parent  #! remove 'self'?

        self.widget = widget(self.parent.widget, parsed_kwargs)

        fallback: str | None = None

        # Style the element from its selector or the fallback.
        self.style = self.get_style_of(widget.__name__, fallback) or dict()
        self.style.update(self.parse_kwargs(kwargs))

        self.parse_id(widget.__name__)  #! Update escape clause?
        self.parse_cl()
        self.display = self.style.get("display", self.display)

        # Configure with values from CSS stylesheet.
        self.inherit_style()
        self.configure(self.style)

        # Reconfigure the widget with any provided keyword arguments.
        if kwargs:
            self.configure(parsed_kwargs)

    def bind(self, *args):
        """Bind an event and handler to an `Element`'s widget."""
        self.widget.bind(*args)

    @update_style
    def configure(self, **kwargs):
        """Configure properties of an `Element` and its widget."""
        kwargs = update_element(self, **kwargs)

        if "frame" in self.widget_name:
            kwargs.pop("fg", None)

        self.widget.configure(**kwargs)

    def parents(self) -> Generator[Element]:
        """Returns an ascending generator of an `Element`'s parents."""
        # Get a reference to the current container.
        ref = self.__iter_parent

        # If the current container has a parent, reference and return it.
        if self.__iter_parent.parent is not None:
            self.__iter_parent = self.__iter_parent.parent
            yield ref

        # Create a new parent reference to restart the generator.
        ref = self.__iter_parent
        self.__iter_parent = self.parent

        # Return the root.
        yield ref

    def parse_cl(self) -> None:
        """Apply CSS classes in the given order."""

        # If no classes are supplied, exit.
        if self.cl is None:
            return

        for cl in self.cl.split(" "):
            # If this CSS class isn't defined in the root, create a new set.
            if self.root.cls.get(cl) is None:
                self.root.cls[cl] = set()

            # Add this Element to the CSS class.
            self.root.cls[cl].add(self)

            cl_dict = self.get_style_of(f".{cl}", self.widget_name)

            # If this CSS class isn't defined in the stylesheet, exit.
            if cl_dict is None:
                return

            # Update the relevant style properties.
            self.style.update(cl_dict)

    def parse_id(self, fallback) -> None:
        if self.id is not None:
            # Raise an error if an element with this id already exists.
            if self.root.ids.get(self.id):
                raise DuplicateIdError(f'An element with id "{self.id}" already exists.')

            # If no error is raised, add this id and Element.
            self.root.ids[self.id] = self

            # Style the element from its id selector.
            self.style.update(self.get_style_of(f"#{self.id}", fallback))

    def parse_kwargs(self, kwargs) -> None:
        return {
            k: v for k, v in kwargs.items() if k in zip(INVALID_CONTAINER_PROPERTIES, ELEMENT_ONLY_PROPERTIES.keys())
        }
