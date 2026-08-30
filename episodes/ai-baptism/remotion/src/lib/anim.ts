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
 * Slow drift applied to otherwise-static frames. The brief forbids more than
 * 12 static seconds; a frame that must hold (S11's face, S06's silence) still
 * breathes so it does not read as a freeze.
 */
export const breathe = (localFrame: number, amount = 0.012, periodSec = 9) =>
  1 + Math.sin((localFrame / (FPS * periodSec)) * Math.PI * 2) * amount;
