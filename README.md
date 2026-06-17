# OpenCode Go

Adds OpenCode Go and Zen as plugin-owned model gateway providers for Agent Zero.

## Providers

- `opencode_zen` uses the OpenAI-compatible OpenCode Zen endpoint for models documented with `/chat/completions`.
- `opencode_zen_anthropic` uses the Anthropic-compatible OpenCode Zen endpoint for models documented with `/messages`.
- `opencode_go` uses the OpenAI-compatible OpenCode Go endpoint for models documented with `/chat/completions`.
- `opencode_go_anthropic` uses the Anthropic-compatible OpenCode Go endpoint for models documented with `/messages`.

OpenCode publishes the live model catalog at `/models` for each gateway. The provider metadata filters that catalog by protocol so Agent Zero only suggests models that match the selected LiteLLM provider family.

## API Keys

Paste the API key from your OpenCode account into the corresponding provider row in Model Configuration. Go and Zen use different base URLs but the same OpenCode account key format.

The plugin also accepts a shared `OPENCODE_API_KEY` / `API_KEY_OPENCODE` environment value. If the Anthropic-compatible Zen or Go entry does not have its own key, it falls back to the matching `opencode_zen` or `opencode_go` key, then to the shared `opencode` key.
