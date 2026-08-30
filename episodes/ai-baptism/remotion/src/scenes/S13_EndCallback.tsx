import React from 'react';
import {AbsoluteFill, interpolate} from 'remotion';
import {Frame, Grain, Vignette} from '../components/Frame';
import {Caption} from '../components/Caption';
import {AvatarPlate} from '../components/AvatarPlate';
import {Statement} from '../components/Type';
import {getScene, useSceneClock} from '../lib/beats';
import {riseIn} from '../lib/anim';
import {T} from '../theme';

const scene = getScene('S13');

/**
 * The callback. Identical framing to S01 — same aperture geometry, same light,
 * same position — because the point is that nothing about the situation has
 * changed except what we now know to ask.
 *
 * Ends on black with one caption. No end card, no subscribe animation, no
 * outro sting. That is a deliberate retention decision, not an omission: the
 * final question is the thing we want carried out of the video, and an outro
 * is the standard way to bury it.
 */
export const S13_EndCallback: React.FC = () => {
  const {absSec, localSec} = useSceneClock(scene);

  const doorPhase = absSec < 694;
  const faceIn = interpolate(absSec, [686.6, 687.4], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const faceOut = interpolate(absSec, [691, 691.6], [1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  const finalLine = absSec >= 700 && absSec < 706;
  const lastCaption = absSec >= 706;

  return (
    <Frame bg={doorPhase ? T.bg : '#000000'}>
      {doorPhase ? (
        <>
          <AbsoluteFill>
            <svg width={1920} height={1080} viewBox="0 0 1920 1080">
              <defs>
                <linearGradient id="endGlow" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor={T.warm} stopOpacity="0.7" />
                  <stop offset="100%" stopColor={T.warm} stopOpacity="0.1" />
                </linearGradient>
                <filter id="endSoft">
                  <feGaussianBlur stdDeviation="26" />
                </filter>
              </defs>
              {[220, 430, 1490, 1700].map((x) => (
                <rect key={x} x={x} y={90} width={62} height={990} fill="#0E0E12" />
              ))}
              <path
                d="M 830 1080 L 830 470 A 130 130 0 0 1 1090 470 L 1090 1080 Z"
                fill="url(#endGlow)"
                filter="url(#endSoft)"
              />
              {/* The pastor, back to camera, unmoving. */}
              <g opacity={interpolate(absSec, [690, 691.5], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'})}>
                <ellipse cx={700} cy={640} rx={50} ry={58} fill="#050506" />
                <path d="M 620 1080 L 630 790 Q 700 732 770 790 L 780 1080 Z" fill="#050506" />
              </g>
            </svg>
          </AbsoluteFill>

          {faceIn * faceOut > 0.01 ? (
            <AbsoluteFill style={{opacity: faceIn * faceOut}}>
              <AvatarPlate sceneId="S13" role="ai" />
            </AbsoluteFill>
          ) : null}

          {absSec >= 691 && absSec < 694 ? (
            <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center'}}>
              <Statement size={92} color={T.inkDim}>
                …
              </Statement>
            </AbsoluteFill>
          ) : null}
        </>
      ) : null}

      {finalLine ? (
        <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center'}}>
          <div style={riseIn((absSec - 700) * 30, 0, 30)}>
            <Statement size={80} color={T.ink}>
              {'"그래서 너와 바로 그 하나님 사이에는\n무슨 일이 있었는데?"'}
            </Statement>
          </div>
        </AbsoluteFill>
      ) : null}

      {lastCaption ? (
        <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center'}}>
          <div
            style={{
              ...riseIn((absSec - 706) * 30, 0, 18),
              opacity: interpolate(absSec, [706, 707, 709, 710], [0, 1, 1, 0], {
                extrapolateLeft: 'clamp',
                extrapolateRight: 'clamp',
              }),
            }}
          >
            <Statement size={68} color={T.inkDim} weight={500}>
              여러분이라면 세례를 주시겠습니까?
            </Statement>
          </div>
        </AbsoluteFill>
      ) : null}

      {doorPhase ? <Vignette /> : null}
      <Grain opacity={doorPhase ? 0.05 : 0.03} />
      {finalLine || lastCaption ? null : <Caption scene={scene} />}
    </Frame>
  );
};
