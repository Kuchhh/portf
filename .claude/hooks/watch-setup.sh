#!/usr/bin/env bash
# Prepare the /watch skill (.claude/skills/watch) in Claude Code cloud sessions.
# Cloud containers start fresh, so install yt-dlp and write a non-interactive
# watch config on every session start. Local machines are left untouched.
set -uo pipefail

[ "${CLAUDE_CODE_REMOTE:-}" = "true" ] || exit 0

SKILL_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}/.claude/skills/watch"
export PATH="$HOME/.local/bin:$PATH"

if ! command -v yt-dlp >/dev/null 2>&1; then
  pip3 install --quiet --user --disable-pip-version-check yt-dlp >/dev/null 2>&1 \
    || echo "[watch] yt-dlp install failed; /watch on local files may not start" >&2
fi

# Frames-only by default: Whisper models and cloud ASR hosts are blocked here.
# If GEMINI_API_KEY is set in the environment's secrets, watch uses Gemini instead.
if [ ! -f "$HOME/.config/watch/.env" ]; then
  python3 "$SKILL_DIR/scripts/setup.py" --backend none --detail balanced >/dev/null 2>&1 \
    || echo "[watch] setup.py failed; run it manually from $SKILL_DIR/scripts" >&2
fi

exit 0
