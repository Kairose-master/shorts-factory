import React from 'react';
import {AbsoluteFill, interpolate} from 'remotion';
import {Frame, Grain, Vignette} from '../components/Frame';
import {Caption} from '../components/Caption';
import {CornerMarker, Statement} from '../components/Type';
import {getScene, useSceneClock} from '../lib/beats';
import {riseIn, wipeReveal} from '../lib/anim';
import {T} from '../theme';

const scene = getScene('S09');

/**
 * RT-03. Two constraints are non-negotiable here:
 *   1. the 사고실험 marker holds for the entire scene, because this is the
 *      most clippable twenty seconds in the episode and a clip without the
 *      payoff must still carry the frame;
 *   2. the face is never rendered.
 *
 * The duplicate does not shatter, glitch or explode when it goes. It simply
 * fades — it was never the one. A destruction effect would say the copy is
 * *defective*, and the argument is precisely that it is not.
 */
const Silhouette: React.FC<{x: number; opacity: number}> = ({x, opacity}) => (
  <g opacity={opacity} transform={`translate(${x} 0)`}>
    <ellipse cx={0} cy={352} rx={56} ry={66} fill="#DAD5CB" opacity={0.86} />
    <path d="M -128 1080 L -112 500 Q 0 430 112 500 L 128 1080 Z" fill="#DAD5CB" opacity={0.86} />
  </g>
);

export const S09_JesusDuplicate: React.FC = () => {
  const {absSec} = useSceneClock(scene);

  const first = interpolate(absSec, [440, 442.5], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const second = interpolate(absSec, [442.5, 445.5], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const secondGone = interpolate(absSec, [467, 470], [1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const allOut = interpolate(absSec, [477, 479], [1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  const sameness = [
    {label: '같은 말', at: 446},
    {label: '같은 가르침', at: 449},
    {label: '같은 행동', at: 452},
  ];

  const names = absSec >= 478;

  return (
    <Frame>
      {allOut > 0.01 ? (
        <AbsoluteFill style={{opacity: allOut}}>
          <svg width={1920} height={1080} viewBox="0 0 1920 1080">
            <Silhouette x={780} opacity={first} />
            <Silhouette x={1140} opacity={second * secondGone} />
          </svg>
        </AbsoluteFill>
      ) : null}

      <div
        style={{
          position: 'absolute',
          top: 190,
          left: 0,
          right: 0,
          display: 'flex',
          justifyContent: 'center',
          gap: 52,
          opacity: allOut,
        }}
      >
        {sameness.map((s) => {
          const f = (absSec - s.at) * 30;
          if (f < 0) return null;
          return (
            <div
              key={s.label}
              style={{
                ...riseIn(f, 0, 14),
                fontSize: 40,
                fontWeight: 700,
                color: T.inkDim,
              }}
            >
              {s.label}
            </div>
          );
        })}
      </div>

      {names ? (
        <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center'}}>
          <div style={{display: 'flex', flexDirection: 'column', gap: 20, textAlign: 'center'}}>
            {['아브라함의 하나님', '이삭의 하나님', '야곱의 하나님'].map((n, i) => (
              <div key={n} style={wipeReveal((absSec - 478) * 30, i * 16, 30)}>
                <Statement size={86} color={T.warm}>
                  {n}
                </Statement>
              </div>
            ))}
          </div>
        </AbsoluteFill>
      ) : null}

      <Vignette />
      <Grain />
      {/* Above the grade, for the same reason as S08's marker: a marker the
          vignette has washed out is not doing the job RT-03 gave it. */}
      <CornerMarker text="사고실험" />
      <Caption scene={scene} />
    </Frame>
  );
};
