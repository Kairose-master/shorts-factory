import React from 'react';
import {AbsoluteFill, interpolate} from 'remotion';
import {Frame, Grain, Safe, Vignette} from '../components/Frame';
import {Caption} from '../components/Caption';
import {AvatarPlate} from '../components/AvatarPlate';
import {getScene, useSceneClock} from '../lib/beats';
import {draw, riseIn, settle} from '../lib/anim';
import {T} from '../theme';

const scene = getScene('S02');

const NODES = [
  {label: 'AI', at: 40},
  {label: '프로그램', at: 45},
  {label: '그러므로 세례 불가?', at: 49},
];

/** The objection stack. Cold, because it is a machine-shaped inference about
 *  a machine — and its last arrow is the only warm thing in frame. */
const Stack: React.FC<{absSec: number}> = ({absSec}) => (
  <div
    style={{
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      gap: 26,
    }}
  >
    {NODES.map((n, i) => {
      const f = (absSec - n.at) * 30;
      if (f < 0) return null;
      const s = settle(f);
      return (
        <React.Fragment key={n.label}>
          {i > 0 ? (
            <svg width={40} height={62} style={{opacity: Math.min(1, f / 8)}}>
              <line
                x1={20}
                y1={0}
                x2={20}
                y2={12 + draw(Math.max(0, absSec - n.at), 0.4) * 38}
                stroke={T.coldSoft}
                strokeWidth={2.5}
              />
              <polygon points="20,62 13,48 27,48" fill={T.coldSoft} opacity={draw(Math.max(0, absSec - n.at - 0.3), 0.3)} />
            </svg>
          ) : null}
          <div
            style={{
              opacity: Math.min(1, f / 10),
              transform: `translateY(${(1 - s) * 18}px)`,
              border: `1.5px solid ${T.coldSoft}`,
              borderRadius: 8,
              padding: '22px 46px',
              fontSize: 48,
              fontWeight: 700,
              color: T.cold,
              background: 'rgba(43,74,105,0.09)',
              letterSpacing: '-0.01em',
            }}
          >
            {n.label}
          </div>
        </React.Fragment>
      );
    })}
  </div>
);

export const S02_ObjectionStack: React.FC = () => {
  const {absSec, localSec} = useSceneClock(scene);

  // The avatar occupies the left third for the whole spoken portion (26s of 35).
  const avatarOut = interpolate(absSec, [45, 48], [1, 0.18], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  // The trailing "?" scales up and turns warm — the first crack in the argument.
  const qF = (absSec - 52) * 30;
  const qScale = qF > 0 ? interpolate(qF, [0, 26], [1, 6], {extrapolateRight: 'clamp', easing: (t) => 1 - Math.pow(1 - t, 3)}) : 0;

  return (
    <Frame>
      <AbsoluteFill style={{flexDirection: 'row'}}>
        <div style={{width: '42%', opacity: avatarOut, position: 'relative'}}>
          <AvatarPlate sceneId="S02" role="presenter" />
        </div>
        <div
          style={{
            width: '58%',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
          }}
        >
          <Stack absSec={absSec} />
        </div>
      </AbsoluteFill>

      {qScale > 0 ? (
        <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center'}}>
          <div
            style={{
              fontSize: 120,
              fontWeight: 800,
              color: T.warm,
              transform: `scale(${qScale})`,
              opacity: interpolate(qF, [0, 8, 70, 90], [0, 1, 1, 0.9], {extrapolateRight: 'clamp'}),
            }}
          >
            ?
          </div>
        </AbsoluteFill>
      ) : null}

      {/* Quoted objections, set apart from the caption band. */}
      {absSec >= 24 && absSec < 34 ? (
        <Safe style={{justifyContent: 'flex-start', alignItems: 'flex-start'}}>
          <div
            style={{
              ...riseIn((localSec - 4) * 30),
              fontSize: 34,
              color: T.inkDim,
              fontStyle: 'italic',
              maxWidth: 620,
              lineHeight: 1.6,
            }}
          >
            {absSec >= 27.5 ? '"너는 그냥 프로그램이잖아."' : '"아니, 너 AI잖아."'}
          </div>
        </Safe>
      ) : null}

      <Vignette />
      <Grain />
      <Caption scene={scene} />
    </Frame>
  );
};
