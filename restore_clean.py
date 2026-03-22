#!/usr/bin/env python3
"""Restore Claude Code to the default official path by removing Poe overrides."""

import json
from pathlib import Path

SETTINGS_FILE = Path.home() / ".claude" / "settings.json"
CLAUDE_JSON = Path.home() / ".claude.json"
PROXY_KEYS = {"ANTHROPIC_BASE_URL", "ANTHROPIC_AUTH_TOKEN", "ANTHROPIC_API_KEY"}


def read_json(path: Path) -> dict:
    if path.exists():
        with open(path, encoding="utf-8") as handle:
            return json.load(handle)
    return {}


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2)
        handle.write("\n")
    print(f"Wrote: {path}")


def clean_settings() -> None:
    settings = read_json(SETTINGS_FILE)
    env = settings.get("env")

    if not env:
        print("No env block found in ~/.claude/settings.json")
        return

    removed = False
    for key in PROXY_KEYS:
        if key in env:
            env.pop(key, None)
            removed = True

    if not removed:
        print("No Poe-related Anthropic overrides found in ~/.claude/settings.json")
        return

    if env:
        settings["env"] = env
    else:
        settings.pop("env", None)

    write_json(SETTINGS_FILE, settings)
    print("Removed Poe-related Claude Code environment overrides")


def clear_credits_cache() -> None:
    claude_json = read_json(CLAUDE_JSON)
    removed = claude_json.pop("cachedExtraUsageDisabledReason", None)
    if removed is not None:
        write_json(CLAUDE_JSON, claude_json)
        print("Cleared cachedExtraUsageDisabledReason from ~/.claude.json")
    else:
        print("No cachedExtraUsageDisabledReason found in ~/.claude.json")


def main() -> None:
    print("=== Restore Claude Code Default Path ===")
    print("[1/2] Cleaning ~/.claude/settings.json ...")
    clean_settings()

    print("[2/2] Clearing Claude Code cached usage state ...")
    clear_credits_cache()

    print("\nDone.")
    print("Restart Claude Code to apply the restored configuration.")


if __name__ == "__main__":
    main()
