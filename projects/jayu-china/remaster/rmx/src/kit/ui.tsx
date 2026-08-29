import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { theme } from "../theme";

/** 프리미엄 입장 — opacity+rise+scale 동시. */
export const Entrance: React.FC<{ delay?: number; from?: number; children: React.ReactNode;
  style?: React.CSSProperties }> = ({ delay = 0, from = 40, children, style }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const p = spring({ frame: frame - delay, fps, config: theme.spring.smooth });
  return (
    <div style={{ opacity: p,
      transform: `translateY(${interpolate(p, [0, 1], [from, 0])}px) scale(${interpolate(p, [0, 1], [0.94, 1])})`,
      ...style }}>{children}</div>
  );
};

/** 단어 단위 리빌. */
export const WordReveal: React.FC<{ text: string; delay?: number; per?: number;
  style?: React.CSSProperties }> = ({ text, delay = 0, per = 3, style }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return (
    <div style={{ display: "flex", flexWrap: "wrap", justifyContent: "center",
      columnGap: "0.26em", ...style }}>
      {text.split(" ").map((word, i) => {
        const p = spring({ frame: frame - delay - i * per, fps, config: theme.spring.snappy });
        return (
          <span key={i} style={{ display: "inline-block", opacity: p,
            transform: `translateY(${interpolate(p, [0, 1], [30, 0])}px)` }}>{word}</span>
        );
      })}
    </div>
  );
};

/** 상단 타이틀 밴드 — 채널 문법 유지(검정 밴드, 흰 줄+노랑 줄, 세계관 라벨). */
export const TitleBand: React.FC<{ l1: string; l2: string; tag: string; world: string;
  intro?: boolean }> = ({ l1, l2, tag, world, intro }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = intro ? frame : 999;
  const bh = interpolate(t, [0, 12], [0, 420], { easing: theme.ease.out,
    extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const p1 = spring({ frame: t - 3, fps, config: theme.spring.smooth });
  const p2 = spring({ frame: t - 8, fps, config: theme.spring.smooth });
  return (
    <div style={{ position: "absolute", top: 0, left: 0, right: 0, height: bh,
      background: "#0a0a0a", overflow: "hidden", zIndex: 40 }}>
      <div style={{ position: "absolute", top: 88, width: "100%", textAlign: "center",
        fontFamily: theme.font.sans, fontSize: 92, color: "#fff",
        WebkitTextStroke: "0px", opacity: p1,
        transform: `translateY(${interpolate(p1, [0, 1], [-40, 0])}px)` }}>{l1}</div>
      <div style={{ position: "absolute", top: 208, width: "100%", textAlign: "center",
        fontFamily: theme.font.sans, fontSize: 104, color: theme.colors.yellow,
        opacity: p2, transform: `translateY(${interpolate(p2, [0, 1], [-40, 0])}px)` }}>{l2}</div>
      <div style={{ position: "absolute", top: 358, right: 40, fontFamily: theme.font.sans,
        fontSize: 34, color: "#c8c8c8" }}>{tag}</div>
      <div style={{ position: "absolute", top: 360, left: 40, fontFamily: theme.font.sans,
        fontSize: 30, color: "#dec684" }}>{world}</div>
    </div>
  );
};

/** 자막 칩 — WordBoundary 실측 타이밍으로 Sequence에 얹는다. */
export const Chip: React.FC<{ text: string }> = ({ text }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const p = spring({ frame, fps, config: theme.spring.bouncy });
  const fs = text.length > 16 ? 50 : 58;
  return (
    <div style={{ position: "absolute", left: 0, right: 0, top: 1430, zIndex: 30,
      display: "flex", justifyContent: "center",
      opacity: Math.min(1, frame / 4),
      transform: `translateY(${interpolate(p, [0, 1], [30, 0])}px) scale(${interpolate(p, [0, 1], [0.88, 1])})` }}>
      <div style={{ background: "rgba(0,0,0,0.84)", borderRadius: 16,
        padding: "18px 36px", fontFamily: theme.font.sans, fontSize: fs,
        color: theme.colors.yellow, maxWidth: 920, textAlign: "center" }}>{text}</div>
    </div>
  );
};

/** 도장 쾅 — 회전 스탬프 (오버슛 + 착지 더스트 링). */
export const Stamp: React.FC<{ text: string; delay?: number; color?: string;
  size?: number; rotate?: number; textColor?: string; style?: React.CSSProperties }> =
({ text, delay = 0, color = theme.colors.red, size = 300, rotate = -7,
   textColor, style }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const p = spring({ frame: frame - delay, fps, config: { damping: 14, stiffness: 300 } });
  const ring = interpolate(frame - delay, [2, 14], [0, 1],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: theme.ease.out });
  const fs = size * (text.length > 2 ? 0.30 : 0.42);
  return (
    <div style={{ position: "relative", width: size, height: size * 0.62,
      transform: `rotate(${rotate}deg) scale(${interpolate(p, [0, 1], [2.1, 1])})`,
      opacity: p, ...style }}>
      <div style={{ position: "absolute", inset: 0, border: `${size * 0.045}px solid ${color}`,
        display: "flex", alignItems: "center", justifyContent: "center",
        fontFamily: theme.font.serif, fontSize: fs, color: textColor ?? color,
        textShadow: "0 4px 18px rgba(0,0,0,0.45)" }}>{text}</div>
      {ring > 0 && ring < 1 && (
        <div style={{ position: "absolute", inset: -size * 0.16 * ring,
          border: `3px solid ${color}`, opacity: 1 - ring, borderRadius: 12 }} />
      )}
    </div>
  );
};

/** 정보 카드 (유리질감). */
export const Card: React.FC<{ w?: number; outline?: string; children: React.ReactNode;
  style?: React.CSSProperties }> = ({ w, outline = "#5a6072", children, style }) => (
  <div style={{ width: w, background: "rgba(24,28,40,0.88)",
    border: `6px solid ${outline}`, borderRadius: 24,
    boxShadow: "0 24px 60px -18px rgba(0,0,0,0.65)",
    padding: "26px 40px", fontFamily: theme.font.sans, color: theme.colors.paper,
    textAlign: "center", ...style }}>{children}</div>
);

/** 상시 미세 호흡. */
export const Breathe: React.FC<{ amp?: number; children: React.ReactNode;
  style?: React.CSSProperties }> = ({ amp = 1, children, style }) => {
  const frame = useCurrentFrame();
  return <div style={{ transform:
    `translateY(${Math.sin(frame / 26) * 3 * amp}px) scale(${1 + Math.sin(frame / 30) * 0.008 * amp})`,
    ...style }}>{children}</div>;
};
