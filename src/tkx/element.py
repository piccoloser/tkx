from __future__ import annotations
from typing import Generator
from tkx.constants import INVALID_CONTAINER_PROPERTIES
from tkx.core import TkxElement, translate_css, update_element, update_style
from tkx.error import DuplicateIdError
import tkinter as tk


class Element(TkxElement):
    def __init__(self, widget: tk.Widget, parent: tk.Widget, **kwargs):
        explicit_display: bool = "display" in kwargs.keys()
        self.display = kwargs.pop("display", "block")
        other_kwargs = dict()

        # Handle keyword arguments tkinter doesn't recognize.
        if widget is tk.Frame:
            for k in INVALID_CONTAINER_PROPERTIES:
                value = kwargs.pop(k, None)
                if value is not None:
                    other_kwargs[translate_css(k)] = value

        kwargs = update_element(self, **kwargs)

        # List of direct children of this Element.
        self.elements: list[Element] | None = None

        # Object to which this Element is added.
        self.parent = parent
        self.__iter_parent = self.parent

        # Use self.parent's widget attribute as the parent of self.widget.
        # Elements by themselves do not have the tk attribute which
        # tkinter requires for a widget to be added to another object.
        if self.parent.widget is not None:
            self.widget = widget(self.parent.widget, **kwargs)

        # If self.parent has no widget attribute, it is assumed that it
        # is a Window, which directly inherits the tk attribute from its
        # superclass (tk.Tk).
        else:
            self.widget = widget(self.parent, **kwargs)

        fallback: str | None = None

        # Style the element from its selector or the fallback.
        self.style = self.get_style_of(widget.__name__, fallback) or dict()
        self.style.update(other_kwargs)

        if explicit_display:
            self.style["display"] = self.display
            print(self.display)

        if self.id is not None:
            # Raise an error if an element with this id already exists.
            if self.root.ids.get(self.id):
                raise DuplicateIdError(f'An element with id "{self.id}" already exists.')

            # If no error is raised, add this id and Element.
            self.root.ids[self.id] = self

            # Style the element from its id selector.
            self.style.update(self.get_style_of(f"#{self.id}", widget.__name__))

        # Apply one or more classes if applicable.
        self.parse_cl()

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

    def parse_cl(self):
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
