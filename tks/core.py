from __future__ import annotations
from tkinter import Widget
from typing import Any, Callable
from tks.constants import (
    CSS_PROPERTY_NAME_TRANSLATIONS,
    INHERITED_PROPERTIES,
    NON_STYLE_CONFIG_OPTIONS,
)


translate_css = lambda x: CSS_PROPERTY_NAME_TRANSLATIONS[x]


class TksElement:
    def add(self, widget: Widget, **kwargs):
        """
        Creates a new child `Element` with the provided
        keyword arguments and adds it to the caller.
        Returns the added `Element`.
        """
        from tks.element import Element

        if self.elements is None:
            self.elements = []

        kwargs = parse_css_kwargs(self, **kwargs)
        element = Element(widget, self, **kwargs)
        self.elements.append(element)

        element.widget.pack()

        return element

    def get_style_of(self, name: str, fallback: str | None = None) -> dict[str, str]:
        """
        Returns the style dictionary associated with the given widget name
        if it can be found in the root `Window`'s stylesheet. Accepts an
        optional `fallback` object to use another element's style.

        Returns `None` if no style is found.
        """
        if self.parent is not None:
            return self.parent.get_style_of(name) or self.parent.get_style_of(fallback) or dict()

        if self.stylesheet is None:
            return None

        if self.stylesheet.get(name) is None:
            return

        # Return a copy of the style dictionary.
        return dict(self.stylesheet.get(name))

    def inherit_style(self) -> None:
        if self.style is None:
            self.style = dict()

        for p in INHERITED_PROPERTIES:
            if self.style.get(translate_css(p)) is None:
                if self.parent.style.get(translate_css(p)) is None:
                    continue

                self.style[translate_css(p)] = self.parent.style.get(translate_css(p))

    @property
    def root(self):
        """Returns the `root` Window."""
        if self.__dict__.get("parent"):
            return self.parent.root
        return self

    @property
    def widget_name(self):
        if self.__dict__.get("widget") is not None:
            return str(self.widget).split(".")[-1]

    def __getattr__(self, attr: str) -> Any | None:
        return self.__dict__.get(attr)

    def __getitem__(self, attr: str) -> Any | None:
        return self.__dict__.get(attr)


def parse_css_kwargs(obj, **kwargs) -> dict[str, str]:
    """
    Parse a set of keyword arguments as though they were
    CSS variables. Possible values include:
    * Percent values (`width: 50%` -> `width={self.parent|root}.width / 2`)
    """
    for k, v in kwargs.items():
        if "%" in str(v):
            percent = float(v.replace("%", ""))

            if obj.parent is not None:
                target = obj.parent

            if target[k] is None:
                target = obj.root

            amount = float(target[k])
            total = float(amount / 100) * percent
            kwargs[k] = str(int(total))

    return obj.root.stylesheet.format_properties(kwargs)


def update_style(fn):
    """
    Decorates the `configure` method of a class which inherits from
    `TksElement`.

    Takes a style dictionary and/or keyword arguments, then parses
    the given values as CSS before configuring the widget wrapped by
    the caller. Dictionary values are overwritten by keyword arguments.

    #### The following examples require `--red` to be defined in the stylesheet.
    ### Example 1

    ```python
    my_element.configure(color="var(--red)")
    ```

    becomes `my_element.configure(fg="#f00")`

    ### Example 2

    ```python
    my_style = {"color": "var(--red)"}
    my_element.configure(my_style)
    ```

    becomes `my_element.configure(fg="#f00")`

    ### Example 3

    ```python
    my_style = {"color": "var(--red)"}
    my_element.configure(my_style, width=50)
    ```

    becomes `my_element.configure(fg="#f00", width=50)`
    """

    def func(self, args: dict[str, Any] | None = None, **kwargs) -> Callable:
        # If both a positional dictionary and keyword arguments
        # are provided, update the dictionary with the provided
        # keyword arguments.
        if args is not None:
            args.update(kwargs)
            kwargs = args

        # Create self.style if it doesn't already exist.
        if self.style is None:
            self.style = dict()

        # If there is no stylesheet or if no arguments exist, exit.
        if self.root.stylesheet is None or not any((args, kwargs)):
            return

        kwargs = parse_css_kwargs(self, **kwargs)

        self.style.update(kwargs)

        # Remove keys not associated with style.
        self.style = dict(filter(lambda i: i[0] not in NON_STYLE_CONFIG_OPTIONS, self.style.items()))

        # Call the original configure method.
        fn(self, **kwargs)

    return func
