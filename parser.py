"""
DSL Parser — stub interface.

Replace the parse() function with your real DSL parser.
The only requirement is: parse(file_path) -> dict.
Tests and views receive whatever dict you return here.
"""


def parse(file_path):
    """Read a DSL file and return parsed content as a dict.

    This stub just returns the raw text. Replace with your real parser.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        return {"raw": f.read()}
