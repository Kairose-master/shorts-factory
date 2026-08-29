import React from "react";
import { AbsoluteFill, useCurrentFrame, staticFile } from "remotion";
import { theme } from "../theme";

/** 폰트 로드 (전 컴포지션 공용). */
export const Fonts: React.FC = () => (
  <style>{`
    @font-face { font-family: NotoSerifKR; src: url('${staticFile("fonts/NotoSerifKR-Black.ttf")}'); }
    @font-face { font-family: NotoSansKR; src: url('${staticFile("fonts/NotoSansKR-Bold.ttf")}'); }
  `}</style>
);

/** 배경 메시 — 절대 플랫 단색 금지. tint로 씬별 무드 변주. */
export const BgMesh: React.FC<{ tint?: string; tint2?: string }> = ({
  tint = theme.colors.amber, tint2 = theme.colors.steel }) => {
  const frame = useCurrentFrame();
  const d1 = Math.sin(frame / 55) * 50;
  const d2 = Math.cos(frame / 70) * 40;
  return (
    <AbsoluteFill style={{ background: `linear-gradient(180deg, ${theme.colors.bg} 0%, ${theme.colors.bg2} 100%)` }}>
      <div style={{ position: "absolute", width: 1300, height: 1300, borderRadius: "50%",
        top: -420, left: -340 + d1, filter: "blur(60px)",
        background: `radial-gradient(circle, ${tint}2e, transparent 62%)` }} />
      <div style={{ position: "absolute", width: 1000, height: 1000, borderRadius: "50%",
        bottom: -380, right: -280 - d2, filter: "blur(80px)",
        background: `radial-gradient(circle, ${tint2}26, transparent 65%)` }} />
    </AbsoluteFill>
  );
};

export const Grade: React.FC = () => (
  <AbsoluteFill style={{ pointerEvents: "none" }}>
    <AbsoluteFill style={{ backgroundColor: theme.colors.amber, mixBlendMode: "soft-light", opacity: 0.14 }} />
    <AbsoluteFill style={{ background: "linear-gradient(180deg, rgba(0,0,0,0.12), transparent 26%, transparent 72%, rgba(0,0,0,0.24))" }} />
  </AbsoluteFill>
);

export const Grain: React.FC = () => {
  const frame = useCurrentFrame();
  const noise = `url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='220' height='220'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2'/%3E%3C/filter%3E%3Crect width='220' height='220' filter='url(%23n)' opacity='0.5'/%3E%3C/svg%3E")`;
  return <AbsoluteFill style={{ pointerEvents: "none", backgroundImage: noise,
    backgroundSize: "220px",
    backgroundPosition: `${(frame * 7) % 220}px ${(frame * 13) % 220}px`,
    opacity: 0.055, mixBlendMode: "overlay" }} />;
};

export const Vignette: React.FC = () => (
  <AbsoluteFill style={{ pointerEvents: "none",
    background: "radial-gradient(ellipse at center, transparent 55%, rgba(0,0,0,0.30) 100%)" }} />
);

/** 씬 카메라 — 느린 push-in/드리프트. */
export const Camera: React.FC<{ dur: number; zoom?: number; panX?: number;
  children: React.ReactNode }> = ({ dur, zoom = 1.05, panX = 0, children }) => {
  const frame = useCurrentFrame();
  const p = Math.min(1, frame / Math.max(dur, 1));
  const e = p * p * (3 - 2 * p);
  return (
    <AbsoluteFill style={{
      transform: `scale(${1 + (zoom - 1) * e}) translateX(${panX * e}px)` }}>
      {children}
    </AbsoluteFill>
  );
};
