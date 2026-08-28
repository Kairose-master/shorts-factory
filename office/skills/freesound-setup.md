# Getting a Freesound key, and attaching it to this environment

## 0. Read this first — what the key actually buys

Verified against Freesound's own resource docs, not assumed:

- `GET /apiv2/sounds/<id>/download/` — *"It requires **OAuth2** authentication."*
- `previews` (mp3 / ogg URIs) — **no OAuth2 requirement**, works with a plain token.

`vendor/sfx-mcp` authenticates with `Authorization: Token <key>` (see
`src/sfx_mcp/services/freesound.py:34`). So with a plain API key you get
**search + metadata + preview audio**. Its `get_download_url()` hits the
OAuth2-only endpoint and **will fail**.

**Is that a problem?** For this Office, barely. Previews are ~128 kbps mp3/ogg.
An SFX sitting under narration in a 30-second vertical video does not need
original-quality WAV. If a shot ever genuinely needs the master file, that needs
a full OAuth2 flow with a browser redirect — awkward in an ephemeral container,
and worth avoiding until something actually demands it.

## 1. Get the key (~2 minutes, free)

1. Create an account at <https://freesound.org> and confirm the email.
2. Go to <https://freesound.org/apiv2/apply/>.
3. Fill in a name and a short description. A URL is requested but anything
   reasonable is accepted.
4. It issues immediately. You get a **client id** and a **client secret / API
   key**. The one you want is the **API key** — that is `FREESOUND_API_KEY`.

## 2. Attach it to this environment — the persistent way

**This is how every other key here got in.** There is no `.env` file in this
container and nothing is hardcoded in a shell profile; `SCRAPECREATORS_API_KEY`,
`APIFY_TOKEN` and the rest are injected as **container environment variables**
from the Claude Code environment configuration.

1. Open <https://claude.ai/code> → environment settings for this environment.
2. Add an environment variable: name `FREESOUND_API_KEY`, value the API key.
3. Save.

It is injected when the container is next created, so **it applies from the next
session**, not retroactively to this one. That is the tradeoff for it surviving
the container being reclaimed. Reference:
<https://code.claude.com/docs/en/claude-code-on-the-web>

## 3. If you want it working in the current session too

Shell state does not persist between commands here, so `export` is useless — it
dies with the command that ran it. The only thing that works in-session is a
file:

```bash
echo 'FREESOUND_API_KEY=your-key-here' >> .env
```

`sfx-mcp` loads `.env` via `python-dotenv`, so it picks it up. **`.env` is
gitignored and the pre-commit hook blocks env files outright**, so it cannot be
committed by accident. It dies with the container — which is why step 2 is the
real answer and this is the stopgap.

**Do not paste the key into chat.** It ends up in the transcript.

## 4. Connect the server

```bash
claude mcp add sfx -- uv run --directory vendor/sfx-mcp sfx-mcp
```

`vendor/sfx-mcp` is already vendored and audited (MIT; talks only to
`freesound.org/apiv2`; hard-filters `license:"Creative Commons 0"` in the query
string). Full audit in `registry.md` beside this file.

Verify with `sfx_search(operation='list_local')`.

## 5. What to actually use it for

The synthesised pack in `office/asset-library/sfx/` already covers every UI
event — clicks, ticks, counters, payment, pass/fail/warning, whoosh, typing —
and is owned outright, which is a stronger licence position than CC0.

Freesound adds **the one thing synthesis cannot**: texture with a performance in
it. Real room tone, real mechanical noise, anything that should sound like a
*place* rather than an event. Reach for it there and nowhere else.

Cache every download into `office/asset-library/sfx/`, dedupe on `content_hash`,
and record the Freesound id, uploader and licence in `sfx-manifest.json`. **Do
not re-download per video.**

## 6. Honest priority

This key is now **optional**. The pilot's audio is already unblocked. The
remaining blocker on `PILOT-10` is that `hire_office($10)` has never been run, so
8 of 20 beats have no footage — that is worth more than any sound library.
