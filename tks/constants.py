# Regular expressions to help parse CSS.
MATCH_COMMENT = r"/\*.+?\*/"
MATCH_BLOCK = r"\{.*?\}"
MATCH_BRACES = r"[\{\}]"
MATCH_DELIMITER_SPACE = r"(?<=[:,])\s"
MATCH_SELECTOR = r"[:\w\.#\-]+\{"
MATCH_SPACE = r"\s"
MATCH_VAR_NAME = r"--\w+"

# tk.Widget options not associated with style.
NON_STYLE_CONFIG_OPTIONS: set[str] = {
    "command",
    "default",
    "repeatdelay",
    "repeatinterval",
    "takefocus",
    "text",
    "textvariable",
}
