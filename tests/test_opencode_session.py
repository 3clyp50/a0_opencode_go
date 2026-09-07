import asyncio
import sys
import types

import pytest


# Agent Zero's helpers.extension is not available in this repo; mock it so the
# extension modules can be imported and instantiated.
_helpers_extension = types.ModuleType("helpers.extension")


class _ExtensionBase:
    def __init__(self, agent=None, **kwargs):
        self.agent = agent
        self.kwargs = kwargs


_helpers_extension.Extension = _ExtensionBase
sys.modules["helpers.extension"] = _helpers_extension

# The extension files import the helper through the plugin's canonical package
# path. Alias the repo-local helpers package to that path for tests.
sys.path.insert(0, __file__.rsplit("/tests/", 1)[0])
import helpers.opencode_session as _session_module

_pkg = types.ModuleType("usr")
_plugins = types.ModuleType("usr.plugins")
_plugin = types.ModuleType("usr.plugins.a0_opencode_go")
_plugin_helpers = types.ModuleType("usr.plugins.a0_opencode_go.helpers")
_plugin_helpers.opencode_session = _session_module

sys.modules["usr"] = _pkg
sys.modules["usr.plugins"] = _plugins
sys.modules["usr.plugins.a0_opencode_go"] = _plugin
sys.modules["usr.plugins.a0_opencode_go.helpers"] = _plugin_helpers
sys.modules["usr.plugins.a0_opencode_go.helpers.opencode_session"] = _session_module

from helpers.opencode_session import (
    OPENCODE_PROVIDERS,
    SESSION_HEADER,
    inject_session_header,
)
from extensions.python.chat_model_call_before._10_opencode_session import (
    OpenCodeChatSessionHeader,
)
from extensions.python.util_model_call_before._10_opencode_session import (
    OpenCodeUtilSessionHeader,
)


class _FakeContext:
    def __init__(self, context_id):
        self.id = context_id


class _FakeAgent:
    def __init__(self, context_id):
        self.context = _FakeContext(context_id)


class _FakeModelConfig:
    def __init__(self, provider):
        self.provider = provider


class _FakeModel:
    def __init__(self, provider, kwargs=None, no_conf=False):
        if no_conf:
            self.a0_model_conf = None
        else:
            self.a0_model_conf = _FakeModelConfig(provider)
        self.kwargs = kwargs or {}


def test_injects_header_for_all_opencode_providers():
    for provider in OPENCODE_PROVIDERS:
        model = _FakeModel(provider)
        inject_session_header(_FakeAgent("ctx-abc"), model)
        assert model.kwargs["extra_headers"][SESSION_HEADER] == "ctx-abc"


@pytest.mark.parametrize("provider", ["openai", "anthropic", "google", "other"])
def test_skips_non_opencode_providers(provider):
    model = _FakeModel(provider)
    inject_session_header(_FakeAgent("ctx-abc"), model)
    assert "extra_headers" not in model.kwargs


def test_preserves_existing_extra_headers():
    model = _FakeModel("opencode_go", kwargs={"extra_headers": {"X-Custom": "keep"}})
    inject_session_header(_FakeAgent("ctx-abc"), model)
    assert model.kwargs["extra_headers"]["X-Custom"] == "keep"
    assert model.kwargs["extra_headers"][SESSION_HEADER] == "ctx-abc"


def test_preserves_user_session_header():
    model = _FakeModel(
        "opencode_go",
        kwargs={"extra_headers": {SESSION_HEADER: "user-session"}},
    )
    inject_session_header(_FakeAgent("ctx-abc"), model)
    assert model.kwargs["extra_headers"][SESSION_HEADER] == "user-session"


def test_no_agent_leaves_kwargs_untouched():
    model = _FakeModel("opencode_go")
    inject_session_header(None, model)
    assert "extra_headers" not in model.kwargs


def test_missing_model_conf_leaves_kwargs_untouched():
    model = _FakeModel("opencode_go", no_conf=True)
    inject_session_header(_FakeAgent("ctx-abc"), model)
    assert "extra_headers" not in model.kwargs


def test_model_none_is_noop():
    inject_session_header(_FakeAgent("ctx-abc"), None)


def test_chat_extension_wires_through_call_data():
    model = _FakeModel("opencode_zen")
    ext = OpenCodeChatSessionHeader(agent=_FakeAgent("ctx-xyz"))
    asyncio.run(ext.execute(call_data={"model": model}))
    assert model.kwargs["extra_headers"][SESSION_HEADER] == "ctx-xyz"


def test_util_extension_wires_through_call_data():
    model = _FakeModel("opencode_go")
    ext = OpenCodeUtilSessionHeader(agent=_FakeAgent("ctx-uvw"))
    asyncio.run(ext.execute(call_data={"model": model}))
    assert model.kwargs["extra_headers"][SESSION_HEADER] == "ctx-uvw"
