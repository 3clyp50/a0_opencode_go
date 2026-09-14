# OpenCode Go Plugin

## Purpose

- Own the standalone Agent Zero OpenCode Go and Zen provider plugin.

## Ownership

- `plugin.yaml` owns the plugin identity and version; `conf/` and `extensions/` own provider integration.
- `hooks.py` owns lifecycle preparation; `README.md` owns setup and upgrade guidance.

## Local Contracts

- Agent Zero invokes `pre_update()` from the installed version before pulling.
- Thumbnail preparation only backs up untracked `webui/thumbnail.webp`; preserve tracked files, symlinks, unrelated files, and existing backups.
- Keep backups plugin-local and ignored by Git. Older installations without the hook require the documented one-time recovery.

## Work Guidance

- Keep provider and migration behavior plugin-owned; reuse Agent Zero's lifecycle hooks.

## Verification

- Run `python -m pytest -q tests` and `git diff --check` before publishing.

## Child DOX Index

No child DOX files.
