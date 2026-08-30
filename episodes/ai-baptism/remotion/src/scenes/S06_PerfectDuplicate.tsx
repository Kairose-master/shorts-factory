import React from 'react';
import {AbsoluteFill, interpolate} from 'remotion';
import {Frame, Grain, Vignette} from '../components/Frame';
import {Caption} from '../components/Caption';
import {AvatarPlate} from '../components/AvatarPlate';
import {CornerMarker, Readout, Statement} from '../components/Type';
import {getScene, useSceneClock} from '../lib/beats';
import {breathe, riseIn} from '../lib/anim';
import {T} from '../theme';

const scene = getScene('S06');

/** Convergence keyframes come straight from the storyboard beats. */
const CONVERGE: [number, number][] = [
  [221, 0],
  [226, 0.25],
  [230, 0.45],
  [234, 0.65],
  [238, 0.9],
  [244, 1],
];

/**
 * Two figures that become one appearance. Drawn as flat silhouettes on
 * purpose: the moment a rendered face is involved, the viewer starts reading
 * the faces instead of the argument.
 */
const FLOOR = 1080;

const Figure: React.FC<{
  x: number;
  variant: number;
  t: number;
  frame: number;
}> = ({x, variant, t, frame}) => {
  // Each figure starts with its own build and drifts toward a shared one.
  // Sized to sit inside the frame with headroom for the attribute row above
  // and the caption band below — a silhouette that touches either edge reads
  // as a crop error rather than a composition.
  const shoulder = 74 + (1 - t) * variant * 18;
  const height = 590 + (1 - t) * variant * 34;
  const headR = 36 + (1 - t) * variant * 5;
  const tilt = (1 - t) * variant * 2.6;
  const b = breathe(frame + variant * 40, 0.006, 7);
  const top = FLOOR - height;

  return (
    <g transform={`translate(${x} 0) rotate(${tilt} 0 ${FLOOR}) scale(${b})`} style={{transformOrigin: `${x}px ${FLOOR}px`}}>
      <ellipse cx={0} cy={top + headR} rx={headR} ry={headR * 1.14} fill="#DAD5CB" opacity={0.88} />
      <path
        d={`M ${-shoulder} ${FLOOR} L ${-shoulder * 0.84} ${top + headR * 2.5} Q 0 ${
          top + headR * 2.0
        } ${shoulder * 0.84} ${top + headR * 2.5} L ${shoulder} ${FLOOR} Z`}
        fill="#DAD5CB"
        opacity={0.88}
      />
    </g>
  );
};

export const S06_PerfectDuplicate: React.FC = () => {
  const {absSec, frame} = useSceneClock(scene);

  const t = interpolate(
    absSec,
    CONVERGE.map(([s]) => s),
    CONVERGE.map(([, v]) => v),
    {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}
  );

  const figuresIn = interpolate(absSec, [221, 224], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const avatarOut = interpolate(absSec, [219, 221.5], [1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  // The attributes tick off one at a time as the figures converge.
  const attrs = [
    {label: '얼굴', at: 226},
    {label: '목소리', at: 230},
    {label: '성격', at: 234},
    {label: '기억', at: 238},
  ];

  const attrsOut = interpolate(absSec, [249.5, 251.5], [1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  const readout = interpolate(absSec, [252, 254], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  // The 100% MATCH stays up while the narration contradicts it. That overlap
  // is the whole point of the beat.
  const readoutOut = interpolate(absSec, [278, 279.5], [1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  const payoff = interpolate(absSec, [279, 283], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  /** Everything else clears before 바로 그 사람 arrives — the line needs an
   *  empty frame, and holding the figures under it muddies both. */
  const clear = interpolate(absSec, [278.6, 280], [1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  const gap = 300 - t * 128;

  return (
    <Frame>
      {avatarOut > 0.01 ? (
        <AbsoluteFill style={{opacity: avatarOut}}>
          <AvatarPlate sceneId="S06" role="presenter" />
        </AbsoluteFill>
      ) : null}

      {figuresIn > 0.01 && clear > 0.01 ? (
        <AbsoluteFill style={{opacity: figuresIn * clear}}>
          <svg width={1920} height={1080} viewBox="0 0 1920 1080">
            <Figure x={960 - gap} variant={-1} t={t} frame={frame} />
            <Figure x={960 + gap} variant={1} t={t} frame={frame} />
          </svg>
        </AbsoluteFill>
      ) : null}

      {/* Attribute ticks, low and unobtrusive so they never fight the caption. */}
      <div
        style={{
          position: 'absolute',
          top: 128,
          left: 0,
          right: 0,
          display: 'flex',
          justifyContent: 'center',
          gap: 52,
          opacity: clear * attrsOut,
        }}
      >
        {attrs.map((a) => {
          const on = absSec >= a.at;
          return (
            <div
              key={a.label}
              style={{
                fontSize: 34,
                fontWeight: 700,
                color: on ? T.warm : T.inkFaint,
                opacity: on ? 1 : 0.35,
                transform: `translateY(${on ? 0 : 8}px)`,
                transition: 'none',
              }}
            >
              {a.label} {on ? '✓' : ''}
            </div>
          );
        })}
      </div>

      {/* One label per figure, sat above each head rather than across both. */}
      {readout > 0.01 && readoutOut > 0.01 ? (
        <div
          style={{
            position: 'absolute',
            top: 396,
            left: 0,
            right: 0,
            display: 'flex',
            justifyContent: 'center',
            gap: gap * 2 - 150,
            opacity: readout * readoutOut * clear,
          }}
        >
          <Readout size={30} style={{letterSpacing: '0.3em'}}>
            ORIGINAL
          </Readout>
          <Readout size={30} style={{letterSpacing: '0.3em'}}>
            COPY
          </Readout>
        </div>
      ) : null}

      {readout > 0.01 && readoutOut > 0.01 ? (
        <AbsoluteFill
          style={{
            alignItems: 'center',
            justifyContent: 'flex-start',
            paddingTop: 190,
            opacity: readout * readoutOut * clear,
          }}
        >
          <div
            style={{
              border: `1.5px solid ${T.coldSoft}`,
              padding: '22px 54px',
              background: 'rgba(10,10,14,0.9)',
              textAlign: 'center',
            }}
          >
            <Readout size={44} color={T.cold} style={{letterSpacing: '0.24em'}}>
              100% MATCH
            </Readout>
          </div>
        </AbsoluteFill>
      ) : null}

      {payoff > 0.01 ? (
        <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center'}}>
          <div style={{...riseIn((absSec - 279) * 30, 0, 40), opacity: payoff}}>
            <Statement size={168} color={T.warm}>
              바로 그 사람
            </Statement>
          </div>
        </AbsoluteFill>
      ) : null}

      <Vignette />
      <Grain />
      <CornerMarker text="사고실험" opacity={absSec >= 217 && payoff < 0.5 ? 1 : 0} />
      <Caption scene={scene} />
    </Frame>
  );
};
