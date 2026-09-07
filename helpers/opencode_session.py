from __future__ import annotations

OPENCODE_PROVIDERS = {
    "opencode_zen",
    "opencode_zen_anthropic",
    "opencode_go",
    "opencode_go_anthropic",
}
SESSION_HEADER = "x-opencode-session"


def inject_session_header(agent, model) -> None:
    if model is None:
        return

    conf = getattr(model, "a0_model_conf", None)
    provider = str(getattr(conf, "provider", "") or "").lower() if conf is not None else ""
    if provider not in OPENCODE_PROVIDERS:
        return

    context = getattr(agent, "context", None) if agent is not None else None
    session_id = str(getattr(context, "id", "") or "").strip() if context is not None else ""
    if not session_id:
        return

    model_kwargs = getattr(model, "kwargs", None)
    if not isinstance(model_kwargs, dict):
        return

    extra_headers = model_kwargs.setdefault("extra_headers", {})
    if not isinstance(extra_headers, dict):
        return

    extra_headers.setdefault(SESSION_HEADER, session_id)
