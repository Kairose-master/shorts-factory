import React from 'react';
import {AbsoluteFill, OffthreadVideo, staticFile, useCurrentFrame} from 'remotion';
import {T} from '../theme';
import {breathe} from '../lib/anim';
import manifest from '../avatarManifest.json';

const CLIPS = (manifest as {clips: Record<string, string>}).clips;

export type AvatarRole = 'ai' | 'presenter';

/**
 * The avatar slot.
 *
 * When a lip-synced clip has been produced for this scene it plays here. When
 * one has not — which is the state of this container, because MuseTalk 1.5 and
 * EchoMimicV2 both need CUDA and there is no GPU — the slot falls back to a
 * designed portrait plate rather than a grey box, so the composition renders,
 * times and reviews correctly before any avatar exists.
 *
 * The fallback is deliberately not a fake face. A bad face is worse than none:
 * the whole reason this episode is 74% motion graphics is that a mediocre
 * talking head is what makes a video smell synthetic.
 */
export const AvatarPlate: React.FC<{
  sceneId: string;
  role: AvatarRole;
  /** 0→1 across the avatar's own on-screen window; drives the breathing. */
  style?: React.CSSProperties;
}> = ({sceneId, role, style}) => {
  const frame = useCurrentFrame();
  const clip = CLIPS[sceneId];
  const scale = breathe(frame, 0.008, 11);

  if (clip) {
    return (
      <AbsoluteFill style={{...style}}>
        <OffthreadVideo
          src={staticFile(`avatar/${clip}`)}
          style={{width: '100%', height: '100%', objectFit: 'cover'}}
        />
      </AbsoluteFill>
    );
  }

  const key = role === 'ai' ? T.cold : T.warm;

  return (
    <AbsoluteFill style={{...style, overflow: 'hidden'}}>
      <AbsoluteFill
        style={{
          transform: `scale(${scale})`,
          background:
            role === 'ai'
              ? `radial-gradient(ellipse 46% 58% at 50% 44%, ${T.bgLift} 0%, ${T.bg} 72%)`
              : `radial-gradient(ellipse 52% 62% at 50% 46%, #1A1712 0%, ${T.bg} 74%)`,
        }}
      />
      {/* Key light from one side — the single cue that reads as "a lit face
          is here", without drawing a face. */}
      <AbsoluteFill
        style={{
          transform: `scale(${scale})`,
          background: `radial-gradient(ellipse 26% 34% at ${
            role === 'ai' ? 44 : 56
          }% 42%, ${key}22 0%, transparent 70%)`,
        }}
      />
      <AbsoluteFill
        style={{
          alignItems: 'center',
          justifyContent: 'center',
          flexDirection: 'column',
          gap: 18,
        }}
      >
        <div
          style={{
            width: 208,
            height: 268,
            borderRadius: '50% 50% 46% 46% / 58% 58% 42% 42%',
            border: `1.5px solid ${key}55`,
            background: `linear-gradient(180deg, ${key}14 0%, transparent 82%)`,
            transform: `scale(${scale})`,
          }}
        />
        <div
          style={{
            fontFamily: T.mono,
            fontSize: 15,
            letterSpacing: '0.3em',
            color: `${key}88`,
          }}
        >
          {role === 'ai' ? 'AVATAR · AI' : 'AVATAR · PRESENTER'}
        </div>
        <div
          style={{
            fontFamily: T.mono,
            fontSize: 12,
            letterSpacing: '0.16em',
            color: T.inkFaint,
          }}
        >
          {sceneId} · awaiting lip-sync render
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
