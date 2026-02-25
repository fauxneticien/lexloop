"""HTML templates for lexloop output pages."""

import html

REFRESH_JS = """
<script>
(function() {
    var currentVersion = "{version}";
    setInterval(function() {
        fetch("/version.txt?_=" + Date.now())
            .then(function(r) { return r.text(); })
            .then(function(v) {
                if (v.trim() !== currentVersion) {
                    window.location.reload();
                }
            })
            .catch(function() {});
    }, 1000);
})();
</script>
"""

PAGE_CSS = """
body { font-family: system-ui, -apple-system, sans-serif; max-width: 900px; margin: 2em auto; padding: 0 1em; color: #333; }
h1 { border-bottom: 2px solid #eee; padding-bottom: 0.3em; }
a { color: #0066cc; }
table { border-collapse: collapse; width: 100%; }
td, th { border: 1px solid #ddd; padding: 8px; text-align: left; }
pre { background: #f5f5f5; padding: 1em; overflow-x: auto; }
.badge { display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 0.85em; font-weight: bold; }
.pass { background: #d4edda; color: #155724; }
.fail { background: #f8d7da; color: #721c24; }
.error { background: #fff3cd; color: #856404; }
"""


def wrap_page(title, body_html, version):
    """Wrap an HTML fragment in a full page with styling and auto-refresh."""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{html.escape(title)} — Lexloop</title>
<style>{PAGE_CSS}</style>
</head>
<body>
<h1>{html.escape(title)}</h1>
{body_html}
{REFRESH_JS.replace("{version}", str(version))}
</body>
</html>"""


def render_index(test_results, view_results, version):
    """Render the dashboard index page."""
    passed = sum(1 for _, r in test_results if r.get("passed"))
    failed = len(test_results) - passed

    body = ""

    # Test summary
    body += "<h2>Tests</h2>\n"
    if test_results:
        body += f"<p>{passed} passed, {failed} failed out of {len(test_results)} tests</p>\n"
        body += "<table><tr><th>Test</th><th>Status</th><th>Details</th></tr>\n"
        for module_name, result in test_results:
            status_class = "pass" if result.get("passed") else "fail"
            status_text = "PASS" if result.get("passed") else "FAIL"
            name = html.escape(result.get("name", module_name))
            details = result.get("details", "")
            body += (
                f'<tr><td><a href="tests/{module_name}.html">{name}</a></td>'
                f'<td><span class="badge {status_class}">{status_text}</span></td>'
                f"<td>{html.escape(details)}</td></tr>\n"
            )
        body += "</table>\n"
    else:
        body += "<p>No tests found. Add .py files to the tests/ folder.</p>\n"

    # Views
    body += "<h2>Views</h2>\n"
    if view_results:
        body += "<ul>\n"
        for module_name, result in view_results:
            name = html.escape(result.get("name", module_name))
            body += f'<li><a href="views/{module_name}.html">{name}</a></li>\n'
        body += "</ul>\n"
    else:
        body += "<p>No views found. Add .py files to the views/ folder.</p>\n"

    return wrap_page("Lexloop Dashboard", body, version)


def render_test_page(module_name, result, version):
    """Render a detail page for a single test result."""
    status_class = "pass" if result.get("passed") else "fail"
    status_text = "PASS" if result.get("passed") else "FAIL"
    name = result.get("name", module_name)
    details = result.get("details", "")

    body = (
        f'<p><a href="../index.html">&larr; Back to dashboard</a></p>\n'
        f'<p>Status: <span class="badge {status_class}">{status_text}</span></p>\n'
        f"<div>{details}</div>\n"
    )
    return wrap_page(name, body, version)


def render_view_page(module_name, result, version):
    """Render a page for a single view."""
    name = result.get("name", module_name)
    view_html = result.get("html", "")

    body = (
        f'<p><a href="../index.html">&larr; Back to dashboard</a></p>\n'
        f"{view_html}\n"
    )
    return wrap_page(name, body, version)


def render_error_page(title, error_message, version):
    """Render an error page (e.g. for parse failures)."""
    body = (
        f'<div class="badge error">ERROR</div>\n'
        f"<pre>{html.escape(error_message)}</pre>\n"
    )
    return wrap_page(title, body, version)
