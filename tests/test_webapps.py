"""Smoke tests for the web-apps suite (formerly MRIRYHED).

Validates structure and basic integrity of the static web apps without a browser:
every app ships an ``index.html``, all HTML parses, and the realtime server
entrypoint exists.
"""
from __future__ import annotations

import glob
import pathlib
from html.parser import HTMLParser

ROOT = pathlib.Path(__file__).resolve().parent.parent

APPS = ["weather-dashboard", "online-code-editor", "zodiac-calculator", "chatx/client"]


class _Collector(HTMLParser):
    def error(self, message):  # pragma: no cover - base signals parse errors via exception
        raise ValueError(message)


def test_each_app_has_index_html() -> None:
    for app in APPS:
        assert (ROOT / app / "index.html").exists(), f"{app}: missing index.html"


def test_html_files_parse() -> None:
    for html in glob.glob(str(ROOT / "**" / "*.html"), recursive=True):
        _Collector().feed(pathlib.Path(html).read_text(encoding="utf-8", errors="replace"))


def test_chat_server_entrypoint() -> None:
    assert (ROOT / "chatx" / "server" / "server.js").exists()
