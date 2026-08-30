import React from 'react';
import {AbsoluteFill, interpolate} from 'remotion';
import {Frame, Grain, Vignette} from '../components/Frame';
import {Caption} from '../components/Caption';
import {Statement} from '../components/Type';
import {getScene, useSceneClock} from '../lib/beats';
import {draw, riseIn} from '../lib/anim';
import {T} from '../theme';

const scene = getScene('S05B');

/**
 * RT-02, the required red-team insert.
 *
 * Design constraint that matters more than it looks: neither column may be
 * visually favoured. Same weight, same colour, same size, symmetric placement,
 * no checkmark, no ordering cue. The scene names that traditions differ and
 * adjudicates nothing — if the graphic picks a winner, the graphic is making a
 * claim the script explicitly refuses to make.
 */
const Column: React.FC<{title: string; sub: string; opacity: number}> = ({
  title,
  sub,
  opacity,
}) => (
  <div style={{opacity, textAlign: 'center', width: 560}}>
    <div style={{fontSize: 54, fontWeight: 800, color: T.ink, letterSpacing: '-0.02em'}}>
      {title}
    </div>
    <div style={{fontSize: 32, color: T.inkDim, marginTop: 16, lineHeight: 1.5}}>
      {sub}
    </div>
  </div>
);

export const S05B_BaptismTraditions: React.FC = () => {
  const {absSec} = useSceneClock(scene);

  const left = interpolate(absSec, [195.5, 198], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const right = interpolate(absSec, [200, 202.5], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const bracket = draw(Math.max(0, absSec - 209), 1.2);
  const resolve = interpolate(absSec, [210.4, 212], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <Frame>
      <AbsoluteFill
        style={{
          alignItems: 'center',
          justifyContent: 'center',
          flexDirection: 'column',
          gap: 0,
          transform: `translateY(${-resolve * 60}px)`,
        }}
      >
        <div style={{display: 'flex', gap: 120, alignItems: 'flex-start'}}>
          <Column title="신앙고백 후 세례" sub="고백을 조건으로" opacity={left} />
          <Column title="유아 세례" sub="고백 이전에도" opacity={right} />
        </div>

        {bracket > 0 ? (
          <svg width={1320} height={130} viewBox="0 0 1320 130" style={{marginTop: 44}}>
            <path
              d={`M 180 0 L 180 ${44 * Math.min(1, bracket * 2)} L ${
                180 + 480 * bracket
              } ${44 * Math.min(1, bracket * 2)}`}
              fill="none"
              stroke={T.inkFaint}
              strokeWidth={2}
            />
            <path
              d={`M 1140 0 L 1140 ${44 * Math.min(1, bracket * 2)} L ${
                1140 - 480 * bracket
              } ${44 * Math.min(1, bracket * 2)}`}
              fill="none"
              stroke={T.inkFaint}
              strokeWidth={2}
            />
            <line
              x1={660}
              y1={44}
              x2={660}
              y2={44 + 56 * Math.max(0, bracket * 2 - 1)}
              stroke={T.warmSoft}
              strokeWidth={2}
            />
          </svg>
        ) : null}

        {resolve > 0.01 ? (
          <div style={{...riseIn((absSec - 210.4) * 30, 0, 26), opacity: resolve}}>
            <Statement size={76} color={T.warm}>
              세례는 공동체가 행하는 사건
            </Statement>
          </div>
        ) : null}
      </AbsoluteFill>

      <Vignette />
      <Grain />
      <Caption scene={scene} />
    </Frame>
  );
};
