import React from "react";
import { useCurrentFrame } from "remotion";
import { theme } from "../theme";

const C = theme.colors;
const O = C.outline;

/** 숲 줄 (씬 뒤 배경). */
export const ForestRow: React.FC<{ y: number; seed?: number; scale?: number;
  color?: string }> = ({ y, seed = 1, scale = 1, color = "#22301f" }) => {
  const trees = [];
  let x = -60, s = seed;
  const rnd = () => { s = (s * 9301 + 49297) % 233280; return s / 233280; };
  while (x < 1140) {
    const h = (280 + rnd() * 240) * scale, w = (110 + rnd() * 80) * scale;
    trees.push(
      <g key={x}>
        {[0, 1, 2].map((k) => (
          <polygon key={k}
            points={`${x},${y - h * (0.58 - 0.2 * k)} ${x + w / 2},${y - h * (1 - 0.22 * k)} ${x + w},${y - h * (0.58 - 0.2 * k)}`}
            fill={shadeHex(color, 1 - 0.08 * k)} stroke={O} strokeWidth={5} />
        ))}
        <rect x={x + w / 2 - 12} y={y - 34} width={24} height={34} fill="#32281e" stroke={O} strokeWidth={4} />
      </g>);
    x += w * 0.82;
  }
  return <g>{trees}</g>;
};

/** 건물 스카이라인. */
export const Skyline: React.FC<{ y: number; seed?: number; minY?: number }> =
({ y, seed = 3, minY = 560 }) => {
  const out = [];
  let x = -40, s = seed;
  const rnd = () => { s = (s * 9301 + 49297) % 233280; return s / 233280; };
  while (x < 1120) {
    const w = 130 + rnd() * 150;
    const top = minY + rnd() * Math.max(60, y - 300 - minY);
    const col = `rgb(${38 + rnd() * 14 | 0},${44 + rnd() * 12 | 0},${58 + rnd() * 10 | 0})`;
    const wins = [];
    for (let wy = top + 46; wy < y - 66; wy += 84) {
      for (let wx = x + 26; wx < x + w - 48; wx += 62) {
        wins.push(<rect key={`${wx}-${wy}`} x={wx} y={wy} width={32} height={40}
          fill={rnd() > 0.42 ? "#3b392f" : "#6e6848"} />);
      }
    }
    out.push(
      <g key={x}>
        <rect x={x} y={top} width={w} height={y - top} fill={col} stroke={O} strokeWidth={6} />
        <rect x={x} y={top} width={w} height={20} fill={shadeHex(col, 0.7)} stroke={O} strokeWidth={4} />
        {wins}
      </g>);
    x += w - 14;
  }
  return <g>{out}</g>;
};

/** 열차 — drive>0이면 오른쪽으로 주행(px/frame), 바퀴 회전. */
export const Train: React.FC<{ x: number; y: number; scale?: number; cars?: number;
  drive?: number; roll?: number; accent?: string }> = ({ x, y, scale = 1, cars = 2,
  drive = 0, roll, accent = C.amber }) => {
  const frame = useCurrentFrame();
  const dx = drive * frame;
  const wheelR = frame * (roll ?? drive * 2.2);
  const CW = 330, CH = 158;
  const wheel = (wx: number) => (
    <g key={wx} transform={`rotate(${wheelR} ${wx} ${y - 26})`}>
      <circle cx={wx} cy={y - 26} r={27} fill="#2a2a2e" stroke={O} strokeWidth={6} />
      <line x1={wx - 16} y1={y - 26} x2={wx + 16} y2={y - 26} stroke="#6a6a72" strokeWidth={5} />
    </g>
  );
  const body: React.ReactNode[] = [];
  for (let k = 0; k < cars; k++) {
    const cx0 = x - CW * 1.08 - k * (CW + 18);
    body.push(
      <g key={k}>
        <rect x={cx0 - CW} y={y - CH} width={CW} height={CH - 14} rx={18}
          fill="#464c5e" stroke={O} strokeWidth={7} />
        {[0.22, 0.5, 0.78].map((f) => (
          <rect key={f} x={cx0 - CW + CW * f - 32} y={y - CH + 26} width={64} height={52}
            rx={8} fill="#b9bdb0" stroke={O} strokeWidth={5} />
        ))}
        {wheel(cx0 - CW + 70)}{wheel(cx0 - 70)}
      </g>);
  }
  return (
    <g transform={`translate(${dx},0) scale(${scale})`} style={{ transformOrigin: `${x}px ${y}px` }}>
      {body}
      <path d={`M ${x - CW} ${y - 14} L ${x - CW} ${y - CH * 1.06} L ${x - 88} ${y - CH * 1.06}
               L ${x} ${y - CH * 0.6} L ${x} ${y - 14} Z`}
        fill={accent} stroke={O} strokeWidth={7} />
      <rect x={x - CW * 0.94} y={y - CH * 0.98} width={CW * 0.34} height={CH * 0.42} rx={8}
        fill="#b9bdb0" stroke={O} strokeWidth={5} />
      <circle cx={x - 20} cy={y - CH * 0.42} r={13} fill="#ffe8a0" stroke={O} strokeWidth={4} />
      <rect x={x - CW * 0.52} y={y - CH * 1.3} width={44} height={40} fill="#454a54" stroke={O} strokeWidth={5} />
      {wheel(x - CW * 0.72)}{wheel(x - CW * 0.24)}
    </g>
  );
};

