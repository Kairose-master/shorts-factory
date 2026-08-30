import React from 'react';
import {AbsoluteFill, interpolate} from 'remotion';
import {Frame, Grain, Vignette} from '../components/Frame';
import {Caption} from '../components/Caption';
import {AvatarPlate} from '../components/AvatarPlate';
import {Readout, Statement} from '../components/Type';
import {getScene, useSceneClock} from '../lib/beats';
import {draw, riseIn} from '../lib/anim';
import {T} from '../theme';

const scene = getScene('S04');

/** A head in wireframe with a scan bar. The UI is intentionally cheap — the
 *  joke only lands if it looks like something a product manager shipped. */
const Detector: React.FC<{absSec: number}> = ({absSec}) => {
  const scan = interpolate(absSec, [123, 127], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const meter = interpolate(absSec, [127, 130], [0, 0.93], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const stamp = interpolate(absSec, [130, 130.5], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const strike = draw(Math.max(0, absSec - 132), 0.45);
  const collapse = interpolate(absSec, [133.0, 134], [1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill
      style={{
        alignItems: 'center',
        justifyContent: 'center',
        opacity: collapse,
      }}
    >
      <div
        style={{
          border: `2px solid ${T.cold}`,
          background: 'rgba(18,22,30,0.94)',
          padding: '52px 78px',
          borderRadius: 6,
          position: 'relative',
          // The panel drops and shrinks as it goes rather than squashing flat —
          // a flattened panel reads as a render fault, not a rejection.
          transform: `translateY(${(1 - collapse) * 46}px) scale(${0.9 + collapse * 0.1})`,
          boxShadow: `0 0 90px ${T.cold}22`,
        }}
      >
        <Readout size={34} style={{marginBottom: 30, letterSpacing: '0.42em'}}>
          FAITH DETECTOR
        </Readout>

        <svg width={560} height={400} viewBox="0 0 420 300">
          {/* head outline */}
          <path
            d="M 210 34 C 292 34 330 96 330 158 C 330 214 296 258 262 268 L 262 300 L 158 300 L 158 268 C 124 258 90 214 90 158 C 90 96 128 34 210 34 Z"
            fill="none"
            stroke={T.cold}
            strokeWidth={1.6}
            opacity={0.75}
          />
          {[0, 1, 2, 3, 4].map((i) => (
            <path
              key={i}
              d={`M ${104 + i * 6} ${74 + i * 34} Q 210 ${52 + i * 34} ${316 - i * 6} ${74 + i * 34}`}
              fill="none"
              stroke={T.coldSoft}
              strokeWidth={1}
              opacity={0.5}
            />
          ))}
          {/* scan bar */}
          <rect
            x={78}
            y={34 + scan * 244}
            width={264}
            height={3}
            fill={T.cold}
            opacity={scan > 0 && scan < 1 ? 0.95 : 0.25}
          />
        </svg>

        <div style={{marginTop: 30, width: 560}}>
          <div
            style={{
              height: 30,
              border: `1px solid ${T.coldSoft}`,
              position: 'relative',
              background: '#0B0B0E',
            }}
          >
            <div
              style={{
                position: 'absolute',
                inset: 2,
                width: `calc(${meter * 100}% - 4px)`,
                background: T.cold,
                opacity: 0.85,
              }}
            />
          </div>
          <Readout size={40} style={{marginTop: 16}}>
            {Math.round(meter * 100)}%
          </Readout>
        </div>

        <div
          style={{
            marginTop: 22,
            opacity: stamp,
            transform: `scale(${1 + (1 - stamp) * 0.5}) rotate(-4deg)`,
            border: `3px solid ${T.cold}`,
            padding: '14px 28px',
            display: 'inline-block',
          }}
        >
          <Readout size={34} style={{letterSpacing: '0.2em'}}>
            BAPTISM APPROVED
          </Readout>
        </div>

        {/* The strike. No sound cue — the silence does the work. */}
        {strike > 0 ? (
          <svg
            style={{position: 'absolute', inset: 0, width: '100%', height: '100%'}}
            viewBox="0 0 100 100"
            preserveAspectRatio="none"
          >
            <line x1={4} y1={4} x2={4 + 92 * strike} y2={4 + 92 * strike} stroke={T.alert} strokeWidth={1.1} vectorEffect="non-scaling-stroke" style={{strokeWidth: 9}} />
            <line x1={96} y1={4} x2={96 - 92 * strike} y2={4 + 92 * strike} stroke={T.alert} strokeWidth={1.1} vectorEffect="non-scaling-stroke" style={{strokeWidth: 9}} />
          </svg>
        ) : null}
      </div>
    </AbsoluteFill>
  );
};

export const S04_FaithDetector: React.FC = () => {
  const {absSec, localSec} = useSceneClock(scene);

  const avatarPhase = absSec < 123;
  const uiPhase = absSec >= 123 && absSec < 134;

  return (
    <Frame>
      {avatarPhase ? (
        <AbsoluteFill>
          <AvatarPlate sceneId="S04" role="presenter" />
        </AbsoluteFill>
      ) : null}

      {uiPhase ? <Detector absSec={absSec} /> : null}

      {/* After the collapse: the three things we actually go on. */}
      {absSec >= 139 && absSec < 144 ? (
        <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center'}}>
          <div style={{...riseIn((absSec - 139) * 30), display: 'flex', gap: 56}}>
            {['말', '행동', '시간'].map((w, i) => (
              <div
                key={w}
                style={{
                  ...riseIn((absSec - 139) * 30, i * 9),
                  fontSize: 86,
                  fontWeight: 800,
                  color: T.warm,
                }}
              >
                {w}
              </div>
            ))}
          </div>
        </AbsoluteFill>
      ) : null}

      {absSec >= 114.5 && absSec < 123 ? (
        <AbsoluteFill
          style={{alignItems: 'center', justifyContent: 'flex-start', paddingTop: 180}}
        >
          <div style={riseIn((absSec - 115.5) * 30)}>
            <Statement size={68} color={T.inkDim}>
              진짜 믿는다는 걸 어떻게 압니까?
            </Statement>
          </div>
        </AbsoluteFill>
      ) : null}

      <Vignette />
      <Grain />
      <Caption scene={scene} />
    </Frame>
  );
};
