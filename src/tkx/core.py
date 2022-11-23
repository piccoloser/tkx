from __future__ import annotations
from tkinter import Widget
from tkx.constants import (
    CSS_PROPERTY_NAME_TRANSLATIONS,
    CSS_PROPERTY_VALUE_TRANSLATIONS,
    ELEMENT_ONLY_PROPERTIES,
    INVALID_CONTAINER_PROPERTIES,
    NON_STYLE_CONFIG_OPTIONS,
    STYLE_CONFIG_OPTIONS,
)
from tkx.error import InvalidDisplayError
from typing import Any, Callable, Literal
import re


def css_name(name: str) -> str | None:
    return CSS_PROPERTY_NAME_TRANSLATIONS.get(name)


class TkxElement:
    def __init__(self):
        super().__init__()
        self.__display: Literal["block", "flex", "grid", "none"] = "block"
        self.__parent: TkxElement | None = None
        self.__style: dict[str, str] | None = None
        self.__widget: Widget | None = None

    def __getattr__(self, attr: str) -> Any | None:
        if self[attr] is None and self["widget"] is not None:
            return getattr(self.widget, attr)
        return self[attr]

    def __getitem__(self, attr: str) -> Any | None:
        return self.__dict__.get(attr)

    def __setitem__(self, key: str, value: Any) -> None:
        self.__dict__[key] = value

    def add(self, widget: Widget, **kwargs) -> None:
        from tkx.element import Element

        if self.elements is None:
            self.elements = []

        element = Element(widget, self, **self.parse_tk_args(kwargs))

        self.elements.append(element)

        self.set_widget(element)

        return element

    @property
    def display(self) -> Literal["block", "flex", "grid", "none"]:
        """The CSS display value of a tkx `Element`. Default is `"block"`."""
        return self.__display

    @display.setter
    def display(self, value: Literal["block", "flex", "grid", "none"]) -> None:
        self.__display = value

    def get_style_of(self, name: str, fallback: str | None = None) -> dict[str, str] | None:
        """
        Returns the style dictionary associated with the given name if it can be found in the `Stylesheet` of the root
        `Window`. Accepts an optional `fallback` parameter in case the former is not found. If not found, returns
        `None`.

        Parameters
        - name: `str` - Name to search the stylesheet for.
        - fallback: `str | None` - Alternate style to search for if `name` is not found.
        """
        if self.parent is not None:
            return self.parent.get_style_of(name) or self.parent.get_style_of(fallback) or None

        if self.stylesheet is None or self.stylesheet.get(name) is None:
            return None

        return dict(self.stylesheet.get(name))

    @property
    def parent(self) -> TkxElement | None:
        """The container of a tkx `Element`. Returns `None` for tkx `Window` elements."""
        return self.__parent

    @parent.setter
    def parent(self, value: TkxElement) -> None:
        self.__parent = value

    def parse_kwargs(self, kwargs) -> dict[str, Any]:
        return {
            k: v for k, v in kwargs.items() if k in zip(INVALID_CONTAINER_PROPERTIES, ELEMENT_ONLY_PROPERTIES.keys())
        }

    def parse_tk_args(self, kwargs) -> dict[str, Any]:
        return {k: v for k, v in kwargs.items() if k in zip(NON_STYLE_CONFIG_OPTIONS, STYLE_CONFIG_OPTIONS)}

    @property
    def root(self) -> TkxElement:
        """Returns the root `Window` of the application."""
        return self.parent or self

    def set_widget(self, element, **kwargs):
        if "label" in element.widget_name:
            if self.text_anchor is not None:
                element.widget.configure(anchor=self.text_anchor)

        if self.parent is None or self.display == "block":
            element.widget.pack(fill="x", **kwargs)

        elif self.display == "flex":
            element.widget.grid(row=0, column=len(self.elements), **kwargs)

        elif self.display == "grid":
            try:
                element.widget.grid(
                    row=(len(self.elements) - 1) // int(self.column_count),
                    column=(len(self.element) - 1) % int(self.column_count),
                    **kwargs,
                )

            except AttributeError as e:
                raise InvalidDisplayError(
                    f'Error creating element with id "{self.id}" and class "{self.cl}": {e}\n'
                    "CSS display: grid cannot be declared without also declaring CSS column-count."
                )

        else:
            raise NotImplementedError()

    @property
    def style(self) -> dict[str, str] | None:
        """Returns the style dictionary associated with this element or an empty `dict[str, str]`."""
        if self.__style is None:
            self.__style: dict[str, str] = dict()
        return self.__style

    @style.setter
    def style(self, value: dict[str, str] | None) -> None:
        self.__style = value

    @property
    def tk_args(self) -> dict[str, Any]:
        """Returns the tk-specific arguments passed to this element."""
        return self.__tk_args

    @property
    def widget(self) -> Widget | None:
        """Returns the tk `Widget` associated with this element or `None`."""
        return self.__widget

    @widget.setter
    def widget(self, value: Widget) -> None:
        self.__widget = value

    @property
    def widget_name(self) -> str | None:
        """Returns the lowercase name of this element's tk `Widget` or `None`."""
        if self.widget is None:
            return None
        return re.search(r"\w+", str(self.widget).split(".")[-1])[0]


def parse_css_kwargs(element, **kwargs) -> dict[str, str]:
    if kwargs.pop("padding", None) is not None:
        pass

    for k, v in kwargs.items():
        pass

    kwargs = {k: CSS_PROPERTY_VALUE_TRANSLATIONS.get(v) or v for k, v in kwargs.items()}

    return element.root.stylesheet.format_properties(kwargs)


def update_element(element, kwargs) -> dict[str, Any]:
    for property, default in ELEMENT_ONLY_PROPERTIES.items():
        value = kwargs.pop(property, default)

        # Prevent default from overriding explicit values.
        current = getattr(element, property)
        if current is not None and current != value:
            continue

        setattr(element, property, value)

    return kwargs


def update_style(fn):
    def inner(self, args: dict[str, Any] | None = None, **kwargs) -> Callable:
        if args is not None:
            args.update(kwargs)
            kwargs = args

        if self.root.stylesheet is None or not any((args, kwargs)):
            return

        kwargs = parse_css_kwargs(self, kwargs)
        self.style.update(kwargs)

        update_element(self, self.style)

        fn(self, **kwargs)

    return inner
