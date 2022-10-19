from __future__ import annotations
from tkinter import Widget
from typing import Optional
from tks.constants import NON_STYLE_CONFIG_OPTIONS
from tks.dbg import dbg


@dbg(False)
def tks_element(base: object):
    """
    Decorates a tks class in order to add the following instance methods:
    * `self.add(widget, **kwargs)`
    * `self.get_style_of(name, fallback)`
    * `self.root()`

    The `add` method creates a new tks `Element` which contains the
    provided `tk.Widget` as a direct child element. Keyword arguments
    can be passed to the method which will be applied to the resulting
    widget.

    The `get_style_of` method recursively asks for the style associated
    with the provided `name` and optional `fallback` arguments. If found,
    a `dict[str, str]` will be returned. Otherwise, this method returns
    `None`.

    The `root` method returns the `Window` which contains everything.
    """

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
                return None

            return self.stylesheet.get(name)

        def root(self):
            if self.__dict__.get("parent"):
                return self.parent.root()

            return self

    return TksElement


@dbg(False)
def configure_style(fn):
    """
    Decorates the `configure` method of a class which is decorated with
    `tks.core.tks_element`.

    Arguments passed to a method with this decorator are stringified,\
    and CSS variables are translated to their actual value in the\
    stylesheet's `:root`.

    ### Example

    `my_element.configure(color="var(--red)")`

    becomes `my_element.configure(color="#f00")`
    
    This only works if `--red` is defined in the stylesheet.
    """

    def func(self, **kwargs):
        if self.style is None:
            self.style = dict()

        if self.root().stylesheet is None:
            return

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
