import type React from 'react';
import {interpolate, spring} from 'remotion';
import {FPS} from '../theme';

/** Fade + rise, the default entrance for every text element in the episode. */
export const riseIn = (localFrame: number, delayFrames = 0, distance = 28) => {
  const f = localFrame - delayFrames;
  const opacity = interpolate(f, [0, 14], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const y = interpolate(f, [0, 20], [distance, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: (t) => 1 - Math.pow(1 - t, 3),
  });
  return {opacity, transform: `translateY(${y}px)`};
};

/** Symmetric in/out envelope, in seconds, for something that appears and leaves. */
export const holdEnvelope = (
  elapsedSec: number,
  durSec: number,
  fadeSec = 0.5
) =>
  interpolate(
    elapsedSec,
    [0, fadeSec, Math.max(fadeSec, durSec - fadeSec), durSec],
    [0, 1, 1, 0],
    {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}
  );

/** A settle with weight — used where an element should feel placed, not slid. */
export const settle = (localFrame: number, delayFrames = 0) =>
  spring({
    frame: localFrame - delayFrames,
    fps: FPS,
    config: {damping: 200, mass: 0.6, stiffness: 90},
  });

/** Draws a stroke 0→1 over `durSec`, used for rules, arrows and the ≠. */
export const draw = (elapsedSec: number, durSec: number) =>
  interpolate(elapsedSec, [0, durSec], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: (t) => 1 - Math.pow(1 - t, 2),
  });

/**
 * The episode's signature motion.
 *
 * Every channel wants one behaviour a viewer recognises across videos. Ours is
 * a bottom-up mask wipe: a statement is uncovered rather than faded in, as if
 * it were already there and the frame moved off it. It suits an essay whose
 * whole claim is that the answer was always in front of the viewer and the
 * question was wrong.
 *
 * Returns a CSS mask. Pair with a small upward drift; the two together read as
 * craft, while a fade alone reads as a default.
 */
export const wipeReveal = (localFrame: number, delayFrames = 0, durFrames = 26) => {
  const p = interpolate(localFrame - delayFrames, [0, durFrames], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: (t) => 1 - Math.pow(1 - t, 3),
  });
  // The soft edge is what sells it. A hard edge reads as a loading bar.
  const top = (1 - p) * 118;
  const grad = `linear-gradient(to top, #000 0%, #000 ${Math.max(
    0,
    100 - top
  )}%, transparent ${Math.max(0, 100 - top + 16)}%, transparent 100%)`;
  return {
    WebkitMaskImage: grad,
    maskImage: grad,
    transform: `translateY(${(1 - p) * 16}px)`,
    opacity: interpolate(localFrame - delayFrames, [0, 6], [0, 1], {
      extrapolateLeft: 'clamp',
      extrapolateRight: 'clamp',
    }),
  } as React.CSSProperties;
};

/**
 * Slow drift applied to otherwise-static frames. The brief forbids more than
 * 12 static seconds; a frame that must hold (S11's face, S06's silence) still
 * breathes so it does not read as a freeze.
 */
export const breathe = (localFrame: number, amount = 0.012, periodSec = 9) =>
  1 + Math.sin((localFrame / (FPS * periodSec)) * Math.PI * 2) * amount;
