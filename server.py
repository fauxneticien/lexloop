"""Background HTTP server for serving output files."""

import threading
import webbrowser
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

_server = None
_thread = None


def start(directory, port=8000):
    """Start the HTTP server if not already running, and open the browser."""
    global _server, _thread

    if _server is not None:
        return  # already running

    handler = partial(SimpleHTTPRequestHandler, directory=directory)
    _server = ThreadingHTTPServer(("127.0.0.1", port), handler)

    _thread = threading.Thread(target=_server.serve_forever, daemon=True)
    _thread.start()

    webbrowser.open(f"http://127.0.0.1:{port}/index.html")


def is_running():
    return _server is not None
