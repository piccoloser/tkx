from __future__ import annotations
from tkinter import Widget
from typing import Optional
from tks.constants import NON_STYLE_CONFIG_OPTIONS


def tks_element(base: object):
    class TksElement(base):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def add(self, widget: Widget, **kwargs):
            """
            Creates a new child `Element` with the provided
            keyword arguments and adds it to the caller.
            Returns the added `Element`.
            """
            from tks.element import Element

            if self.elements is None:
                self.elements = []

            element = Element(widget, self, **kwargs)
            self.elements.append(element)

            element.widget.pack()

            return element

        def get_style_of(
            self, name: str, fallback: Optional[str] = None
        ) -> dict[str, str]:
            if self.__dict__.get("parent"):
                return (
                    self.parent.get_style_of(name)
                    or self.parent.get_style_of(fallback)
                    or dict()
                )

            if self.stylesheet is None:
                return dict()

            return self.stylesheet.get(name) or dict()

        def root(self):
            if self.__dict__.get("parent"):
                return self.parent.root()

            return self

    return TksElement


def parse_css_vars(fn):
    def func(self, **kwargs):
        if self.style is None:
            self.style = dict()

        kwargs = self.root().stylesheet.format_properties(kwargs)
        self.style.update(kwargs)

        # Remove keys not associated with style.
        self.style = dict(
            filter(
                lambda i: i[0] not in NON_STYLE_CONFIG_OPTIONS,
                self.style.items(),
            )
        )

        fn(self, **kwargs)

    return func
