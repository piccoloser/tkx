from tks.element import Element


class ClassList:
    """
    Container for CSS class names and sets of elements
    to which those class names are assigned. This object
    can be indexed into using CSS class names.

    ### Example
    ```python
    class_list["blue"] -> {element1, element2, ...}
    ```
    """

    def __init__(self):
        self.classes: dict[str, set[Element]] = dict()

    def __getitem__(self, attr: str) -> set[Element]:
        if self.classes.get(attr) is None:
            self.classes[attr] = set()

        return self.classes[attr]

    def __repr__(self):
        return f"""ClassList ({self.classes})"""
