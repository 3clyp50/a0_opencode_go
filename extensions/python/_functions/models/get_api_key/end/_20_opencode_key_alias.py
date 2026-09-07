from __future__ import annotations

from helpers.extension import Extension
import models


KEY_ALIASES = {
    "opencode_zen": ("opencode",),
    "opencode_zen_anthropic": ("opencode_zen", "opencode"),
    "opencode_go": ("opencode",),
    "opencode_go_anthropic": ("opencode_go", "opencode"),
}


class OpenCodeKeyAlias(Extension):
    def execute(self, data: dict | None = None, **kwargs):
        del kwargs
        if not isinstance(data, dict):
            return

        result = str(data.get("result") or "").strip()
        if result and result != "None":
            return

        args = data.get("args")
        call_kwargs = data.get("kwargs")
        if isinstance(args, (list, tuple)) and args:
            service = str(args[0] or "")
        elif isinstance(call_kwargs, dict):
            service = str(call_kwargs.get("service") or "")
        else:
            return

        for alias in KEY_ALIASES.get(service.lower(), ()):
            key = str(models.get_api_key(alias) or "").strip()
            if key and key != "None":
                data["result"] = key
                return
