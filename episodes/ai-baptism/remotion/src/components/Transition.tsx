import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import {FPS} from '../theme';
import type {Scene} from '../lib/beats';

/**
 * Scene transitions, driven by the storyboard's `transitionOut`.
 *
 * The storyboard has declared these from the start and the composition ignored
 * them, so every boundary rendered as a hard cut — including the ones written
 * as a dip or a dissolve, where the cut fights the pacing the scene was built
 * for (S03 into S04, S08's near-silence, S13's fall to black).
 *
 * Scenes are non-overlapping Sequences, so the crossover is a short dip through
 * black rather than a true A-over-B dissolve. At these lengths that reads
 * correctly, and it keeps beat times episode-absolute — a real dissolve would
 * mean mounting a scene before its own start, which is the one thing the timing
 * model must never do.
 */
const OUT: Record<string, number> = {
  'hard-cut': 0,
  'wipe-left': 0.34,
  'cross-dissolve': 0.42,
  'dip-to-black': 0.58,
  end: 1.1,
};

/** How the incoming scene arrives, keyed by the PREVIOUS scene's transitionOut. */
const IN: Record<string, number> = {
  'hard-cut': 0,
  'wipe-left': 0.3,
  'cross-dissolve': 0.4,
  'dip-to-black': 0.5,
  end: 0,
};

export const SceneTransition: React.FC<{
  scene: Scene;
  /** transitionOut of the scene before this one; undefined for the first. */
  prevTransition?: string;
  children: React.ReactNode;
}> = ({scene, prevTransition, children}) => {
  const frame = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();

  const outSec = OUT[scene.transitionOut] ?? 0;
  const inSec = prevTransition ? IN[prevTransition] ?? 0 : 0;

  const fadeIn = inSec
    ? interpolate(frame, [0, inSec * FPS], [0, 1], {
        extrapolateLeft: 'clamp',
        extrapolateRight: 'clamp',
      })
    : 1;

  const fadeOut = outSec
    ? interpolate(
        frame,
        [durationInFrames - outSec * FPS, durationInFrames],
        [1, 0],
        {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}
      )
    : 1;

  const wipeIn = prevTransition === 'wipe-left' ? fadeIn : 1;
  const wipeOut = scene.transitionOut === 'wipe-left' ? fadeOut : 1;

  return (
    <AbsoluteFill
      style={{
        opacity: fadeIn * fadeOut,
        // A wipe travels; a fade does not. Pairing a small horizontal drift
        // with the fade is what separates the two visually at this length.
        transform:
          wipeIn < 1 || wipeOut < 1
            ? `translateX(${(1 - wipeIn) * 44 - (1 - wipeOut) * 44}px)`
            : undefined,
      }}
    >
      {children}
    </AbsoluteFill>
  );
};
