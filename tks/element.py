import tkinter as tk


class Element:
    def __init__(
        self,
        widget: tk.Widget,
        parent: tk.Widget,
        **kwargs,
    ):
        self.id = kwargs.pop("id", None)
        self.cl = kwargs.pop("cl", None)
        self.widget = widget(parent, **kwargs)

        if parent.__dict__.get("elements") is not None:
            if parent.stylesheet is not None:
                if parent.stylesheet.get(widget.__name__):
                    self.widget.configure(**parent.stylesheet.get(widget.__name__))

    def bind(self, *args):
        self.widget.bind(*args)
