# Skills & toolchain registry

Every third-party capability, its source, what was inspected, and the decision.
**Nothing here was installed by running a vendor install script.** Each repo was
cloned read-only and read before anything was copied.

Audited 2026-08-27.

## Installed

| Capability | Source | Commit / version | Licence | Why |
|---|---|---|---|---|
| Remotion authoring ×6 — `remotion-best-practices`, `-create`, `-markup`, `-captions`, `-render`, `-multimedia` | `remotion-dev/skills` | `7a3d0ca` · v4.0.518 · 2026-08-26 | see repo | The only asset-layer capability needing **no credential**. Docs and guidance only; no executable install step. |
| `last30days` v3.21.1 | `mvanhorn/last30days-skill` | 2026-08-27 | MIT | Audience research. Needs Python 3.12 (provisioned via `uv`). |
| OpenMontage render engine | `calesthio/OpenMontage` | 2026-08-27 | **AGPL-3.0** | Vendored outside the skills tree on purpose — copyleft stays unmerged. |
| `voicebox-tts` 1.0.0 | `austin-bowen/voicebox` | 1.0.0 | MIT | Narration cast. |
| Piper voices (lessac, alan) | `rhasspy/piper-voices` | — | MIT-compatible | Offline TTS, no key. |
| static ffmpeg/ffprobe 7.0.2 | johnvansickle build | 7.0.2 | LGPL/GPL build | Encode, mux, probe. |

Rejected from `remotion-dev/skills`: `remotion-maps` (624K, irrelevant),
`-saas`, `-studio`, `-upgrade`, `-docs`, `-interactivity` — no current use, and
the smallest useful set is the rule.

## Audited, approved, BLOCKED on a credential

All three are safe to enable the moment a key exists. **No credential was
fabricated and no placeholder was written.**

### `hanoak/pexels-mcp-server` — stock video + photo · PRIMARY
`44dacfd` · v1.0.2 · 2026-08-19 · **MIT**

- **Dependencies: 2.** `@modelcontextprotocol/sdk`, `zod`. Unusually lean.
- **Network: `https://api.pexels.com/v1` only.** No other host in `src/`.
- No `postinstall`/`preinstall`. A `prepare: husky` dev hook only.
- `child_process` appears **only in `test/stdout-purity.test.ts`**, not in shipped code.
- Ships `SECURITY.md`, a production `npm audit` script, and an allowlist
  licence-checker restricted to permissive licences.
- Carries `photographer`, `photographer_url`, `photographer_id`; supports
  `orientation` (incl. `portrait`), `size`, `per_page`, `locale` — all six
  required capabilities are present.
- **Verdict: APPROVE.** Cleanest of the three.
- **`BLOCKED: PEXELS_API_KEY_REQUIRED`**

### `cevatkerim/unsplash-mcp` — photography · SECONDARY
`b92603c` · 2026-01-10 · **MIT**

- **40 KB, one file** (`server.py`), 3 deps: `fastmcp`, `httpx`, `python-dotenv`.
- **Network: `https://api.unsplash.com` only.** **Zero** shell/exec/eval anywhere.
- Tools: `search_photos`, `get_random_photos`, **`track_download`**.
- Builds `attribution_text` / `attribution_html` ready to use, and the dataclass
  comments mark attribution as *required by Unsplash API guidelines* — it takes
  the licence obligation seriously, which is the point of using it.
- **Staleness: last commit 2026-01-10, ~7 months.** Small and dependency-light
  enough that this is a low risk, but re-check before relying on it heavily.
- **Verdict: APPROVE as secondary.**
- **`BLOCKED: UNSPLASH_ACCESS_KEY_REQUIRED`**

### `sandraschi/sfx-mcp` — CC0 sound effects
`fe50f86` · 2026-08-20 · **MIT**

- **Network: `freesound.org/apiv2` only** (plus localhost/Tauri for its own UI).
- **Hard-filters `license:"Creative Commons 0"` in the query string itself** —
  CC0 is enforced at the source, not hoped for afterwards. Stores `license` per item.
- Local SQLite cache + local path: exactly the "reusable library, don't
  re-download per video" behaviour the spec asks for.
- Ships `hooks/hooks.json` with a **SessionStart hook of `"type": "text"`** — it
  injects context text, it does **not** execute anything. Benign, but it is a
  hook that would run in every session, so it is named here rather than left to
  be discovered.
- `start.bat` / `start.ps1` are Windows launchers, unused here and not run.
- Extra dep `prefab-ui` pulls a UI layer we do not need; the MCP server works
  without touching it.
- **Verdict: APPROVE.**
- **`BLOCKED: FREESOUND_API_KEY_REQUIRED`** — free from freesound.org.

## What being blocked actually costs

With no stock or SFX keys, the asset decision engine collapses toward
`REAL_HANDSEL_CAPTURE` and `REMOTION_GENERATED`. That is **the correct priority
order anyway** — real product behaviour outranks stock, and agent-native concepts
have no honest stock representation. The blocked layer costs texture and B-roll,
not the ability to make videos.

Three keys, all free or cheap, unblock it: `PEXELS_API_KEY`,
`UNSPLASH_ACCESS_KEY`, `FREESOUND_API_KEY`.