/** 철로. */
export const Rail: React.FC<{ x0: number; x1: number; y: number }> = ({ x0, x1, y }) => (
  <g>
    {Array.from({ length: Math.ceil((x1 - x0) / 64) }).map((_, i) => (
      <rect key={i} x={x0 + i * 64} y={y + 6} width={14} height={22} fill="#5e5030" />
    ))}
    <rect x={x0} y={y} width={x1 - x0} height={10} fill="#786848" />
  </g>
);

/** 트러스 철교. */
export const Bridge: React.FC<{ x0: number; x1: number; y: number }> = ({ x0, x1, y }) => {
  const n = Math.max(3, Math.round((x1 - x0) / 180));
  const step = (x1 - x0) / n;
  const el = [];
  for (let k = 0; k < n; k++) {
    const ax = x0 + k * step;
    el.push(<polyline key={k} points={`${ax},${y} ${ax + step / 2},${y - 110} ${ax + step},${y}`}
      fill="none" stroke="#57503f" strokeWidth={13} strokeLinejoin="round" />);
  }
  return (
    <g>
      <line x1={x0} y1={y - 110} x2={x1} y2={y - 110} stroke="#57503f" strokeWidth={11} />
      {el}
      <rect x={x0} y={y} width={x1 - x0} height={24} fill="#57503f" stroke={O} strokeWidth={6} />
      {Array.from({ length: n + 1 }).map((_, k) => (
        <rect key={k} x={x0 + k * step - 9} y={y + 24} width={18} height={70} fill="#4a4436" stroke={O} strokeWidth={4} />
      ))}
    </g>
  );
};

/** 강 물결. */
export const River: React.FC<{ y0: number; y1: number }> = ({ y0, y1 }) => {
  const frame = useCurrentFrame();
  return (
    <g>
      <rect x={0} y={y0} width={1080} height={y1 - y0} fill="#26354a" />
      {[0, 1, 2, 3, 4].map((k) => {
        const wy = y0 + 34 + k * 46 + (k % 2) * 12;
        const dx = Math.sin(frame / 30 + k) * 14;
        return <path key={k}
          d={`M ${60 + k * 200 + dx} ${wy} q 40 -16 80 0 q 40 16 80 0`}
          stroke="#41546c" strokeWidth={7} fill="none" strokeLinecap="round" />;
      })}
    </g>
  );
};

/** 화물선. */
export const Ship: React.FC<{ x: number; y: number; scale?: number }> = ({ x, y, scale = 1 }) => {
  const frame = useCurrentFrame();
  const bob = Math.sin(frame / 34) * 4;
  return (
    <g transform={`translate(${x},${y + bob}) scale(${scale})`}>
      <path d="M -300 -80 L 300 -80 L 246 36 L -246 36 Z" fill="#3e4454" stroke={O} strokeWidth={7} />
      <rect x={82} y={-178} width={126} height={98} fill="#596070" stroke={O} strokeWidth={6} />
      <rect x={118} y={-232} width={54} height={54} fill="#596070" stroke={O} strokeWidth={5} />
      {[-1, 0, 1].map((k) => (
        <rect key={k} x={-258 + (k + 1) * 118} y={-134} width={100} height={54}
          fill={["#78602c", "#5b6878", "#8c4634"][k + 1]} stroke={O} strokeWidth={5} />
      ))}
    </g>
  );
};

