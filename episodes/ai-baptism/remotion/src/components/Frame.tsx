import React from 'react';
import {AbsoluteFill} from 'remotion';
import {loadFonts, T} from '../theme';

/** Every scene sits on this. Background, safe area, and nothing else. */
export const Frame: React.FC<{
  children: React.ReactNode;
  bg?: string;
  style?: React.CSSProperties;
}> = ({children, bg = T.bg, style}) => {
  // Called here rather than only in Episode: each scene is also its own
  // composition, and a standalone scene render must still have the font.
  loadFonts();
  return (
  <AbsoluteFill
    style={{
      backgroundColor: bg,
      fontFamily: T.font,
      color: T.ink,
      ...style,
    }}
  >
    {children}
  </AbsoluteFill>
  );
};

/** Content inset to the 96px safe margin the brief specifies. */
export const Safe: React.FC<{
  children: React.ReactNode;
  style?: React.CSSProperties;
}> = ({children, style}) => (
  <AbsoluteFill
    style={{
      padding: T.safe,
      display: 'flex',
      flexDirection: 'column',
      ...style,
    }}
  >
    {children}
  </AbsoluteFill>
);

/**
 * A slow vertical vignette. Present in every scene at low strength so cuts
 * between scenes never feel like cuts between different films.
 */
export const Vignette: React.FC<{strength?: number}> = ({strength = 0.55}) => (
  <AbsoluteFill
    style={{
      background: `radial-gradient(ellipse 78% 68% at 50% 46%, rgba(0,0,0,0) 0%, rgba(0,0,0,${strength}) 100%)`,
      pointerEvents: 'none',
    }}
  />
);

/** Faint film grain. Kills the flat-vector look that reads as "AI made this". */
export const Grain: React.FC<{opacity?: number}> = ({opacity = 0.05}) => (
  <AbsoluteFill
    style={{
      opacity,
      pointerEvents: 'none',
      mixBlendMode: 'overlay',
      backgroundImage:
        "url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='180' height='180'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='3'/%3E%3C/filter%3E%3Crect width='180' height='180' filter='url(%23n)'/%3E%3C/svg%3E\")",
      backgroundSize: '180px 180px',
    }}
  />
);
