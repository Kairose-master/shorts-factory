import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { theme } from "../theme";

const C = theme.colors;

/**
 * 해압축 상자 — 시즌2 「자유중국의 철학」 연출 시그니처.
 * 정본(philosophy-series-bible-v1.txt): "label 상자가 열리며 incident들이 나오는" 애니메이션.
 * 하나의 라벨(예: 마르크스主義)이 사실은 여러 사건의 압축임을 시각으로 보인다.
 *
 * open=false면 상자가 잠긴 채 굳어 있다(=이긴 이념), true면 뚜껑이 열리고
 * incident 칩들이 스태거로 튀어나온다(=진 이념).
 */
export const DecompressBox: React.FC<{
  label: string; incidents: string[]; x: number; y: number;
  delay?: number; open?: boolean; w?: number; color?: string;
}> = ({ label, incidents, x, y, delay = 0, open = true, w = 340,
  color = C.amber }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const box = spring({ frame: frame - delay, fps, config: theme.spring.smooth });
  const lid = open
    ? spring({ frame: frame - delay - 10, fps, config: theme.spring.bouncy })
    : 0;
  const h = 150;
  return (
    <g opacity={box} transform={`translate(${x}, ${y})`}>
      {/* 튀어나오는 incident 칩 */}
      {open && incidents.map((t, i) => {
        const p = spring({ frame: frame - delay - 16 - i * 5, fps,
          config: { damping: 13, stiffness: 170 } });
        const a = -Math.PI / 2 + (i - (incidents.length - 1) / 2) * 0.74;
        const r = interpolate(p, [0, 1], [0, 330]);
        const cx = Math.cos(a) * r * 1.02, cy = Math.sin(a) * r - 60;
        const tw = t.length * 30 + 56;
        return (
          <g key={t} opacity={p}
            transform={`translate(${cx}, ${cy}) scale(${interpolate(p, [0, 1], [0.5, 1])})`}>
            <rect x={-tw / 2} y={-36} width={tw} height={72} rx={16}
              fill="rgba(24,28,40,0.95)" stroke={color} strokeWidth={5} />
            <text x={0} y={14} textAnchor="middle" fontFamily={theme.font.sans}
              fontSize={38} fill={C.paper}>{t}</text>
          </g>
        );
      })}
      {/* 뚜껑 */}
      <g transform={`translate(0, ${-h / 2 - interpolate(lid, [0, 1], [0, 54])})
                     rotate(${interpolate(lid, [0, 1], [0, -14])})`}>
        <rect x={-w / 2 - 14} y={-26} width={w + 28} height={30} rx={8}
          fill={open ? "#4a4436" : "#3a3630"} stroke={C.outline} strokeWidth={7} />
      </g>
      {/* 몸통 */}
      <rect x={-w / 2} y={-h / 2} width={w} height={h} rx={14}
        fill="rgba(24,28,40,0.94)" stroke={open ? color : "#5a6072"} strokeWidth={7} />
      <text x={0} y={12} textAnchor="middle" fontFamily={theme.font.serif}
        fontSize={52} fill={open ? color : "#7c8090"}>{label}</text>
      {/* 잠금(=굳음) 표시 */}
      {!open && (
        <g>
          <rect x={-34} y={h / 2 - 22} width={68} height={56} rx={10}
            fill="#5a6072" stroke={C.outline} strokeWidth={5} />
          <path d={`M -19 ${h / 2 - 22} a 19 19 0 0 1 38 0`} fill="none"
            stroke="#5a6072" strokeWidth={10} />
        </g>
      )}
    </g>
  );
};
