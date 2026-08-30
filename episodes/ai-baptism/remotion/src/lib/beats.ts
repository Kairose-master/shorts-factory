import {useCurrentFrame, useVideoConfig} from 'remotion';
import storyboard from '../../../storyboard/storyboard.json';
import captionTrack from '../../../audio/caption-track.json';
import {FPS} from '../theme';

export type Beat = {
  t: number;
  dur: number;
  kind: string;
  speaker?: string;
  vo?: string | null;
  onScreen?: string | null;
  visual?: string;
  emphasis?: boolean;
  marker?: boolean;
  markerHold?: boolean;
  guard?: string;
  theology?: string;
  station?: number;
  event?: number;
  stat?: number;
  column?: string;
  converge?: number;
  zoom?: number;
};

export type Scene = {
  id: string;
  title: string;
  component: string;
  startSec: number;
  endSec: number;
  avatarSec: number;
  avatarRole?: string;
  voice?: string;
  audioNote?: string;
  redTeam?: string;
  transitionOut: string;
  beats: Beat[];
};

export const STORYBOARD = storyboard as unknown as {
  episodeId: string;
  fps: number;
  width: number;
  height: number;
  durationInFrames: number;
  emphasisKeywords: string[];
  scenes: Scene[];
};

export const getScene = (id: string): Scene => {
  const s = STORYBOARD.scenes.find((x) => x.id === id);
  if (!s) throw new Error(`storyboard has no scene ${id}`);
  return s;
};

/**
 * Beat times in storyboard.json are absolute episode seconds; inside a Sequence
 * the frame counter is scene-local. Everything here converts to scene-local so
 * a scene component never has to know where it sits in the episode.
 */
export const useSceneClock = (scene: Scene) => {
  const frame = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  const localSec = frame / FPS;
  const absSec = scene.startSec + localSec;
  const beatIndex = scene.beats.findIndex(
    (b) => absSec >= b.t && absSec < b.t + b.dur
  );
  const idx = beatIndex === -1 ? scene.beats.length - 1 : beatIndex;
  const beat = scene.beats[idx];
  const inBeat = absSec - beat.t;
  return {
    frame,
    localSec,
    absSec,
    durationInFrames,
    beat,
    beatIndex: idx,
    /** 0→1 across the current beat */
    beatProgress: Math.min(1, Math.max(0, inBeat / beat.dur)),
    /** seconds elapsed inside the current beat */
    inBeat,
    /** local frame at which a given absolute-second mark falls */
    at: (absoluteSec: number) => (absoluteSec - scene.startSec) * FPS,
  };
};

/** Beats whose `vo` is non-null, i.e. the ones that produce a caption. */
export const spokenBeats = (scene: Scene) => scene.beats.filter((b) => b.vo);

export type Cue = {
  start: number;
  end: number;
  text: string;
  speaker: string;
  scene: string;
};

/**
 * Where each line is ACTUALLY spoken, measured from the generated narration.
 *
 * Graphics stay on their authored beats — they are choreographed to the
 * argument, and a diagram that moves because a sentence ran long is a worse
 * defect than a caption that lingers. Captions have exactly one job, to match
 * the voice, so they read from here instead of from the beat grid. That split
 * is what lets a line overrun its beat without desyncing anything.
 */
export const CUES = captionTrack as unknown as Cue[];

export const cueAt = (absSec: number): Cue | null => {
  for (const c of CUES) {
    if (absSec >= c.start && absSec < c.end) return c;
  }
  return null;
};
