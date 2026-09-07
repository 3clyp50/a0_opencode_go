# OpenCode Go

Adds OpenCode Go and Zen as plugin-owned model gateway providers for Agent Zero.

## Providers

- `opencode_zen` uses the OpenAI-compatible OpenCode Zen endpoint for models documented with `/chat/completions`.
- `opencode_zen_anthropic` uses the Anthropic-compatible OpenCode Zen endpoint for models documented with `/messages`.
- `opencode_go` uses the OpenAI-compatible OpenCode Go endpoint for models documented with `/chat/completions` (GLM, Kimi, DeepSeek, and MiMo).
- `opencode_go_anthropic` uses the Anthropic-compatible OpenCode Go endpoint for models documented with `/messages` (MiniMax and Qwen).

OpenCode publishes the live model catalog at `/models` for each gateway. The provider metadata filters that catalog by protocol so Agent Zero only suggests models that match the selected LiteLLM provider family.

## API Keys

Paste the API key from your OpenCode account into the corresponding provider row in Model Configuration. Go and Zen use different base URLs but the same OpenCode account key format.

The plugin also accepts a shared `OPENCODE_API_KEY` / `API_KEY_OPENCODE` environment value. If the Anthropic-compatible Zen or Go entry does not have its own key, it falls back to the matching `opencode_zen` or `opencode_go` key, then to the shared `opencode` key.

## Session affinity

The plugin automatically sends an `x-opencode-session` header on every chat and utility-model request to OpenCode Zen and Go. The value is derived from the current Agent Zero conversation context so requests in the same conversation are routed consistently. This prevents HTTP 400 "Model is unavailable" errors on backends that require sticky session routing.

If you set `extra_headers.x-opencode-session` in your model kwargs, that value is respected and the plugin will not overwrite it.

## Model names in Agent Zero

Use the exact OpenCode model ID in the Agent Zero model field. Do not include the OpenCode config provider prefix.

For example, to use MiniMax M2.7:

- Provider: `OpenCode Go (MiniMax/Qwen)`
- Model: `minimax-m2.7`

Do not enter `opencode-go/minimax-m2.7`, `MiniMax M2.7`, or `MiniMax-M2.7` as the Agent Zero model name. Those are OpenCode UI/config labels, while the API expects the lowercase model ID.
