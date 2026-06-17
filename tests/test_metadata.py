from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


def _providers():
    data = yaml.safe_load((ROOT / "conf" / "model_providers.yaml").read_text(encoding="utf-8"))
    return data["chat"]


def test_minimax_and_qwen_use_messages_provider():
    chat = _providers()
    go = "\n".join(chat["opencode_go"]["models_list"]["include"])
    go_messages = "\n".join(chat["opencode_go_anthropic"]["models_list"]["include"])

    assert "minimax" not in go
    assert "qwen" not in go
    assert "minimax" in go_messages
    assert "qwen" in go_messages
    assert chat["opencode_go_anthropic"]["litellm_provider"] == "anthropic"


def test_openai_compatible_go_label_names_supported_family():
    chat = _providers()

    assert chat["opencode_go"]["name"] == "OpenCode Go (GLM/Kimi/DeepSeek/MiMo)"
    assert chat["opencode_go_anthropic"]["name"] == "OpenCode Go (MiniMax/Qwen)"
