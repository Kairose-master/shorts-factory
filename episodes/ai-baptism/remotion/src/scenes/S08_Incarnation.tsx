import React from 'react';
import {AbsoluteFill, interpolate, random} from 'remotion';
import {Frame, Grain, Vignette} from '../components/Frame';
import {Caption} from '../components/Caption';
import {Statement, TheologyMarker} from '../components/Type';
import {getScene, useSceneClock} from '../lib/beats';
import {riseIn} from '../lib/anim';
import {T} from '../theme';

const scene = getScene('S08');

/** Zoom keyframes, lifted from the `zoom` field on the storyboard beats. */
const ZOOM: [number, number][] = [
  [355, 0], [358, 0], [363, 0.05], [368, 0.1], [373, 0.15],
  [378, 0.18], [380, 0.2], [383, 0.3], [390, 0.42], [398, 0.55],
  [403, 0.62], [407, 0.72], [411, 0.85], [416, 0.92], [420, 0.96], [435, 1.0],
];

const STARS = new Array(220).fill(0).map((_, i) => ({
  x: random(`x${i}`) * 1920,
  y: random(`y${i}`) * 1080,
  r: 0.5 + random(`r${i}`) * 1.9,
  o: 0.2 + random(`o${i}`) * 0.8,
}));

/**
 * One uninterrupted zoom from a star field to a single silhouette. It is a
 * single continuous motion rather than a sequence of cuts because the claim is
 * about one movement, not five pictures — and because 80 seconds of cuts here
 * would break the stillness the scene needs.
 *
 * Each layer scales exponentially and hands off to the next. The face is never
 * rendered (RT-03 and the brief's rule on religious imagery).
 */
const layerStyle = (z: number, inAt: number, outAt: number, power = 5.5) => {
  const local = (z - inAt) / (outAt - inAt);
  const scale = Math.pow(2, local * power);
  const opacity = interpolate(
    z,
    [inAt - 0.02, inAt + 0.04, outAt - 0.06, outAt + 0.02],
    [0, 1, 1, 0],
    {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}
  );
  return {transform: `scale(${scale})`, opacity};
};

export const S08_Incarnation: React.FC = () => {
  const {absSec} = useSceneClock(scene);

  const z = interpolate(
    absSec,
    ZOOM.map(([s]) => s),
    ZOOM.map(([, v]) => v),
    {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}
  );

  const title = absSec >= 378 && absSec < 383.4;
  const marker = absSec >= 416;
  const markerFade = interpolate(absSec, [416, 417.4], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  const chain = [
    {label: '무한', at: 403},
    {label: '역사', at: 407},
    {label: '특정한 때 · 특정한 장소 · 특정한 삶', at: 411},
  ];

  return (
    <Frame bg="#040406">
      {/* cosmos */}
      <AbsoluteFill style={layerStyle(z, 0, 0.34, 4.2)}>
        <svg width={1920} height={1080}>
          {STARS.map((s, i) => (
            <circle key={i} cx={s.x} cy={s.y} r={s.r} fill="#EDE8DC" opacity={s.o} />
          ))}
        </svg>
      </AbsoluteFill>

      {/* earth */}
      <AbsoluteFill style={layerStyle(z, 0.3, 0.58, 5.2)}>
        <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center'}}>
          <div
            style={{
              width: 520,
              height: 520,
              borderRadius: '50%',
              background:
                'radial-gradient(circle at 38% 34%, #24405C 0%, #16283A 52%, #070B10 100%)',
              boxShadow: `0 0 120px ${T.cold}22`,
            }}
          />
        </AbsoluteFill>
      </AbsoluteFill>

      {/* ancient Near East — a coastline, schematic, not a labelled map */}
      <AbsoluteFill style={layerStyle(z, 0.54, 0.78, 5.0)}>
        <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center'}}>
          <svg width={900} height={700} viewBox="0 0 900 700">
            <path
              d="M 120 40 C 260 120 300 240 268 340 C 240 430 300 520 380 600 L 420 700 L 900 700 L 900 0 L 200 0 Z"
              fill="#1A1712"
              stroke={T.warmSoft}
              strokeWidth={1.2}
              opacity={0.85}
            />
            <path d="M 0 0 L 120 40 C 260 120 300 240 268 340 C 240 430 300 520 380 600 L 420 700 L 0 700 Z" fill="#070B10" />
          </svg>
        </AbsoluteFill>
      </AbsoluteFill>

      {/* one settlement */}
      <AbsoluteFill style={layerStyle(z, 0.74, 0.9, 4.6)}>
        <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center'}}>
          <svg width={760} height={420} viewBox="0 0 760 420">
            {[0, 1, 2, 3, 4, 5, 6].map((i) => {
              const w = 60 + random(`w${i}`) * 46;
              const h = 54 + random(`h${i}`) * 62;
              const x = 60 + i * 96;
              return (
                <g key={i}>
                  <rect x={x} y={420 - h} width={w} height={h} fill="#241F18" stroke={T.warmSoft} strokeWidth={0.9} opacity={0.9} />
                  <rect x={x + w * 0.36} y={420 - h * 0.6} width={w * 0.24} height={h * 0.26} fill={T.warm} opacity={0.5} />
                </g>
              );
            })}
          </svg>
        </AbsoluteFill>
      </AbsoluteFill>

      {/* one human silhouette — face never rendered */}
      <AbsoluteFill style={layerStyle(z, 0.87, 1.06, 3.0)}>
        <AbsoluteFill style={{alignItems: 'center', justifyContent: 'flex-end'}}>
          <svg width={560} height={780} viewBox="0 0 560 780">
            <ellipse cx={280} cy={128} rx={62} ry={72} fill="#0B0B0E" />
            <path d="M 132 780 L 148 320 Q 280 246 412 320 L 428 780 Z" fill="#0B0B0E" />
          </svg>
        </AbsoluteFill>
      </AbsoluteFill>

      {title ? (
        <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center'}}>
          <div style={riseIn((absSec - 378) * 30, 0, 20)}>
            <Statement size={132} color={T.ink}>
              성육신
            </Statement>
          </div>
        </AbsoluteFill>
      ) : null}

      {/* 무한 → 역사 → 특정성, stacked at frame left, out of the caption band */}
      <div
        style={{
          position: 'absolute',
          left: T.safe,
          top: 260,
          display: 'flex',
          flexDirection: 'column',
          gap: 30,
        }}
      >
        {chain.map((c, i) => {
          const f = (absSec - c.at) * 30;
          if (f < 0 || absSec > 434) return null;
          return (
            <div key={c.label}>
              {i > 0 ? (
                <div style={{fontSize: 30, color: T.inkFaint, marginBottom: 14}}>↓</div>
              ) : null}
              <div
                style={{
                  ...riseIn(f, 0, 18),
                  fontSize: i === 2 ? 40 : 58,
                  fontWeight: 800,
                  color: i === 2 ? T.warm : T.ink,
                }}
              >
                {c.label}
              </div>
            </div>
          );
        })}
      </div>

      {/* RT-01: the marker holds for the entire metaphor, it does not flash. */}
      {marker ? <TheologyMarker text="※ 비유입니다 — 교리 정식이 아닙니다" opacity={markerFade} /> : null}

      <Vignette strength={0.62} />
      <Grain opacity={0.06} />
      <Caption scene={scene} />
    </Frame>
  );
};
