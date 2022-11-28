from __future__ import annotations
from tkinter import Widget
from tkx.constants import (
    ELEMENT_ONLY_PROPERTIES,
    TK_PROPERTIES,
    TKX_PROPERTIES,
)
from tkx.core import TkxElement
from tkx.error import DuplicateIdError
from typing import Generator


class Element(TkxElement):
    def __init__(self, widget: Widget, parent: Widget, **kwargs):
        self.tk_properties = self.parse_tk_properties(kwargs)
        self.tkx_properties = self.parse_tkx_properties(kwargs)

        # Get default and explicit values.
        for property, default in ELEMENT_ONLY_PROPERTIES.items():
            self[property] = self.tkx_properties.get(property) or default

        self.elements: list[Element] | None = None
        fallback: str | None = None

        self.parent = parent
        self.__iter_parent = parent

        self.widget = widget(self.parent.widget, **self.tk_properties)

        self.style = self.get_style_of(widget.__name__, fallback) or dict()
        self.style.update(self.tkx_properties)

        if kwargs.get("id") is not None:
            self.parse_id()

        if kwargs.get("cl") is not None:
            self.parse_cl()

        self.configure(**self.style)

    def bind(self, *args) -> None:
        """Bind an event and handler to the tk `Widget` of a tkx `Element`."""
        self.widget.bind(*args)

    def configure(self, **kwargs):
        """Configure properties of an `Element` and its widget."""
        self.tk_properties.update({k: v for k, v in kwargs.items() if k in TK_PROPERTIES})
        self.tkx_properties.update({k: v for k, v in kwargs.items() if k in TKX_PROPERTIES})
        self.widget.configure(self.tk_args, **self.tk_properties)

    def parents(self) -> Generator[Element]:
        """Returns an ascending `Generator` over the parents of an `Element`."""
        ref = self.__iter_parent

        if self.__iter_parent.parent is not None:
            self.__iter_parent = self.__iter_parent.parent
            yield ref

        ref = self.__iter_parent
        self.__iter_parent = self.parent
        yield ref

    def parse_cl(self) -> None:
        """Apply CSS classes in the given order."""
        if self.cl is None:
            return

        for cl in self.cl.split(" "):
            if self.root.cls.get(cl) is None:
                self.root.cls[cl] = set()

            self.root.cls[cl].add(self)

            cl_dict = self.get_style_of(f".{cl}", self.widget_name)

            if cl_dict is None:
                return

            self.style.update(cl_dict)

    def parse_id(self) -> None:
        """Check that the ID of this element is valid and update `self.style`."""
        if self.root.ids.get(self.id):
            raise DuplicateIdError(f'An Element with ID "{self.id}" already exists.')

        self.root.ids[self.id] = self

        self.style.update(self.get_style_of(f"#{self.id}", self.widget_name))
