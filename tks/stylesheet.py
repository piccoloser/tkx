from pathlib import Path
from tks.constants import (
    MATCH_BLOCK,
    MATCH_BRACES,
    MATCH_COMMENT,
    MATCH_DELIMITER_SPACE,
    MATCH_SELECTOR,
    MATCH_SPACE,
    MATCH_VAR_NAME,
)
from typing import Optional
import re


# Property name translations.
CSS_TO_TK = {
    "background": "bg",
    "background-color": "bg",
    "border-style": "relief",
    "border-width": "bd",
    "color": "fg",
}


class Stylesheet:
    """
    Basic CSS parser and container for parsed styles.

    Simply creating this class with a valid CSS filepath
    will make it available for use in your code. Reading
    and parsing happens upon instantiation.
    """

    def __init__(self, source_path: str):
        self.styles = dict()

        if not Path(source_path).is_file():
            raise ValueError("Stylesheet expects a valid file path.")

        # Minify and store the provided CSS.
        self.source_min = self.minify_css(source_path)

        # Parse and store the minified CSS into `self.styles`.
        for selector, block in zip(self.get_selectors(), self.get_blocks()):
            self.styles[selector] = self.parse_block(block)

    def format_properties(self, properties: dict[str, str]) -> dict[str, str]:
        return {k: self.var(v) for k, v in properties.items()}

    def get(self, name: str) -> Optional[str]:
        """
        Return the CSS block associated with
        `name` or `None` if it does not exist.
        """
        return self.styles.get(name)

    def get_blocks(self) -> tuple[str]:
        """Return a list of blocks found in the stylesheet."""
        # Split along selectors and remove empty strings.
        result = filter(None, re.split(MATCH_SELECTOR, self.source_min))

        # Remove any leftover curly braces and return the result.
        return (*map(lambda i: re.sub(MATCH_BRACES, "", i), result),)

    def get_property(self, widget_name: str, property: str) -> Optional[str]:
        """Return the value of a property given a selector and property name."""
        return self.styles[widget_name].get(property)

    def get_selectors(self) -> tuple[str]:
        """Return a list of selectors found in the stylesheet."""
        # Remove empty strings and return the result.
        return (*filter(None, re.split(MATCH_BLOCK, self.source_min)),)

    def minify_css(self, source_path: str) -> str:
        """Remove whitespace and comments from stylesheet."""
        with open(source_path) as f:
            lines = map(str.strip, f.readlines())

        # For non-property lines, remove all spaces.
        # For property lines, remove spaces following
        # a colon or a comma.
        result = map(
            lambda line: re.sub(MATCH_DELIMITER_SPACE, "", line)
            if line.endswith(";")
            else re.sub(MATCH_SPACE, "", line),
            lines,
        )

        return re.sub(MATCH_COMMENT, "", "".join(result))

    def parse_block(self, block: str) -> dict[str, str]:
        """Return a minified CSS block as a dictionary."""
        results = {
            property[0]: property[1]
            for property in map(
                lambda i: (*i.split(":"),),
                filter(None, block.split(";")),
            )
        }

        # Translate from CSS property names.
        translated_results = {}
        for k in results.keys():
            if k in CSS_TO_TK.keys():
                translated_results[CSS_TO_TK[k]] = results[k]

            else:
                translated_results[k] = results[k]

        return dict(
            filter(lambda k: results.get(k) is None, translated_results.items())
        )

    def var(self, value: str) -> Optional[str]:
        """Return the value associated with a given variable name."""
        name = re.findall(MATCH_VAR_NAME, value)

        if not name:
            return value

        return self.get_property(":root", *name)
