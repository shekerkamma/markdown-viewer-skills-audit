#!/usr/bin/env bash
# repo-architecture · End-to-end orchestrator.
#
# Walks through the 4-phase pipeline:
#   1.    extract.py             (deterministic)
#   1.5   summarize README       (LLM — paste from your model)
#   2.    classify into layers   (LLM — paste from your model)
#   2.5   validate.py            (deterministic)
#   3.    render.py              (deterministic)
#
# Usage: run.sh <owner/repo> [--scope <subpath>] [--out <dir>] [--prefix <css>]
#
# Deterministic phases run automatically. LLM phases print the prompt and
# input, then read the model's output from stdin (Ctrl-D to finish). No API
# key required. To wire up the Anthropic API end-to-end, see "automation"
# notes at the bottom of this file.

set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "usage: $(basename "$0") <owner/repo> [--scope <subpath>] [--out <dir>] [--prefix <css>] [--auto] [--model <id>]" >&2
  echo >&2
  echo "  --auto         call the Anthropic API for the LLM phases (needs ANTHROPIC_API_KEY)" >&2
  echo "  --model <id>   override the API model (default: claude-haiku-4-5-20251001)" >&2
  exit 2
fi

REPO="$1"; shift
SCOPE=""
OUT=""
PREFIX="ra"
AUTO="no"
MODEL=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --scope)  SCOPE="$2";  shift 2 ;;
    --out)    OUT="$2";    shift 2 ;;
    --prefix) PREFIX="$2"; shift 2 ;;
    --auto)   AUTO="yes";  shift ;;
    --model)  MODEL="$2";  shift 2 ;;
    *) echo "unknown arg: $1" >&2; exit 2 ;;
  esac
done

if [[ "$AUTO" == "yes" && -z "${ANTHROPIC_API_KEY:-}" ]]; then
  echo "error: --auto requires ANTHROPIC_API_KEY in environment" >&2
  exit 2
fi
API_ARGS=()
[[ -n "$MODEL" ]] && API_ARGS+=(--model "$MODEL")

[[ -z "$OUT" ]] && OUT="out/${REPO//\//-}"
HERE="$(cd "$(dirname "$0")" && pwd)"
mkdir -p "$OUT"

# ---------- Phase 1: extract ----------
echo "=== Phase 1: extract structure ===" >&2
EXTRACT_ARGS=("$REPO" --out "$OUT")
[[ -n "$SCOPE" ]] && EXTRACT_ARGS+=(--scope "$SCOPE")
"$HERE/extract.py" "${EXTRACT_ARGS[@]}"

# ---------- Phase 1.5: summarize README (LLM) ----------
echo >&2
echo "=== Phase 1.5: summarize README (LLM step) ===" >&2
SUMMARIZE_PROMPT="$HERE/../prompts/summarize-readme.md"
README_PATH="$OUT/README.md"
if [[ "$AUTO" == "yes" ]]; then
  if [[ ! -f "$README_PATH" ]]; then
    echo "warning: $README_PATH missing — using INSUFFICIENT_README" >&2
    SUMMARY="INSUFFICIENT_README"
  else
    echo "calling Anthropic API…" >&2
    SUMMARY=$("$HERE/_api_call.py" --system "$SUMMARIZE_PROMPT" --user-file "$README_PATH" "${API_ARGS[@]}")
  fi
else
  echo "Run this prompt with your LLM. System prompt is in:" >&2
  echo "  $SUMMARIZE_PROMPT" >&2
  echo "User content is the raw README at:" >&2
  echo "  $README_PATH" >&2
  echo >&2
  echo "Paste the 200-word summary below, then press Ctrl-D when done." >&2
  echo "(If README is empty/boilerplate, paste 'INSUFFICIENT_README' and Ctrl-D.)" >&2
  echo >&2
  SUMMARY=$(cat)
fi
python3 - <<PYEOF
import json, sys
from pathlib import Path
p = Path("$OUT/structure.json")
d = json.loads(p.read_text())
d["readme_summary"] = """$SUMMARY""".strip()
p.write_text(json.dumps(d, indent=2))
print(f"updated structure.json with readme_summary ({len(d['readme_summary'])} chars)", file=sys.stderr)
PYEOF

if [[ "$SUMMARY" == "INSUFFICIENT_README" ]]; then
  echo "README signal too weak. Stopping — Phase 2 will refuse." >&2
  exit 0
fi

# ---------- Phase 2: classify (LLM) ----------
echo >&2
echo "=== Phase 2: classify modules into layers (LLM step) ===" >&2
CLASSIFY_PROMPT="$HERE/../prompts/classify-modules.md"
STRUCTURE_PATH="$OUT/structure.json"
if [[ "$AUTO" == "yes" ]]; then
  echo "calling Anthropic API…" >&2
  RAW_PLAN=$("$HERE/_api_call.py" --system "$CLASSIFY_PROMPT" --user-file "$STRUCTURE_PATH" "${API_ARGS[@]}" --max-tokens 8192)
  # Strip ```yaml ... ``` fences if the model wrapped the output.
  printf '%s\n' "$RAW_PLAN" | python3 -c "
import re, sys
text = sys.stdin.read()
m = re.search(r'\`\`\`(?:yaml|yml)?\n(.*?)\n\`\`\`', text, re.DOTALL)
sys.stdout.write((m.group(1) if m else text).rstrip() + '\n')
" > "$OUT/layer-plan.yaml"
else
  echo "Run this prompt with your LLM. System prompt is in:" >&2
  echo "  $CLASSIFY_PROMPT" >&2
  echo "User content is the structure.json at:" >&2
  echo "  $STRUCTURE_PATH" >&2
  echo >&2
  echo "Paste the layer-plan YAML below, then press Ctrl-D when done." >&2
  echo "(For refusal, paste 'error: refused' YAML per the prompt's refusal schema.)" >&2
  echo >&2
  cat > "$OUT/layer-plan.yaml"
fi
echo "wrote $OUT/layer-plan.yaml ($(wc -l < "$OUT/layer-plan.yaml") lines)" >&2

# ---------- Phase 2.5: validate ----------
echo >&2
echo "=== Phase 2.5: validate ===" >&2
set +e
"$HERE/validate.py" "$OUT/layer-plan.yaml"
RC=$?
set -e
case "$RC" in
  0) ;;  # valid — proceed
  2) echo "Plan is a refusal — see message above. Stopping." >&2; exit 0 ;;
  *) echo "Plan is invalid. Fix it and re-run: $HERE/validate.py $OUT/layer-plan.yaml" >&2; exit 1 ;;
esac

# ---------- Phase 3: render ----------
echo >&2
echo "=== Phase 3: render ===" >&2
"$HERE/render.py" "$OUT/layer-plan.yaml" --out "$OUT/diagram.html" --prefix "$PREFIX"

echo >&2
echo "Done. Open $OUT/diagram.html in a browser." >&2

# ---------- Notes ----------
# Manual mode (default): each LLM phase prints the prompt and reads from stdin.
#                        Paste your model's output, Ctrl-D to continue.
# Auto mode (--auto):    bin/_api_call.py shells out to the Anthropic API for
#                        each LLM phase using prompt caching. Requires
#                        ANTHROPIC_API_KEY in env. Default model is haiku-4-5;
#                        override with --model claude-sonnet-4-5 or similar.
