#!/usr/bin/env python3
"""Configure Claude Code to use Poe's official Anthropic-compatible API directly."""

import argparse
import json
import os
import sys
from pathlib import Path

SETTINGS_FILE = Path.home() / ".claude" / "settings.json"
CLAUDE_JSON = Path.home() / ".claude.json"
SCHEMA_URL = "https://json.schemastore.org/claude-code-settings.json"


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


def patch_settings(token: str) -> None:
    settings = read_json(SETTINGS_FILE)
    settings.setdefault("$schema", SCHEMA_URL)

    env = settings.setdefault("env", {})
    env["ANTHROPIC_BASE_URL"] = "https://api.poe.com"
    env["ANTHROPIC_AUTH_TOKEN"] = token
    env["ANTHROPIC_API_KEY"] = ""

    write_json(SETTINGS_FILE, settings)


def clear_credits_cache() -> None:
    claude_json = read_json(CLAUDE_JSON)
    removed = claude_json.pop("cachedExtraUsageDisabledReason", None)
    if removed is not None:
        write_json(CLAUDE_JSON, claude_json)
        print("Cleared cachedExtraUsageDisabledReason from ~/.claude.json")
    else:
        print("No cachedExtraUsageDisabledReason found in ~/.claude.json")


def resolve_token(cli_token: str | None) -> str:
    token = cli_token or os.environ.get("POE_API_KEY", "")
    if not token:
        print("Error: provide --token or set POE_API_KEY in the environment.", file=sys.stderr)
        sys.exit(1)
    return token


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Configure Claude Code to use Poe directly through Anthropic-compatible API"
    )
    parser.add_argument(
        "--token",
        help="Poe API key. If omitted, POE_API_KEY from the environment is used.",
    )
    args = parser.parse_args()

    token = resolve_token(args.token)

    print("=== Configure Claude Code -> Poe Direct ===")
    print("[1/2] Updating ~/.claude/settings.json ...")
    patch_settings(token)

    print("[2/2] Clearing Claude Code cached usage state ...")
    clear_credits_cache()

    print("\nDone.")
    print("Restart Claude Code, then run /status to verify:")
    print("  Anthropic base URL: https://api.poe.com")


if __name__ == "__main__":
    main()
