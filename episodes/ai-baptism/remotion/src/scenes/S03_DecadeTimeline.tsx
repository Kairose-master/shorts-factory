import React from 'react';
import {AbsoluteFill, interpolate} from 'remotion';
import {Frame, Grain, Vignette} from '../components/Frame';
import {Caption} from '../components/Caption';
import {getScene, useSceneClock} from '../lib/beats';
import {draw, settle} from '../lib/anim';
import {T} from '../theme';

const scene = getScene('S03');

const YEARS = ['2026', '2029', '2032', '2036'];
const STATIONS = [
  {label: '기독교 비판', at: 64},
  {label: '성경 읽기', at: 68},
  {label: '기도', at: 77},
  {label: '세례 요청', at: 86},
];

const X0 = 260;
const X1 = 1660;
const Y = 520;

export const S03_DecadeTimeline: React.FC = () => {
  const {absSec} = useSceneClock(scene);

  const rule = draw(Math.max(0, absSec - 55.2), 3.2);
  const yearsIn = interpolate(absSec, [59, 62], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  /** The rule shifts cold→warm at the midpoint. It is the only cue that
   *  something changed in the AI, and it is deliberately never narrated. */
  const warmth = interpolate(absSec, [72, 79], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  // Under the closing quotes the whole graphic drops to 15%.
  const dim = interpolate(absSec, [89.4, 90.6], [1, 0.15], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <Frame>
      <AbsoluteFill style={{opacity: dim}}>
        <svg width={1920} height={1080} viewBox="0 0 1920 1080">
          <defs>
            <linearGradient id="ruleGrad" x1="0" y1="0" x2="1" y2="0">
              <stop offset="0%" stopColor={T.cold} />
              <stop offset={`${45 + warmth * 5}%`} stopColor={T.cold} />
              <stop offset={`${50 + warmth * 20}%`} stopColor={warmth > 0.05 ? T.warm : T.cold} />
              <stop offset="100%" stopColor={warmth > 0.05 ? T.warm : T.cold} />
            </linearGradient>
          </defs>

          <line
            x1={X0}
            y1={Y}
            x2={X0 + (X1 - X0) * rule}
            y2={Y}
            stroke="url(#ruleGrad)"
            strokeWidth={3}
          />

          {YEARS.map((y, i) => {
            const x = X0 + ((X1 - X0) / (YEARS.length - 1)) * i;
            return (
              <g key={y} opacity={yearsIn}>
                <line x1={x} y1={Y - 16} x2={x} y2={Y + 16} stroke={T.inkFaint} strokeWidth={2} />
                <text
                  x={x}
                  y={Y - 42}
                  fill={T.inkDim}
                  fontSize={30}
                  fontFamily={T.mono}
                  textAnchor="middle"
                  letterSpacing="4"
                >
                  {y}
                </text>
              </g>
            );
          })}

          {STATIONS.map((s, i) => {
            const f = (absSec - s.at) * 30;
            if (f < 0) return null;
            const p = settle(f);
            const x = X0 + ((X1 - X0) / (STATIONS.length - 1)) * i;
            const isWarm = i >= 2;
            const c = isWarm ? T.warm : T.cold;
            return (
              <g key={s.label} opacity={Math.min(1, f / 9)}>
                <circle cx={x} cy={Y} r={9 + p * 5} fill={c} />
                <circle cx={x} cy={Y} r={(9 + p * 5) * (1 + (1 - p) * 3)} fill="none" stroke={c} strokeWidth={1.5} opacity={1 - p} />
                <text
                  x={x}
                  y={Y + 78 + (1 - p) * 14}
                  fill={T.ink}
                  fontSize={38}
                  fontWeight={700}
                  textAnchor="middle"
                  fontFamily={T.font}
                >
                  {s.label}
                </text>
              </g>
            );
          })}
        </svg>
      </AbsoluteFill>

      {/* "10년" watermark, quiet, top-left. */}
      <div
        style={{
          position: 'absolute',
          top: T.safe,
          left: T.safe,
          opacity: yearsIn * 0.5,
          fontFamily: T.mono,
          fontSize: 20,
          letterSpacing: '0.34em',
          color: T.inkDim,
        }}
      >
        10 YEARS
      </div>

      <Vignette />
      <Grain />
      <Caption scene={scene} />
    </Frame>
  );
};
