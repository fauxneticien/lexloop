"""Example view: renders raw file content in a pre block."""

import html as html_mod


def render(parsed_data):
    raw = parsed_data.get("raw", "")
    escaped = html_mod.escape(raw)
    return {
        "name": "Raw Content",
        "html": f"<pre>{escaped}</pre>" if raw else "<p>No content.</p>",
    }
