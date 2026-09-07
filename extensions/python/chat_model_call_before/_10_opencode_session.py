from __future__ import annotations

from helpers.extension import Extension
from usr.plugins.a0_opencode_go.helpers.opencode_session import inject_session_header


class OpenCodeChatSessionHeader(Extension):
    async def execute(self, **kwargs):
        call_data = kwargs.get("call_data")
        if isinstance(call_data, dict):
            inject_session_header(self.agent, call_data.get("model"))