/** 항만 크레인. */
export const Crane: React.FC<{ x: number; y: number; dir?: 1 | -1; scale?: number }> =
({ x, y, dir = 1, scale = 1 }) => (
  <g transform={`translate(${x},${y}) scale(${scale})`}>
    <line x1={-58} y1={0} x2={-34} y2={-470} stroke={O} strokeWidth={26} />
    <line x1={58} y1={0} x2={34} y2={-470} stroke={O} strokeWidth={26} />
    <line x1={-58} y1={0} x2={-34} y2={-470} stroke="#6c7080" strokeWidth={16} />
    <line x1={58} y1={0} x2={34} y2={-470} stroke="#6c7080" strokeWidth={16} />
    <line x1={dir * -140} y1={-436} x2={dir * 316} y2={-490} stroke={O} strokeWidth={24} />
    <line x1={dir * -140} y1={-436} x2={dir * 316} y2={-490} stroke="#6c7080" strokeWidth={14} />
    <line x1={dir * 236} y1={-478} x2={dir * 236} y2={-290} stroke="#6c7080" strokeWidth={8} />
    <rect x={dir * 236 - 50} y={-290} width={100} height={66} rx={7} fill="#78602c" stroke={O} strokeWidth={6} />
  </g>
);

export const Containers: React.FC<{ x: number; y: number }> = ({ x, y }) => (
  <g>
    {[["#78602c", 0], ["#5b6878", 1], ["#8c4634", 2]].map(([c, i]) => (
      <rect key={i as number} x={x + (i as number) * 180} y={y - 78} width={164} height={78}
        rx={6} fill={c as string} stroke={O} strokeWidth={6} />
    ))}
    <rect x={x + 92} y={y - 152} width={164} height={70} rx={6} fill="#64543c" stroke={O} strokeWidth={6} />
  </g>
);

/** 펄럭이는 깃발. */
export const Flag: React.FC<{ x: number; y: number; w: number; color: string;
  h?: number }> = ({ x, y, w, color, h = 560 }) => {
  const frame = useCurrentFrame();
  const wv = Math.sin(frame / 9) * 8;
  const hh = Math.abs(w) * 0.6;
  return (
    <g>
      <line x1={x} y1={y} x2={x} y2={y - h} stroke="#787064" strokeWidth={12} />
      <circle cx={x} cy={y - h - 6} r={10} fill="#b4aa8c" />
      <path d={`M ${x} ${y - h + 8}
               Q ${x + w * 0.5} ${y - h + 8 + wv} ${x + w} ${y - h + 14 + wv * 0.6}
               L ${x + w} ${y - h + 14 + hh * 0.86 + wv * 0.6}
               Q ${x + w * 0.5} ${y - h + hh + wv} ${x} ${y - h + 8 + hh} Z`}
        fill={color} stroke={O} strokeWidth={6} />
    </g>
  );
};

/** 피켓. */
export const Picket: React.FC<{ x: number; top: number; w: number; h: number;
  poleTo: number; children?: React.ReactNode }> = ({ x, top, w, h, poleTo, children }) => {
  const frame = useCurrentFrame();
  const sway = Math.sin(frame / 18) * 1.6;
  return (
    <g transform={`rotate(${sway} ${x} ${poleTo})`}>
      <line x1={x} y1={top + h} x2={x} y2={poleTo} stroke="#6e6250" strokeWidth={14} />
      <rect x={x - w / 2} y={top} width={w} height={h} rx={14}
        fill="#e8e2d4" stroke={O} strokeWidth={8} />
      {children}
    </g>
  );
};

/** 연기 퍼프 (기관차/공장). */
export const Smoke: React.FC<{ x: number; y: number; scale?: number }> = ({ x, y, scale = 1 }) => {
  const frame = useCurrentFrame();
  return (
    <g>
      {[0, 1, 2, 3].map((k) => {
        const p = ((frame / 34 + k * 0.25) % 1);
        const sy = y - p * 210 * scale, sx = x + Math.sin(p * 5 + k) * 20 + p * 46;
        const r = (26 + p * 42) * scale;
        return <circle key={k} cx={sx} cy={sy} r={r} fill="#5a5e6c"
          opacity={0.55 * (1 - p)} />;
      })}
    </g>
  );
};

function shadeHex(hex: string, f: number): string {
  const n = parseInt(hex.slice(1), 16);
  return `rgb(${Math.round(((n >> 16) & 255) * f)},${Math.round(((n >> 8) & 255) * f)},${Math.round((n & 255) * f)})`;
}
