"""Core orchestration: parse -> test -> view -> HTML -> serve."""

import importlib.util
import os
import sys
import time
import traceback

import parser as dsl_parser
import server
import templates


def get_base_dir():
    """Return the base directory for locating tests/ and views/."""
    if getattr(sys, "frozen", False):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))


def _load_modules(directory, entry_point, parsed_data):
    """Discover .py files in a directory and call entry_point on each.

    Returns list of (module_name, result_dict) tuples.
    """
    results = []
    if not os.path.isdir(directory):
        return results

    for filename in sorted(os.listdir(directory)):
        if not filename.endswith(".py") or filename == "__init__.py":
            continue

        module_name = filename[:-3]
        file_path = os.path.join(directory, filename)

        try:
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            func = getattr(mod, entry_point)
            result = func(parsed_data)
        except Exception:
            result = {
                "name": module_name,
                "passed": False,
                "html": f"<pre>{traceback.format_exc()}</pre>",
                "details": traceback.format_exc(),
            }

        results.append((module_name, result))

    return results


def run(file_path, port=8000):
    """Run the full pipeline. Returns a status summary string."""
    base_dir = get_base_dir()
    output_dir = os.path.join(base_dir, "output")
    os.makedirs(os.path.join(output_dir, "tests"), exist_ok=True)
    os.makedirs(os.path.join(output_dir, "views"), exist_ok=True)

    version = str(int(time.time() * 1000))

    # Step 1: Parse
    try:
        parsed_data = dsl_parser.parse(file_path)
    except Exception:
        error_html = templates.render_error_page(
            "Parse Error", traceback.format_exc(), version
        )
        _write(os.path.join(output_dir, "index.html"), error_html)
        _write(os.path.join(output_dir, "version.txt"), version)
        server.start(output_dir, port)
        return "Parse error — see browser"

    # Step 2: Run tests
    tests_dir = os.path.join(base_dir, "tests")
    test_results = _load_modules(tests_dir, "run", parsed_data)

    # Step 3: Run views
    views_dir = os.path.join(base_dir, "views")
    view_results = _load_modules(views_dir, "render", parsed_data)

    # Step 4: Generate HTML
    for module_name, result in test_results:
        page = templates.render_test_page(module_name, result, version)
        _write(os.path.join(output_dir, "tests", f"{module_name}.html"), page)

    for module_name, result in view_results:
        page = templates.render_view_page(module_name, result, version)
        _write(os.path.join(output_dir, "views", f"{module_name}.html"), page)

    index_html = templates.render_index(test_results, view_results, version)
    _write(os.path.join(output_dir, "index.html"), index_html)
    _write(os.path.join(output_dir, "version.txt"), version)

    # Step 5: Start server if needed
    server.start(output_dir, port)

    # Summary
    passed = sum(1 for _, r in test_results if r.get("passed"))
    failed = len(test_results) - passed
    return f"{len(test_results)} tests: {passed} passed, {failed} failed | {len(view_results)} views"


def _write(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
