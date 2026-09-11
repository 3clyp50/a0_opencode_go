from __future__ import annotations

import hashlib
import uuid

from helpers.context import get_context_data


API_BASE_MATCH = "opencode.ai/zen"
USER_AGENT = "opencode/1.18.30 ai-sdk/provider-utils/4.0.40 runtime/bun/1.3.14"


def apply_client_headers(wrapper) -> None:
    api_base = str(dict(getattr(wrapper, "kwargs", {}) or {}).get("api_base") or "").lower()
    if not api_base:
        config = getattr(wrapper, "a0_model_conf", None)
        api_base = str(getattr(config, "api_base", "") or "").lower()
    if API_BASE_MATCH not in api_base:
        return

    context_id = str(get_context_data("agent_context_id") or "").strip()
    if context_id:
        session_id = f"ses_{hashlib.sha1(context_id.encode()).hexdigest()[:27]}"
    else:
        session_id = f"ses_{uuid.uuid4().hex[:27]}"

    headers = dict(getattr(wrapper, "kwargs", {}).get("extra_headers") or {})
    headers["x-opencode-client"] = "cli"
    headers["x-opencode-session"] = session_id
    headers["x-opencode-project"] = _project_id(context_id)
    headers["x-opencode-request"] = f"msg_{uuid.uuid4().hex[:23]}"
    headers["User-Agent"] = USER_AGENT
    wrapper.kwargs["extra_headers"] = headers


def _project_id(context_id: str) -> str:
    seed = context_id or str(uuid.getnode())
    return hashlib.sha1(seed.encode()).hexdigest()[:40]
