# Property name translations.
CSS_PROPERTY_NAME_TRANSLATIONS: dict[str, str] = {
    "background": "bg",
    "background-color": "bg",
    "border-style": "relief",
    "border-width": "bd",
    "color": "fg",
    "column-count": "column_count",
    "column-width": "column_width",
    "text-align": "text_anchor",
}

# Property value translations.
CSS_PROPERTY_VALUE_TRANSLATIONS: dict[str, str] = {
    "bottom": "s",
    "bottom-left": "sw",
    "bottom-right": "se",
    "center": "center",
    "origin": "n",
    "left": "w",
    "right": "e",
    "top": "n",
    "top-left": "nw",
    "top-right": "ne",
}

# Properties that apply only to tkx Elements [k: name, v: default].
ELEMENT_ONLY_PROPERTIES: dict[str, str | None] = {
    "cl": None,
    "column_count": None,
    "column_width": None,
    "display": "block",
    "id": None,
    "text_anchor": None,
}

# Supported properties which inherit from
# the parent element by default.
INHERITED_PROPERTIES: list[str] = [
    "background",
    "color",
]

# Properties not supported by container objects.
INVALID_CONTAINER_PROPERTIES: list[str] = [
    "color",
]

# Regular expressions to help parse CSS.
MATCH_COMMENT: str = r"/\*.+?\*/"
MATCH_BLOCK: str = r"\{.*?\}"
MATCH_BRACES: str = r"[\{\}]"
MATCH_DELIMITER_SPACE: str = r"(?<=[:,])\s"
MATCH_SELECTOR: str = r"[:\w\.#\-]+\{"
MATCH_SPACE: str = r"\s"
MATCH_VAR_NAME: str = r"--\w+"

# tk.Widget options not associated with style.
NON_STYLE_CONFIG_OPTIONS: set[str] = {
    "class",
    "colormap",
    "command",
    "container",
    "default",
    "from_",
    "repeatdelay",
    "repeatinterval",
    "takefocus",
    "text",
    "textvariable",
    "to",
    "visual",
}

# tk.Widget options associated with style.
STYLE_CONFIG_OPTIONS: set[str] = {
    "bd",
    "borderwidth",
    "relief",
    "background",
    "bg",
    "cursor",
    "height",
    "highlightbackground",
    "highlightcolor",
    "highlightthickness",
    "padx",
    "pady",
    "width",
}
