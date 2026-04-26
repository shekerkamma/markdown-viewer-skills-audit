#!/usr/bin/env python3
"""Helper · call the Anthropic Messages API for a single system+user exchange.

Used by run.sh's --auto path to skip the paste-from-LLM step. Implements
prompt caching for the system message (the prompts/*.md files are reused
across phases), so a typical full pipeline run is one cache write + one
cache hit per phase.

Usage:
  _api_call.py --system <prompt-file> --user-file <path>
  _api_call.py --system <prompt-file> --user <inline-text>
  _api_call.py [--model <id>] [--max-tokens N]

Reads ANTHROPIC_API_KEY from env. Stdlib only — no Anthropic SDK required.

stdout : the assistant's response text only (the part the caller wants).
stderr : one line of metadata (model, token counts, cache hit/miss).

Exit codes:
  0  success
  1  API error (HTTP non-2xx, network failure)
  2  ANTHROPIC_API_KEY missing
  3  bad args
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

DEFAULT_MODEL = "claude-haiku-4-5-20251001"
API_URL = "https://api.anthropic.com/v1/messages"
API_VERSION = "2023-06-01"
MAX_TOKENS_DEFAULT = 4096
TIMEOUT_SEC = 120


def call_api(system_text: str, user_text: str, model: str, max_tokens: int) -> tuple[str, dict]:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("error: ANTHROPIC_API_KEY environment variable is not set", file=sys.stderr)
        print("       export it, or run without --auto and paste model output manually.", file=sys.stderr)
        sys.exit(2)

    body = {
        "model": model,
        "max_tokens": max_tokens,
        "system": [
            {
                "type": "text",
                "text": system_text,
                "cache_control": {"type": "ephemeral"},
            }
        ],
        "messages": [{"role": "user", "content": user_text}],
    }
    req = urllib.request.Request(
        API_URL,
        data=json.dumps(body).encode(),
        headers={
            "x-api-key": api_key,
            "anthropic-version": API_VERSION,
            "content-type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT_SEC) as r:
            payload = json.loads(r.read())
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace")
        print(f"error: HTTP {e.code} from Anthropic API", file=sys.stderr)
        print(err_body, file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"error: network failure: {e.reason}", file=sys.stderr)
        sys.exit(1)
    except (json.JSONDecodeError, KeyError) as e:
        print(f"error: malformed response: {e}", file=sys.stderr)
        sys.exit(1)

    text = "".join(b["text"] for b in payload.get("content", []) if b.get("type") == "text")
    usage = payload.get("usage", {})
    meta = {
        "model": payload.get("model", model),
        "input_tokens": usage.get("input_tokens"),
        "output_tokens": usage.get("output_tokens"),
        "cache_creation_input_tokens": usage.get("cache_creation_input_tokens", 0),
        "cache_read_input_tokens": usage.get("cache_read_input_tokens", 0),
    }
    return text, meta


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--system", required=True, help="path to system prompt file")
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--user-file", help="path to user content file")
    src.add_argument("--user", help="inline user content")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--max-tokens", type=int, default=MAX_TOKENS_DEFAULT)
    args = ap.parse_args()

    sys_path = Path(args.system)
    if not sys_path.is_file():
        print(f"error: system prompt file not found: {sys_path}", file=sys.stderr)
        return 3
    system_text = sys_path.read_text()
    user_text = Path(args.user_file).read_text() if args.user_file else args.user

    text, meta = call_api(system_text, user_text, args.model, args.max_tokens)
    print(text)
    print(
        f"[api: model={meta['model']} "
        f"in={meta['input_tokens']} out={meta['output_tokens']} "
        f"cache_create={meta['cache_creation_input_tokens']} "
        f"cache_read={meta['cache_read_input_tokens']}]",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
