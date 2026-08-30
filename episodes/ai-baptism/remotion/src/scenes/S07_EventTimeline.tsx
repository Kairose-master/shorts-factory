import React from 'react';
import {AbsoluteFill, interpolate} from 'remotion';
import {Frame, Grain, Vignette} from '../components/Frame';
import {Caption} from '../components/Caption';
import {AvatarPlate} from '../components/AvatarPlate';
import {Statement} from '../components/Type';
import {getScene, useSceneClock} from '../lib/beats';
import {draw, settle} from '../lib/anim';
import {T} from '../theme';

const scene = getScene('S07');

const EVENTS = [
  {label: '싸움', at: 300},
  {label: '사과', at: 303.5},
  {label: '여행', at: 307},
  {label: '약속', at: 310.5},
  {label: '용서', at: 314},
];

export const S07_EventTimeline: React.FC = () => {
  const {absSec} = useSceneClock(scene);

  const avatarOut = interpolate(absSec, [298, 300.5], [1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  /** At 318 the five separate events pull into one continuous strand — the
   *  visual claim that a life is not a list of remembered items. */
  const braid = interpolate(absSec, [318, 323], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: (t) => 1 - Math.pow(1 - t, 3),
  });

  const inequality = absSec >= 324 && absSec < 333.5;
  const ineqIn = interpolate(absSec, [324, 326], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const strokeNe = draw(Math.max(0, absSec - 327.5), 0.8);

  return (
    <Frame>
      {avatarOut > 0.01 ? (
        <AbsoluteFill style={{opacity: avatarOut}}>
          <AvatarPlate sceneId="S07" role="presenter" />
        </AbsoluteFill>
      ) : null}

      {!inequality && absSec >= 299 ? (
        <AbsoluteFill>
          <svg width={1920} height={1080} viewBox="0 0 1920 1080">
            {EVENTS.map((e, i) => {
              const f = (absSec - e.at) * 30;
              if (f < 0) return null;
              const p = settle(f);
              const spread = 1 - braid;
              const x = 300 + i * 330;
              const y = 500 + Math.sin(i * 1.7) * 120 * spread;
              return (
                <g key={e.label} opacity={Math.min(1, f / 8)}>
                  {i > 0 && absSec >= EVENTS[i].at ? (
                    <line
                      x1={300 + (i - 1) * 330}
                      y1={500 + Math.sin((i - 1) * 1.7) * 120 * spread}
                      x2={x}
                      y2={y}
                      stroke={T.warmSoft}
                      strokeWidth={1.5 + braid * 2}
                      opacity={0.35 + braid * 0.5}
                    />
                  ) : null}
                  <circle cx={x} cy={y} r={7 + p * 4} fill={T.warm} />
                  <text
                    x={x}
                    y={y - 44}
                    fill={T.ink}
                    fontSize={40}
                    fontWeight={700}
                    textAnchor="middle"
                    fontFamily={T.font}
                  >
                    {e.label}
                  </text>
                </g>
              );
            })}
          </svg>
        </AbsoluteFill>
      ) : null}

      {inequality ? (
        <AbsoluteFill
          style={{
            alignItems: 'center',
            justifyContent: 'center',
            flexDirection: 'column',
            gap: 22,
            opacity: ineqIn,
          }}
        >
          <Statement size={72} color={T.ink}>
            기억하는 것
          </Statement>
          <svg width={200} height={110} viewBox="0 0 200 110">
            <line x1={40} y1={38} x2={40 + 120} y2={38} stroke={T.inkDim} strokeWidth={5} opacity={ineqIn} />
            <line x1={40} y1={72} x2={40 + 120} y2={72} stroke={T.inkDim} strokeWidth={5} opacity={ineqIn} />
            {/* The slash is drawn last, and it is what the beat is about. */}
            <line
              x1={148}
              y1={14}
              x2={148 - 96 * strokeNe}
              y2={14 + 84 * strokeNe}
              stroke={T.alert}
              strokeWidth={7}
            />
          </svg>
          <Statement size={72} color={T.warm}>
            그 사건의 당사자였던 것
          </Statement>
        </AbsoluteFill>
      ) : null}

      <Vignette />
      <Grain />
      <Caption scene={scene} />
    </Frame>
  );
};
