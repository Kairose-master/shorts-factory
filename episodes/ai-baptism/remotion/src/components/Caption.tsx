import React from 'react';
import {AbsoluteFill} from 'remotion';
import {T} from '../theme';
import {STORYBOARD, cueAt, type Scene, useSceneClock} from '../lib/beats';
import {holdEnvelope} from '../lib/anim';

const KEYWORDS = STORYBOARD.emphasisKeywords;

/**
 * Captions are burned in because most of this audience watches muted on a
 * phone. Rules from the brief: 1–2 lines, never a paragraph, and only semantic
 * keywords are highlighted — highlighting everything highlights nothing.
 */
const emphasise = (line: string) => {
  const hits = KEYWORDS.filter((k) => line.includes(k)).sort(
    (a, b) => b.length - a.length
  );
  if (hits.length === 0) return <>{line}</>;
  const pattern = new RegExp(`(${hits.map(escapeRe).join('|')})`, 'g');
  return (
    <>
      {line.split(pattern).map((part, i) =>
        hits.includes(part) ? (
          <span key={i} style={{color: T.warm, fontWeight: 700}}>
            {part}
          </span>
        ) : (
          <React.Fragment key={i}>{part}</React.Fragment>
        )
      )}
    </>
  );
};

const escapeRe = (s: string) => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');

/** Break one VO line into at most two balanced caption lines. */
const wrap = (text: string, maxChars = 26): string[] => {
  if (text.length <= maxChars) return [text];
  const words = text.split(' ');
  if (words.length === 1) return [text];
  let best = 1;
  let bestDelta = Infinity;
  for (let i = 1; i < words.length; i++) {
    const a = words.slice(0, i).join(' ').length;
    const b = words.slice(i).join(' ').length;
    const delta = Math.abs(a - b) + Math.max(0, Math.max(a, b) - maxChars) * 3;
    if (delta < bestDelta) {
      bestDelta = delta;
      best = i;
    }
  }
  return [words.slice(0, best).join(' '), words.slice(best).join(' ')];
};

export const Caption: React.FC<{scene: Scene}> = ({scene}) => {
  const {absSec} = useSceneClock(scene);
  // Driven by measured narration, not by the beat grid — see `CUES`.
  const cue = cueAt(absSec);
  if (!cue) return null;

  const lines = wrap(cue.text);
  const opacity = holdEnvelope(absSec - cue.start, cue.end - cue.start, 0.22);
  const isAI = cue.speaker === 'ai' || cue.speaker === 'copy';

  return (
    <AbsoluteFill
      style={{
        justifyContent: 'flex-end',
        alignItems: 'center',
        paddingBottom: 1080 - T.captionBaseline,
        pointerEvents: 'none',
      }}
    >
      <div
        style={{
          position: 'absolute',
          left: 0,
          right: 0,
          bottom: 0,
          height: 420,
          opacity: opacity * 0.9,
          background:
            'linear-gradient(180deg, rgba(10,10,12,0) 0%, rgba(10,10,12,0.62) 58%, rgba(10,10,12,0.78) 100%)',
        }}
      />
      <div
        style={{
          position: 'relative',
          opacity,
          maxWidth: 1440,
          textAlign: 'center',
          fontSize: 46,
          lineHeight: 1.42,
          fontWeight: 500,
          letterSpacing: '-0.01em',
          color: isAI ? '#DCE6F2' : T.ink,
          textShadow: '0 2px 18px rgba(0,0,0,0.85)',
          fontStyle: isAI ? 'normal' : 'normal',
        }}
      >
        {isAI ? (
          <span
            style={{
              display: 'block',
              fontSize: 22,
              letterSpacing: '0.28em',
              color: T.cold,
              marginBottom: 14,
              fontWeight: 700,
            }}
          >
            AI
          </span>
        ) : null}
        {lines.map((l, i) => (
          <div key={i}>{emphasise(l)}</div>
        ))}
      </div>
    </AbsoluteFill>
  );
};
