# Poe Direct for Claude Code

Poe Direct for Claude Code is the lightweight edition of the Poe + Claude Code setup.

It uses Poe's official Anthropic-compatible API directly, so Claude Code can talk to Poe without a local proxy server.

---

## Positioning

This repository is the minimal, official-path setup.

Use it when you want:

- no local proxy
- no compatibility shim to maintain
- the shortest path from Claude Code to Poe's Claude models

This is the clean counterpart to the heavier proxy-based setup.

---

## Why This Exists

Poe now officially documents a Claude Code integration path through its Anthropic-compatible API.

That direct path also has a straightforward pricing story. If your goal is still to use official Claude models, but through Poe's billing path instead of the default Claude subscription path, this lightweight repository is the honest minimal version of that setup.

For many users, that is the real appeal: keep using Claude in Claude Code, but do it through Poe's account and pricing model rather than through a heavier local proxy arrangement.

## Background: Why Switch Away From The Default Subscription?

Claude usage can get expensive quickly, especially long-context Claude Code sessions on Opus-class models.

For users who still want official Claude models, but would rather access them through Poe's account and pricing path, the direct Poe route is often the simplest reason to switch.

Now that Poe exposes an official Anthropic-compatible path, this lightweight repository does not need to keep a local proxy layer at all.

That means a local compatibility proxy is no longer required if your only goal is:

- using Claude Code through Poe
- staying on Claude models
- keeping setup simple and easy to explain

This repository keeps only the minimal scripts and documentation needed for that direct path.

---

## How It Works

```text
Claude Code (VS Code)
  |
  | ANTHROPIC_BASE_URL=https://api.poe.com
  | ANTHROPIC_AUTH_TOKEN=<your Poe API key>
  | ANTHROPIC_API_KEY=
  v
Poe Anthropic-compatible API (/v1/messages)
  |
  v
Claude models on Poe
```

There is no local proxy in this repository.
Claude Code speaks its normal Anthropic-compatible protocol directly to Poe.

---

## Prerequisites

1. Claude Code is installed and working.
2. You have a Poe account.
3. You have a Poe API key from https://poe.com/api/keys.
4. Python 3 is available to run the helper scripts.

If your main motivation is simply lower-friction or lower-cost Claude access through Poe, this repository is the right place for that story.

---

## Files

| File | Purpose |
|------|---------|
| `setup_poe.py` | Write Claude Code environment overrides for Poe direct mode |
| `restore_clean.py` | Remove Poe-related overrides and restore the normal path |
| `README_zhCN.md` | Chinese documentation |

---

## Quick Start

Run:

```bash
python setup_poe.py --token p-xxxxxxxxxxxxxxxxxxxx
```

The setup script will:

1. Write Poe-related environment variables into `~/.claude/settings.json`.
2. Clear `cachedExtraUsageDisabledReason` from `~/.claude.json`.
3. Print the values that Claude Code will use after restart.

The injected configuration looks like this:

```json
"env": {
  "ANTHROPIC_BASE_URL": "https://api.poe.com",
  "ANTHROPIC_AUTH_TOKEN": "p-xxx...",
  "ANTHROPIC_API_KEY": ""
}
```

---

## Verify

Restart Claude Code, then run:

```text
/status
```

You should see Claude Code using:

```text
Anthropic base URL: https://api.poe.com
```

---

## Restore Official Mode

To stop using Poe and return Claude Code to the normal official path:

```bash
python restore_clean.py
```

This removes the Poe-related environment overrides and clears the cached usage-related UI state.

---

## Scope

This lightweight repository is intentionally limited.

It is suitable when:

- you only need Claude Code -> Poe direct access
- you only need official Claude models on Poe
- you do not need custom bots or non-Claude providers through an Anthropic-shaped interface

It is not meant to replace a compatibility proxy for broader Poe integrations.

---

## Notes

- Restart Claude Code after running either script.
- Poe API usage still consumes Poe subscription points or add-on points.
- Poe's Anthropic-compatible API is limited to official Claude models.
- If you need custom bots or non-Claude models behind an Anthropic-compatible facade, use a heavier proxy-based project instead.
