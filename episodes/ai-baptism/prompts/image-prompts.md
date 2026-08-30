# Image prompts — `ai-baptism`

**Read this first.** Most of this episode's visuals are **drawn in Remotion**,
not generated. That is a deliberate choice, not a fallback:

- Consistency is free. A generated church that changes between S01 and S13
  breaks the callback the ending depends on, and inconsistency between scenes is
  a mandatory failure in `video-red-team`.
- Korean type inside a generated image comes back as plausible nonsense.
- Timelines, UI panels, stat sheets and diagrams are *typographic* objects. A
  model renders a picture of one; Remotion renders one.
- It costs nothing per render and re-renders in seconds after a note.

So generation is reserved for the few shots where a *scene* is wanted behind the
typography. Those are below. Everything else is a component.

## Visual bible — applies to every generated shot

```
Editorial, restrained, contemplative. Cinematic but not cinematic-spectacle.
Dark ground (#0A0A0C), warm candlelight accent (#C9A227), cold accent (#4A7FB5).
16:9. Leave the lower third and generous negative space clear for Korean captions.

NEVER: cyberpunk, neon, glitch, circuit boards, chrome robots, lens flare,
holograms, HUD overlays, horror, gore, grotesque or sensational religious
imagery, the rendered face of Jesus or any religious figure, embedded text.
```

The `NEVER` list is not stylistic fussiness. Each entry is a way this specific
episode reads as unserious, and "AI video about AI" is the exact impression the
whole 74%-graphics structure exists to avoid.

---

## P-01 · Church interior (S01, S13)

Generate **once**. S13 must be the same room, same lens, same light, same
position as S01 — the callback is the ending's entire structural payoff, and a
second generation will not match.

```
A dark, near-empty church nave photographed from the rear. Stone columns recede
into shadow on both sides. A single arched wooden door stands at the far end,
slightly ajar, with warm low light spilling through it onto the stone floor.
No people. No crucifix in frame. No visible text or signage.
Deep shadow, one warm light source, heavy negative space in the lower half.
Quiet, ordinary, unremarkable — a working parish, not a cathedral.
Editorial photography, muted, restrained. 16:9.
```

## P-02 · The AI figure reference (S01, S02, S04, S05, S11, S13)

Generate **once** and drive every avatar clip from this single reference.
Regenerating per scene is the most common source of the inconsistency failure.

```
Portrait of a calm young adult of ambiguous presentation, seated, facing camera,
lit by a single soft key from one side against a near-black background.
Plain dark clothing, no logos, no patterns.
Neutral expression, still, unhurried.
Exactly one detail that is not human — a faint cold-blue light at the temple,
subtle enough to miss on first look.
No chrome, no visible seams, no glowing eyes, no android styling.
The face must read as a person until the viewer asks whether it is one.
Editorial portrait, shallow depth of field. 16:9.
```

**Why understated.** An obviously robotic face answers the episode's question in
the character design. The whole essay depends on the viewer being unable to
settle it by looking.

## P-03 · The duplicate pair (S06 — reference only)

Rendered as silhouettes in the composition. Generate only if a photographic
treatment is preferred over the drawn one.

```
Two visually identical young adults stand opposite each other in a quiet,
neutral, undecorated room. Face, clothing, posture and expression are
indistinguishable. Even, shadowless light. Nothing in the room dates it.
The image should evoke identity uncertainty, not science-fiction action.
Minimal, sophisticated, editorial. No cyberpunk neon. No horror.
16:9. Leave generous negative space for Korean captions.
```

## P-04 · Incarnation sequence (S08 — reference only)

Rendered as a continuous programmatic zoom. It has to be one uninterrupted
movement, which a set of generated stills cannot be — the claim is about a single
motion, not five pictures.

```
An abstract cinematic sequence expressing movement from immensity into concrete
historical particularity. Begin with a vast star-filled cosmic field, then narrow
progressively: cosmos → Earth → an ancient Near Eastern coastline → one small
settlement → one human silhouette.

The visual idea is NOT "God shrinking." It is the infinite entering a concrete
human history. Serious, restrained, contemplative.
Avoid kitsch religious imagery. Never depict the face of Jesus.
The final silhouette must remain a silhouette. 16:9.
```

## P-05 · Thumbnail plate

The thumbnail is a Remotion `<Still>` (`Thumbnail` composition) so it inherits
the episode's palette, fonts and visual language. Generate only the scene behind
the type if a photographic ground is wanted:

```
A humanoid figure in silhouette standing just inside a church doorway, seen from
inside the dark nave, warm light behind them. Figure at right of frame, large.
Left two-thirds of the frame nearly empty and dark for Korean headline type.
One small cold-blue light detail at the figure's temple.
No text in the image. Restrained, editorial, high contrast. 16:9.
```

---

## Provider routing

| Need | Route |
|---|---|
| Consistent reference stills (P-01, P-02) | ComfyUI or a hosted image model, generated **once**, stored in `assets/` |
| Diagrams, timelines, UI, typography | Remotion — never a model |
| Motion | Remotion |
| A shot the free path cannot make and a human can drive | `aicron` (GUI, human-in-the-loop, no API) |

Record provider, prompt, seed and licence for every generated asset in
`assets/manifest.json` before it enters a render.
