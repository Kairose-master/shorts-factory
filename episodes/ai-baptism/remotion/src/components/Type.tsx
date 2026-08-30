import React from 'react';
import {AbsoluteFill} from 'remotion';
import {T} from '../theme';

/** The episode's large statement type. Used only for load-bearing lines. */
export const Statement: React.FC<{
  children: React.ReactNode;
  size?: number;
  color?: string;
  weight?: number;
  style?: React.CSSProperties;
}> = ({children, size = 92, color = T.ink, weight = 800, style}) => (
  <div
    style={{
      fontSize: size,
      fontWeight: weight,
      color,
      letterSpacing: '-0.03em',
      lineHeight: 1.24,
      textAlign: 'center',
      whiteSpace: 'pre-line',
      ...style,
    }}
  >
    {children}
  </div>
);

/** Cold monospace, for anything that is a machine reading a human. */
export const Readout: React.FC<{
  children: React.ReactNode;
  size?: number;
  color?: string;
  style?: React.CSSProperties;
}> = ({children, size = 30, color = T.cold, style}) => (
  <div
    style={{
      fontFamily: T.mono,
      fontSize: size,
      color,
      letterSpacing: '0.14em',
      whiteSpace: 'pre-line',
      ...style,
    }}
  >
    {children}
  </div>
);

/**
 * The persistent theology marker. RT-01 and RT-03 both require a label that
 * *holds* rather than flashes, because a flashed disclaimer is a deniable one.
 * Low third, small, always legible, never animated after entry.
 */
export const TheologyMarker: React.FC<{text: string; opacity?: number}> = ({
  text,
  opacity = 1,
}) => (
  <AbsoluteFill
    style={{
      justifyContent: 'flex-end',
      alignItems: 'center',
      paddingBottom: 44,
      pointerEvents: 'none',
    }}
  >
    <div
      style={{
        opacity,
        fontSize: 26,
        fontWeight: 500,
        letterSpacing: '0.04em',
        color: T.ink,
        border: `1.5px solid ${T.warmSoft}`,
        borderRadius: 4,
        padding: '10px 26px',
        background: 'rgba(14,12,8,0.92)',
        textShadow: '0 1px 10px rgba(0,0,0,0.9)',
      }}
    >
      {text}
    </div>
  </AbsoluteFill>
);

/** Scene-corner label, e.g. 사고실험. Sits top-left, out of the caption zone. */
export const CornerMarker: React.FC<{text: string; opacity?: number}> = ({
  text,
  opacity = 1,
}) => (
  <div
    style={{
      position: 'absolute',
      top: T.safe,
      left: T.safe,
      opacity: opacity * 0.7,
      fontFamily: T.mono,
      fontSize: 19,
      letterSpacing: '0.34em',
      color: T.inkDim,
    }}
  >
    {text}
  </div>
);
