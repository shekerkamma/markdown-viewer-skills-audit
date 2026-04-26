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
  echo "usage: $(basename "$0") <owner/repo> [--scope <subpath>] [--out <dir>] [--prefix <css>]" >&2
  exit 2
fi

REPO="$1"; shift
SCOPE=""
OUT=""
PREFIX="ra"
while [[ $# -gt 0 ]]; do
  case "$1" in
    --scope)  SCOPE="$2";  shift 2 ;;
    --out)    OUT="$2";    shift 2 ;;
    --prefix) PREFIX="$2"; shift 2 ;;
    *) echo "unknown arg: $1" >&2; exit 2 ;;
  esac
done

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
echo "Run this prompt with your LLM. System prompt is in:" >&2
echo "  $HERE/../prompts/summarize-readme.md" >&2
echo "User content is the raw README at:" >&2
echo "  $OUT/README.md" >&2
echo >&2
echo "Paste the 200-word summary below, then press Ctrl-D when done." >&2
echo "(If README is empty/boilerplate, paste 'INSUFFICIENT_README' and Ctrl-D.)" >&2
echo >&2
SUMMARY=$(cat)
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
echo "Run this prompt with your LLM. System prompt is in:" >&2
echo "  $HERE/../prompts/classify-modules.md" >&2
echo "User content is the structure.json at:" >&2
echo "  $OUT/structure.json" >&2
echo >&2
echo "Paste the layer-plan YAML below, then press Ctrl-D when done." >&2
echo "(For refusal, paste 'error: refused' YAML per the prompt's refusal schema.)" >&2
echo >&2
cat > "$OUT/layer-plan.yaml"
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

# ---------- Notes on full automation ----------
# To skip the manual paste steps, replace Phase 1.5 and Phase 2 with calls
# to your LLM API. The contract:
#   - Phase 1.5: input = README.md + summarize-readme.md. Output = plain text.
#   - Phase 2:   input = structure.json + classify-modules.md. Output = YAML.
# A reference Python implementation using urllib (no SDK dep) is one of the
# open follow-ups for this skill — see the "Honest gaps" section of SKILL.md.
