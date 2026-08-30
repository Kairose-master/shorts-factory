import React from 'react';
import {AbsoluteFill} from 'remotion';
import {Grain, Vignette} from './components/Frame';
import {loadFonts, T} from './theme';

/**
 * Thumbnail concept A — "저도 믿는데요?"
 *
 * The brief rules out "인간이랑 뭐가 달라?" because that framing sells the video
 * as a human-similarity argument, which is the one reading the episode spends
 * eleven minutes refusing. "저도 믿는데요?" puts the claim in the AI's mouth and
 * leaves the judgement to the viewer — same curiosity, correct thesis.
 *
 * Must be readable without the title: church, a figure that is clearly not a
 * person, and the line.
 */
export const Thumbnail: React.FC = () => {
  loadFonts();
  return (
    <AbsoluteFill style={{backgroundColor: '#08080A', fontFamily: T.font}}>
      <AbsoluteFill>
        <svg width={1920} height={1080} viewBox="0 0 1920 1080">
          <defs>
            <linearGradient id="tGlow" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor={T.warm} stopOpacity="0.9" />
              <stop offset="100%" stopColor={T.warm} stopOpacity="0.12" />
            </linearGradient>
            <filter id="tSoft">
              <feGaussianBlur stdDeviation="30" />
            </filter>
          </defs>
          {[120, 330] .map((x) => (
            <rect key={x} x={x} y={60} width={70} height={1020} fill="#0E0E12" />
          ))}
          <path
            d="M 1180 1080 L 1180 380 A 170 170 0 0 1 1520 380 L 1520 1080 Z"
            fill="url(#tGlow)"
            filter="url(#tSoft)"
          />
          <g>
            <ellipse cx={1350} cy={520} rx={62} ry={74} fill="#05050699" />
            <path d="M 1240 1080 L 1252 660 Q 1350 596 1448 660 L 1460 1080 Z" fill="#050506CC" />
            {/* the one cue that this is not a person */}
            <circle cx={1350} cy={512} r={9} fill={T.cold} />
          </g>
        </svg>
      </AbsoluteFill>

      <AbsoluteFill style={{padding: 110, justifyContent: 'center'}}>
        <div style={{maxWidth: 1000}}>
          <div
            style={{
              fontSize: 40,
              letterSpacing: '0.3em',
              color: T.cold,
              fontWeight: 700,
              marginBottom: 30,
            }}
          >
            AI
          </div>
          <div
            style={{
              fontSize: 170,
              fontWeight: 800,
              color: T.ink,
              lineHeight: 1.1,
              letterSpacing: '-0.045em',
              textShadow: '0 6px 44px rgba(0,0,0,0.9)',
            }}
          >
            저도 믿는데요?
          </div>
          <div
            style={{
              marginTop: 40,
              fontSize: 58,
              fontWeight: 700,
              color: T.warm,
              letterSpacing: '-0.02em',
            }}
          >
            세례를 줘도 될까?
          </div>
        </div>
      </AbsoluteFill>

      <Vignette strength={0.5} />
      <Grain opacity={0.045} />
    </AbsoluteFill>
  );
};
