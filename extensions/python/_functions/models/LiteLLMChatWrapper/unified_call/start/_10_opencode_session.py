from __future__ import annotations

from helpers.extension import Extension
from usr.plugins.a0_opencode_go.helpers import opencode_headers


class OpenCodeClientHeaders(Extension):
    """Send official opencode client headers on OpenCode Zen/Go model calls."""

    def execute(self, data: dict | None = None, **kwargs):
        if not isinstance(data, dict):
            return
        args = data.get("args")
        wrapper = args[0] if isinstance(args, tuple) and args else None
        if wrapper is None:
            return
        opencode_headers.apply_client_headers(wrapper)
