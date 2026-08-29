import React from "react";
import { useCurrentFrame } from "remotion";
import { theme } from "../theme";

const C = theme.colors;
const OUTFITS: Record<string, string> = {
  suit: C.suitD, suit_b: C.suitB, suit_r: C.suitR, uniform: C.uniG,
  worker: C.workB, coat: C.coatG, student: "#3a3e4e",
};

export type Pose = "stand" | "point_r" | "point_l" | "hands_up" | "arms_cross"
  | "hold_case" | "reach_r" | "reach_l" | "hold_sign" | "wave";

/**
 * SD 캐릭터 (viewBox 0 0 240 350, 발끝 y=344).
 * height px로 스케일. 팔은 어깨 피벗 회전이라 pose 전환이 애니메이션 가능.
 */
export const Person: React.FC<{
  x: number; y: number; height?: number; outfit?: keyof typeof OUTFITS | string;
  expr?: "neutral" | "smug" | "worried" | "shout" | "surprised" | "smile" | "closed";
  hat?: "helmet" | "cap" | "none" | "hair";
  facing?: -1 | 0 | 1; pose?: Pose; tie?: string; waveArm?: boolean;
  label?: string; labelColor?: string;
}> = ({ x, y, height = 500, outfit = "suit", expr = "neutral", hat = "hair",
  facing = 0, pose = "stand", tie = "#983a2e", waveArm = false,
  label, labelColor = C.paper }) => {
  const frame = useCurrentFrame();
  const col = OUTFITS[outfit] ?? outfit;
  const leg = shade(col, 0.62);
  const s = height / 350;
  const breathe = Math.sin(frame / 24 + x * 0.01) * 1.6;
  const wob = waveArm ? Math.sin(frame / 5) * 14 : 0;

  // 팔 각도 (0=아래, 양수=몸 바깥쪽으로 올림; 회전은 어깨 기준)
  const arms: Record<string, [number, number, number, number]> = {
    // [왼팔 각도, 오른팔 각도, 왼팔 길이배수, 오른팔 길이배수]
    stand: [12, 12, 1, 1], wave: [12, 155 + wob, 1, 0.95],
    point_r: [12, 118, 1, 1.15], point_l: [118, 12, 1.15, 1],
    hands_up: [150, 150 + wob, 1, 1], arms_cross: [-58, -58, 0.82, 0.82],
    hold_case: [12, 28, 1, 1], reach_r: [12, 84, 1, 1.25], reach_l: [84, 12, 1.25, 1],
    hold_sign: [148, 148, 0.9, 0.9],
  };
  const [aL, aR, mL, mR] = arms[pose] ?? arms.stand;

  const fx = facing * 10; // 이목구비 시프트
  const eyeY = 76, eyeDX = 21, eyeR = 6.5;
  const mouth = () => {
    const mx = 120 + fx, my = 104;
    switch (expr) {
      case "smug": return <path d={`M ${mx - 15} ${my} Q ${mx + 2} ${my + 9} ${mx + 15} ${my - 6}`} stroke={C.outline} strokeWidth={5.5} fill="none" strokeLinecap="round" />;
      case "smile": return <path d={`M ${mx - 15} ${my - 2} Q ${mx} ${my + 11} ${mx + 15} ${my - 2}`} stroke={C.outline} strokeWidth={5.5} fill="none" strokeLinecap="round" />;
      case "worried": return <path d={`M ${mx - 13} ${my + 5} Q ${mx} ${my - 5} ${mx + 13} ${my + 5}`} stroke={C.outline} strokeWidth={5.5} fill="none" strokeLinecap="round" />;
      case "shout": return <ellipse cx={mx} cy={my + 2} rx={12} ry={14} fill="#4e2c28" stroke={C.outline} strokeWidth={4} />;
      case "surprised": return <ellipse cx={mx} cy={my + 2} rx={8} ry={9} fill="#4e2c28" stroke={C.outline} strokeWidth={4} />;
      default: return <line x1={120 + fx - 12} y1={my} x2={120 + fx + 12} y2={my} stroke={C.outline} strokeWidth={5.5} strokeLinecap="round" />;
    }
  };
  const eyes = expr === "closed"
    ? <>
        <path d={`M ${120 + fx - eyeDX - 9} ${eyeY} q 9 8 18 0`} stroke={C.outline} strokeWidth={5} fill="none" strokeLinecap="round" />
        <path d={`M ${120 + fx + eyeDX - 9} ${eyeY} q 9 8 18 0`} stroke={C.outline} strokeWidth={5} fill="none" strokeLinecap="round" />
      </>
    : <>
        <circle cx={120 + fx - eyeDX} cy={eyeY} r={eyeR} fill={C.outline} />
        <circle cx={120 + fx + eyeDX} cy={eyeY} r={eyeR} fill={C.outline} />
      </>;

  const armEl = (side: -1 | 1, ang: number, mult: number) => {
    const sx = 120 + side * 46, sy = 152;
    const len = 74 * mult;
    return (
      <g transform={`rotate(${-side * ang} ${sx} ${sy})`}>
        <line x1={sx} y1={sy} x2={sx} y2={sy + len} stroke={C.outline} strokeWidth={26} strokeLinecap="round" />
        <line x1={sx} y1={sy} x2={sx} y2={sy + len} stroke={col} strokeWidth={17} strokeLinecap="round" />
        <circle cx={sx} cy={sy + len} r={12} fill={C.skin} stroke={C.outline} strokeWidth={5} />
        {pose === "hold_case" && side === 1 && (
          <g>
            <rect x={sx - 26} y={sy + len + 10} width={52} height={40} rx={7}
              fill="#4c3c2a" stroke={C.outline} strokeWidth={5} />
            <rect x={sx - 8} y={sy + len + 4} width={16} height={10} rx={4}
              fill="none" stroke={C.outline} strokeWidth={5} />
          </g>
        )}
      </g>
    );
  };

  return (
    <g transform={`translate(${x - 120 * s}, ${y - 344 * s + breathe}) scale(${s})`}>
      {/* 그림자 */}
      <ellipse cx={120} cy={340} rx={78} ry={12} fill="rgba(0,0,0,0.35)" />
      {/* 다리/신발 */}
      <rect x={86} y={252} width={28} height={80} fill={leg} stroke={C.outline} strokeWidth={6} />
      <rect x={126} y={252} width={28} height={80} fill={leg} stroke={C.outline} strokeWidth={6} />
      <ellipse cx={98} cy={334} rx={26} ry={11} fill={C.outline} />
      <ellipse cx={142} cy={334} rx={26} ry={11} fill={C.outline} />
      {/* 팔 (몸통 뒤) */}
      {armEl(-1, aL, mL)}
      {armEl(1, aR, mR)}
      {/* 몸통 */}
      <rect x={72} y={140} width={96} height={126} rx={34} fill={col} stroke={C.outline} strokeWidth={7} />
      {(outfit === "suit" || outfit === "suit_b" || outfit === "suit_r" || outfit === "student") && (
        <>
          <path d="M 96 146 L 144 146 L 120 190 Z" fill={C.shirt} stroke={C.outline} strokeWidth={4} />
          <path d="M 112 150 L 128 150 L 120 196 Z" fill={tie} stroke={C.outline} strokeWidth={3} />
        </>
      )}
      {outfit === "uniform" && (
        <>
          <rect x={72} y={210} width={96} height={14} fill="#302c24" stroke={C.outline} strokeWidth={4} />
          {[0, 1, 2].map((k) => <circle key={k} cx={120} cy={160 + k * 20} r={4.5} fill="#d2be78" />)}
        </>
      )}
      {outfit === "worker" && (
        <rect x={72} y={196} width={96} height={12} fill="#3c3224" stroke={C.outline} strokeWidth={4} />
      )}
      {/* 얼굴 */}
      <circle cx={120} cy={84} r={58} fill={C.skin} stroke={C.outline} strokeWidth={7} />
      {eyes}{mouth()}
      {/* 머리 장식 */}
      {hat === "hair" && (
        <path d="M 63 78 A 57 57 0 0 1 177 78 L 172 62 Q 120 22 68 62 Z" fill={C.hair} />
      )}
      {hat === "hair" && (
        <path d="M 64 80 A 56 52 0 0 1 176 80 L 176 66 A 60 54 0 0 0 64 66 Z" fill={C.hair} />
      )}
      {hat === "helmet" && (
        <g>
          <path d="M 56 76 A 64 58 0 0 1 184 76 Z" fill="#4c5044" stroke={C.outline} strokeWidth={7} />
          <rect x={52} y={64} width={136} height={16} rx={8} fill="#4c5044" stroke={C.outline} strokeWidth={5} />
        </g>
      )}
      {hat === "cap" && (
        <g>
          <path d="M 60 72 A 60 54 0 0 1 180 72 Z" fill="#363a48" stroke={C.outline} strokeWidth={6} />
          <rect x={facing >= 0 ? 118 : 40} y={62} width={82} height={14} rx={7}
            fill="#363a48" stroke={C.outline} strokeWidth={5} />
        </g>
      )}
      {label && (
        <text x={120} y={396} textAnchor="middle" fontFamily={theme.font.sans}
          fontSize={40} fill={labelColor} stroke="#000" strokeWidth={7}
          paintOrder="stroke">{label}</text>
      )}
    </g>
  );
};

function shade(hex: string, f: number): string {
  const n = parseInt(hex.slice(1), 16);
  const r = Math.round(((n >> 16) & 255) * f), g = Math.round(((n >> 8) & 255) * f),
    b = Math.round((n & 255) * f);
  return `rgb(${r},${g},${b})`;
}
