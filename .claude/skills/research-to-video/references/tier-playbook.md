# Tier playbook

Per-tier scene grammar and the asset checklist. Tiers are defined in SKILL.md;
this file is what to do once one is chosen.

## Tier A — code-drawn, $0, buildable now

Everything on screen is text, shape or chart. Nothing is sourced.

**Scene grammars that work at A:**

| Grammar | Shape | Measured evidence |
|---|---|---|
| **Calculation** | price → guess → question → itemised build → total | the highest-median channel in the KR set (11.16× subscribers, no video under 1× of its own median); its top comment praises the method, not the picture |
| **Ranked verdict** | claim → ranked bars → the one that breaks the pattern | a tier list ran 13.05× in the AI-tools set and farms omission arguments in the replies |
| **Receipt / audit** | header → line items with leaders → rule → total | `projects/the-bill` |
| **Distribution reveal** | setup number → method → the field → the outlier → the twist | `projects/gijunseon` |
| **Process narration** | question → step 1..n in order → **stop without a verdict** | 68.4× on the KR set; the comments supply the humour, the physics and the moral |

The last one is worth spelling out: **ending without a judgement is the format,
not an omission.** The channel that does it best states facts and stops, and its
comment section writes the opinion for it — 43,000 likes on a joke the video did
not make, 14,000 on a physics correction it did not offer.

**A-tier asset checklist:** a font that covers the script · a palette of two
colours and one accent · the numbers, each traceable to a research line. That is
all. If a shot needs anything else, it is not A.

## Tier B — public-domain / CC archive + code

Same grammars, with a footage or stills layer underneath.

**Sourcing:** `web-media-getter`, five no-key sources.

| Source | Best for | Licence reality |
|---|---|---|
| NASA | space, launches, earth imagery | public domain, the cleanest of the five |
| Wikimedia Commons | factual, historical, landmarks, specimens | per-item; PD and CC BY-SA mixed — read the item |
| Openverse | CC web images from Flickr and museums | per-item CC, attribution usually required |
| Internet Archive | historical film and images | per-item and often unclear; weakest relevance ranking |
| Library of Congress | US prints and photographs | per-item |

**Rules:**

- **A licence tag is not a licence check.** The tool reports what the API says.
  Open the item page for anything that ships.
- **Keep `attribution.json`.** `--download` writes it; commit it next to the
  clips. Attribution you cannot reconstruct is attribution you cannot give.
- **Ken Burns on stills, always.** Two of the KR channels' stock-led formats
  measured `ken_burns_push` and `ken_burns_pan`; a static still reads as a
  broken video.
- **Budget the search.** Relevance is the weak point, not availability. Expect to
  reject most of what comes back, and write the query in English even for a
  Korean video — these archives are indexed in English.

## Tier C — broadcast, film, news clips

Four of the nine KR channels live here, and they are the ones with the biggest
multiples. It is a real lane; it is not a free one.

**Do not storyboard a C-tier idea until the quotation scope is decided by a
person.** What has to be settled first: how much of a clip, whether commentary
is layered over it, which jurisdiction, and whether the platform's own rights
system will flag it regardless of the legal answer.

What this skill will do at C: say the tier, name the specific footage the idea
depends on, and offer the A/B rebuild. What it will not do: call it free, or
quietly proceed.

## Tier D — custom illustration, original shooting

Webtoon animation and tabletop demo both sit here. A recurring illustrated
character is a genuine moat — one KR channel's comments play with its characters'
names by the thousand — and it is an ongoing production cost, not a render
setting.

**The A-tier rebuild is usually available.** Ask what the format's engine
actually is. If the answer is "the calculation" or "the ordering" or "the
reveal", the pixels are replaceable and the idea moves to A.

## Choosing between A and B

Default to A. Add B only when a shot is *about a thing in the world* — a place,
a specimen, an event, a person. Text, numbers, comparisons, processes and
rankings are all better as code: sharper, re-editable, instantly re-renderable
when a number changes, and free.

The cost of a B layer is not money, it is search time and licence reading. Spend
it where footage carries meaning, not where it decorates.
