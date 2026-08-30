import {continueRender, delayRender, staticFile} from 'remotion';

/**
 * The container has no Korean font installed — `fc-list` finds only
 * NotoColorEmoji — so every Hangul glyph renders as tofu unless we load one
 * ourselves. Pretendard (SIL OFL 1.1) is vendored under public/fonts.
 */
const FACES: [string, number][] = [
  ['Pretendard-Regular', 400],
  ['Pretendard-Medium', 500],
  ['Pretendard-Bold', 700],
  ['Pretendard-ExtraBold', 800],
];

let started = false;

export const loadFonts = () => {
  if (started) return;
  started = true;
  const handle = delayRender('Loading Pretendard');
  Promise.all(
    FACES.map(async ([file, weight]) => {
      const face = new FontFace('Pretendard', `url(${staticFile(`fonts/${file}.woff2`)})`, {
        weight: String(weight),
      });
      await face.load();
      (document.fonts as unknown as {add: (f: FontFace) => void}).add(face);
    })
  )
    .then(() => continueRender(handle))
    .catch(() => continueRender(handle));
};

/**
 * Warm = church, history, the particular.
 * Cold = UI, scoring, machine-reading.
 * The two are never mixed inside one beat. That contrast carries the argument,
 * so treat a warm accent inside a cold panel as a deliberate authored event
 * (S02's question mark, S03's midpoint) rather than decoration.
 */
export const T = {
  bg: '#0A0A0C',
  bgLift: '#141419',
  ink: '#F2EFE9',
  inkDim: '#8B8880',
  inkFaint: '#4A4844',
  warm: '#C9A227',
  warmSoft: '#8A7326',
  cold: '#4A7FB5',
  coldSoft: '#2B4A69',
  alert: '#B5484A',
  font: 'Pretendard, sans-serif',
  mono: 'ui-monospace, "SF Mono", Menlo, monospace',
  safe: 96,
  captionBaseline: 900,
} as const;

export const FPS = 30;
export const sec = (s: number) => Math.round(s * FPS);
