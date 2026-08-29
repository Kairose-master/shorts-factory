import React from "react";
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { theme } from "../theme";
import { BgMesh, Camera } from "../kit/layers";
import { Entrance } from "../kit/ui";
import { ForestRow } from "../kit/props";

const C = theme.colors;
export const W = 1080, H = 1920;
export const GROUND = "#2c2a2c";

/** SVG 씬 캔버스 + 지면. */
export const Scene: React.FC<{ ground?: number; groundCol?: string;
  children: React.ReactNode }> = ({ ground, groundCol = GROUND, children }) => (
  <svg width={W} height={H} viewBox={`0 0 ${W} ${H}`} style={{ position: "absolute", inset: 0 }}>
    {ground !== undefined && (
      <>
        <rect x={0} y={ground} width={W} height={H - ground} fill={groundCol} />
        <rect x={0} y={ground - 6} width={W} height={14} fill="#3f434f" />
      </>
    )}
    {children}
  </svg>
);

export const Serif: React.FC<{ x: number; y: number; size: number; color?: string;
  children: React.ReactNode }> = ({ x, y, size, color = C.paper, children }) => (
  <text x={x} y={y} textAnchor="middle" fontFamily={theme.font.serif} fontSize={size}
    fill={color} stroke="#000" strokeWidth={size * 0.09} paintOrder="stroke">{children}</text>
);

export const Sans: React.FC<{ x: number; y: number; size: number; color?: string;
  anchor?: string; children: React.ReactNode }> = ({ x, y, size, color = C.paper,
  anchor = "middle", children }) => (
  <text x={x} y={y} textAnchor={anchor as never} fontFamily={theme.font.sans} fontSize={size}
    fill={color} stroke="#000" strokeWidth={size * 0.11} paintOrder="stroke">{children}</text>
);

/** HTML 타이포 블록 (Entrance 래핑). */
export const Typo: React.FC<{ top: number; size: number; color?: string; delay?: number;
  serif?: boolean; children: React.ReactNode }> = ({ top, size, color = C.paper,
  delay = 3, serif = true, children }) => (
  <Entrance delay={delay} style={{ position: "absolute", top, width: "100%", textAlign: "center" }}>
    <span style={{ fontFamily: serif ? theme.font.serif : theme.font.sans, fontSize: size,
      color, textShadow: "0 6px 26px #000" }}>{children}</span>
  </Entrance>
);

/** 시리즈 앵커: 1946 갈림길 — 전 EP 공유, 동일 코드. */
export const Anchor1946: React.FC<{ dur: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const grow = spring({ frame: frame - 6, fps, config: theme.spring.heavy });
  const jx = 540, jy = 1330;
  const bx = interpolate(grow, [0, 1], [0, 300]);
  const by = interpolate(grow, [0, 1], [0, 330]);
  return (
    <AbsoluteFill>
      <BgMesh tint={C.steel} tint2={C.amber} />
      <Camera dur={dur} zoom={1.06}>
        <Scene ground={1010} groundCol="#292628">
          <ForestRow y={1010} seed={46} color="#1f2c20" />
          {Array.from({ length: 8 }).map((_, i) => {
            const t = i / 7;
            return <rect key={i} x={jx - 84 + 30 * t} y={1740 - (1740 - jy) * t}
              width={168 - 60 * t} height={13} fill="#5e5030" />;
          })}
          <line x1={jx} y1={1740} x2={jx} y2={jy} stroke={C.outline} strokeWidth={26} />
          <line x1={jx} y1={1740} x2={jx} y2={jy} stroke="#787c8a" strokeWidth={15} />
          <line x1={jx} y1={jy} x2={jx - bx} y2={jy - by * 0.82} stroke={C.outline} strokeWidth={20} />
          <line x1={jx} y1={jy} x2={jx - bx} y2={jy - by * 0.82} stroke="#4c505e" strokeWidth={11} />
          <line x1={jx} y1={jy} x2={jx + bx} y2={jy - by * 0.82} stroke={C.outline} strokeWidth={24} />
          <line x1={jx} y1={jy} x2={jx + bx} y2={jy - by * 0.82} stroke={C.amber} strokeWidth={14} />
          <circle cx={jx} cy={jy} r={26} fill={C.paper} stroke={C.outline} strokeWidth={8} />
          {grow > 0.75 && (
            <>
              <Sans x={205} y={1090} size={46} color="#7c8090">공산당</Sans>
              <Sans x={880} y={1058} size={54} color={C.amber}>국민당 승리</Sans>
            </>
          )}
        </Scene>
      </Camera>
      <Typo top={560} size={175} delay={2}>1946</Typo>
    </AbsoluteFill>
  );
};
