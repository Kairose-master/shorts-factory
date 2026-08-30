import React from 'react';
import {AbsoluteFill, interpolate} from 'remotion';
import {Frame, Grain, Vignette} from '../components/Frame';
import {Caption} from '../components/Caption';
import {AvatarPlate} from '../components/AvatarPlate';
import {Statement} from '../components/Type';
import {getScene, useSceneClock} from '../lib/beats';
import {riseIn} from '../lib/anim';
import {T} from '../theme';

const scene = getScene('S01');

/** The nave: a dark room and one lit door. Drawn, not filmed — a photoreal
 *  church would be the single most AI-looking asset in the episode. */
const Nave: React.FC<{push: number; doorOpen: number; figure: number}> = ({
  push,
  doorOpen,
  figure,
}) => (
  <AbsoluteFill style={{transform: `scale(${1 + push * 0.16})`}}>
    <AbsoluteFill style={{background: '#08080A'}} />
    {/* Arched door frame */}
    <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center'}}>
      <svg width={1920} height={1080} viewBox="0 0 1920 1080">
        <defs>
          <linearGradient id="doorGlow" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor={T.warm} stopOpacity="0.85" />
            <stop offset="100%" stopColor={T.warm} stopOpacity="0.12" />
          </linearGradient>
          <filter id="soft">
            <feGaussianBlur stdDeviation="26" />
          </filter>
        </defs>
        {/* Interior columns, barely visible */}
        {[220, 430, 1490, 1700].map((x) => (
          <rect key={x} x={x} y={90} width={62} height={990} fill="#0E0E12" />
        ))}
        {/* The doorway aperture */}
        <path
          d="M 830 1080 L 830 470 A 130 130 0 0 1 1090 470 L 1090 1080 Z"
          fill="#0B0B0E"
          stroke="#17171C"
          strokeWidth={3}
        />
        {/* Light spilling through as it opens */}
        <g opacity={doorOpen}>
          <path
            d="M 830 1080 L 830 470 A 130 130 0 0 1 1090 470 L 1090 1080 Z"
            fill="url(#doorGlow)"
            filter="url(#soft)"
          />
          <path
            d="M 830 1080 L 830 470 A 130 130 0 0 1 1090 470 L 1090 1080 Z"
            fill="url(#doorGlow)"
            opacity={0.5}
          />
          {/* Floor throw */}
          <path
            d="M 830 1080 L 1090 1080 L 1330 1080 L 620 1080 Z"
            fill={T.warm}
            opacity={0.18}
            filter="url(#soft)"
          />
        </g>
        {/* The figure, entering as silhouette against the light */}
        <g opacity={figure}>
          <ellipse cx={960} cy={618} rx={44} ry={52} fill="#050506" />
          <path
            d="M 890 1080 L 898 760 Q 960 706 1022 760 L 1030 1080 Z"
            fill="#050506"
          />
        </g>
      </svg>
    </AbsoluteFill>
  </AbsoluteFill>
);

export const S01_ColdOpenChurch: React.FC = () => {
  const {localSec, beatIndex, frame} = useSceneClock(scene);

  const push = interpolate(localSec, [0, 5], [0, 1], {extrapolateRight: 'clamp'});
  const doorOpen = interpolate(localSec, [1.4, 4.2], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const figure = interpolate(localSec, [3.0, 4.8], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  // Hard cut at 5s to the face. Absolutely no dissolve — the cut is the shock.
  const onFace = localSec >= 5 && localSec < 14;
  const onTitle = localSec >= 16.4;

  return (
    <Frame>
      {!onFace && !onTitle ? (
        <Nave push={push} doorOpen={doorOpen} figure={figure} />
      ) : null}

      {onFace ? (
        <AvatarPlate sceneId="S01" role="ai" />
      ) : null}

      {onTitle ? (
        <AbsoluteFill
          style={{alignItems: 'center', justifyContent: 'center'}}
        >
          <div style={riseIn((localSec - 16.4) * 30, 0, 34)}>
            <Statement size={104} color={T.ink}>
              AI에게 세례를 줘도 될까?
            </Statement>
          </div>
        </AbsoluteFill>
      ) : null}

      <Vignette strength={onFace ? 0.72 : 0.5} />
      <Grain />
      {/* Beat 3 is the 2s silence on the face: no caption, and that is correct. */}
      {beatIndex === 3 ? null : <Caption scene={scene} />}
    </Frame>
  );
};
