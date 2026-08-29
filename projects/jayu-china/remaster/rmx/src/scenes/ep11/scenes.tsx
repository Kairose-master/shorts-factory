import React from "react";
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { theme } from "../../theme";
import { BgMesh, Camera } from "../../kit/layers";
import { Entrance, Card } from "../../kit/ui";
import { Person } from "../../kit/people";
import { Skyline } from "../../kit/props";
import { Anchor1946, Scene, Sans, Typo } from "../common";

const C = theme.colors;
const LBLUE = "#4a6a90";   // 현실 좌 코드
const RRED = "#8c4634";    // 현실 우 코드

/** 후보 카드 — 한 카드 안에 상반된 색의 공약 두 개. */
const Cand: React.FC<{ no: string; pledges: [string, string][]; delay: number;
  x: number; y: number }> = ({ no, pledges, delay, x, y }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const p = spring({ frame: frame - delay, fps, config: theme.spring.snappy });
  return (
    <g opacity={p} transform={`translate(${x}, ${y + interpolate(p, [0, 1], [30, 0])})`}>
      <rect x={-230} y={-110} width={460} height={230} rx={22} fill="rgba(24,28,40,0.92)"
        stroke="#5a6072" strokeWidth={7} />
      <circle cx={-170} cy={-52} r={38} fill={C.amber} stroke={C.outline} strokeWidth={6} />
      <text x={-170} y={-36} textAnchor="middle" fontFamily={theme.font.serif}
        fontSize={44} fill={C.ink}>{no}</text>
      {pledges.map(([t, col], i) => (
        <g key={t}>
          <rect x={-100} y={-88 + i * 88} width={300} height={70} rx={14}
            fill={col} stroke={C.outline} strokeWidth={5} />
          <text x={50} y={-42 + i * 88} textAnchor="middle" fontFamily={theme.font.sans}
            fontSize={36} fill="#f2e9dc">{t}</text>
        </g>
      ))}
    </g>
  );
};

/* s1 — WTF: 공약 3개 → 좌? 우? */
const S1: React.FC<{ dur: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const pills = ["복지 확대", "시장 개방", "군비 증강"];
  const cols = [LBLUE, RRED, RRED];
  const q = spring({ frame: frame - 34, fps, config: theme.spring.bouncy });
  return (
    <AbsoluteFill>
      <BgMesh tint={C.steel} tint2={C.red} />
      <Camera dur={dur} zoom={1.05}>
        <Scene ground={1450} groundCol="#26242a">
          <Skyline y={1450} seed={111} minY={1050} />
          <Person x={540} y={1480} height={420} outfit="suit_b" expr="neutral"
            pose="stand" tie="#3e5a78" facing={0} />
        </Scene>
      </Camera>
      <div style={{ position: "absolute", top: 545, left: 0, right: 0, display: "flex",
        flexDirection: "column", alignItems: "center", gap: 20 }}>
        {pills.map((t, i) => (
          <Entrance key={t} delay={3 + i * 7}>
            <div style={{ background: cols[i], border: `6px solid ${C.outline}`,
              borderRadius: 18, padding: "14px 44px", fontFamily: theme.font.sans,
              fontSize: 52, color: "#f2e9dc" }}>{t}</div>
          </Entrance>
        ))}
      </div>
      <div style={{ position: "absolute", top: 1050, width: "100%", textAlign: "center",
        opacity: q, transform: `scale(${interpolate(q, [0, 1], [0.7, 1])})` }}>
        <span style={{ fontFamily: theme.font.serif, fontSize: 120, color: C.yellow,
          textShadow: "0 6px 26px #000" }}>左? 右?</span>
      </div>
    </AbsoluteFill>
  );
};

/* s3 — 근거1: 후보 1·2 */
const S3: React.FC<{ dur: number }> = ({ dur }) => (
  <AbsoluteFill>
    <BgMesh tint={C.steel} />
    <Camera dur={dur} zoom={1.04}>
      <Scene ground={1620} groundCol="#26242a">
        <Skyline y={1620} seed={113} minY={1450} />
        <Cand no="1" delay={4} x={540} y={760}
          pledges={[["국영 철도 사수", LBLUE], ["무역 개방", RRED]]} />
        <Cand no="2" delay={22} x={540} y={1120}
          pledges={[["민영화 확대", RRED], ["외국 자본 규제", LBLUE]]} />
      </Scene>
    </Camera>
  </AbsoluteFill>
);

/* s4 — 미니 페이오프: 네 명 모두 반씩 걸친다 */
const S4: React.FC<{ dur: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const p = spring({ frame: frame - 14, fps, config: theme.spring.smooth });
  return (
    <AbsoluteFill>
      <BgMesh tint={C.amber} tint2={C.steel} />
      <Camera dur={dur} zoom={1.05}>
        <Scene ground={1560} groundCol="#26242a">
          {/* 좌→우 그라데이션 자 4개, 마커 전부 중앙 */}
          <defs>
            <linearGradient id="lr" x1="0" x2="1">
              <stop offset="0" stopColor={LBLUE} /><stop offset="1" stopColor={RRED} />
            </linearGradient>
          </defs>
          {[0, 1, 2, 3].map((k) => {
            const y = 900 + k * 130;
            return (
              <g key={k} opacity={p}>
                <rect x={160} y={y} width={760} height={34} rx={17} fill="url(#lr)"
                  stroke={C.outline} strokeWidth={5} />
                <circle cx={540 + (k % 2 ? 26 : -22)} cy={y + 17} r={26}
                  fill={C.paper} stroke={C.outline} strokeWidth={6} />
                <Sans x={110} y={y + 30} size={34} color="#9a9eaa">{k + 1}</Sans>
              </g>
            );
          })}
          <Sans x={210} y={860} size={36} color="#8fa8c4">左</Sans>
          <Sans x={880} y={860} size={36} color="#d2917c">右</Sans>
        </Scene>
      </Camera>
      <Typo top={545} size={78} delay={2}>벌써 헷갈리죠?</Typo>
      <Typo top={1460} size={62} color={C.yellow} delay={26}>네 명 모두 반씩 걸친다</Typo>
    </AbsoluteFill>
  );
};

/* s5 — 근거2: 후보 3·4 */
const S5: React.FC<{ dur: number }> = ({ dur }) => (
  <AbsoluteFill>
    <BgMesh tint={C.green} tint2={C.red} />
    <Camera dur={dur} zoom={1.04}>
      <Scene ground={1620} groundCol="#26242a">
        <Skyline y={1620} seed={115} minY={1450} />
        <Cand no="3" delay={4} x={540} y={760}
          pledges={[["복지 확대", LBLUE], ["군비 증강", RRED]]} />
        <Cand no="4" delay={22} x={540} y={1120}
          pledges={[["감세", RRED], ["재벌 해체", LBLUE]]} />
      </Scene>
    </Camera>
  </AbsoluteFill>
);

/* s6 — 근거3: 속임수가 아니라 자연스러운 동맹 (웹) */
const S6: React.FC<{ dur: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const draw = interpolate(frame, [8, 46], [0, 1],
    { easing: theme.ease.inOut, extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const nodes: [number, number, string][] = [[300, 900, "1"], [780, 900, "2"],
    [300, 1250, "3"], [780, 1250, "4"]];
  return (
    <AbsoluteFill>
      <BgMesh tint={C.amber} />
      <Camera dur={dur} zoom={1.05}>
        <Scene ground={1560} groundCol="#26242a">
          {nodes.map((a, i) => nodes.slice(i + 1).map((b, j) => (
            <line key={`${i}-${j}`} x1={a[0]} y1={a[1]} x2={b[0]} y2={b[1]}
              stroke={C.amber} strokeWidth={7} strokeDasharray={600}
              strokeDashoffset={600 * (1 - draw)} opacity={0.75} />
          )))}
          {nodes.map(([x, y, n]) => (
            <g key={n}>
              <circle cx={x} cy={y} r={62} fill="#3a3630" stroke={C.outline} strokeWidth={7} />
              <Sans x={x} y={y + 18} size={48} color={C.yellow}>{n}</Sans>
            </g>
          ))}
        </Scene>
      </Camera>
      <Typo top={545} size={78} delay={2}>속임수가 아니다</Typo>
      <Typo top={1420} size={56} delay={26} serif={false} color="#d8d0c2">전부 자연스러운 동맹</Typo>
    </AbsoluteFill>
  );
};

/* s7 — Second Hook: 전쟁·동맹·산업 → 다른 묶음 */
const S7: React.FC<{ dur: number }> = () => (
  <AbsoluteFill>
    <BgMesh tint={C.steel} tint2={C.amber} />
    <Scene ground={1600} groundCol="#26242a">
      <Skyline y={1600} seed={117} minY={1420} />
    </Scene>
    <div style={{ position: "absolute", top: 640, left: 0, right: 0, display: "flex",
      justifyContent: "center", gap: 22 }}>
      {["전쟁", "동맹", "산업"].map((t, i) => (
        <Entrance key={t} delay={4 + i * 6}>
          <Card w={250} outline="#5a6072" style={{ padding: "22px 10px" }}>
            <span style={{ fontSize: 50 }}>{t}</span></Card>
        </Entrance>
      ))}
    </div>
    <Entrance delay={26} from={16} style={{ position: "absolute", top: 880, width: "100%",
      display: "flex", justifyContent: "center" }}>
      <svg width={60} height={80}>
        <line x1={30} y1={0} x2={30} y2={52} stroke={C.amber} strokeWidth={10} />
        <polygon points="30,76 10,50 50,50" fill={C.amber} />
      </svg>
    </Entrance>
    <Entrance delay={34} style={{ position: "absolute", top: 1010, width: "100%",
      display: "flex", justifyContent: "center" }}>
      <Card w={620} outline={C.yellow}>
        <span style={{ fontSize: 54, color: C.yellow, whiteSpace: "nowrap" }}>다른 공약 묶음</span></Card>
    </Entrance>
  </AbsoluteFill>
);

/* s8 — 본 페이오프: 이념이 아니라 역사 / 다른 세계의 자 */
const S8: React.FC<{ dur: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const crack = spring({ frame: frame - 30, fps, config: theme.spring.bouncy });
  return (
    <AbsoluteFill>
      <BgMesh tint={C.red} tint2={C.steel} />
      <Camera dur={dur} zoom={1.05}>
        <Scene ground={1560} groundCol="#26242a">
          {/* 부러진 나침반 */}
          <circle cx={540} cy={1120} r={210} fill="#2a2e3a" stroke={C.outline} strokeWidth={12} />
          <circle cx={540} cy={1120} r={168} fill="none" stroke="#57606f" strokeWidth={6} />
          <g transform={`rotate(${interpolate(crack, [0, 1], [0, -34])} 540 1120)`}>
            <line x1={540} y1={1120} x2={540} y2={960} stroke={C.red} strokeWidth={16} strokeLinecap="round" />
          </g>
          <g opacity={crack} transform="rotate(28 540 1120)">
            <line x1={540} y1={1120} x2={660} y2={1230} stroke="#787c8a" strokeWidth={14} strokeLinecap="round" />
          </g>
          <circle cx={540} cy={1120} r={22} fill={C.paper} stroke={C.outline} strokeWidth={6} />
        </Scene>
      </Camera>
      <Typo top={545} size={72} delay={2}>이념이 아니라 역사</Typo>
      <Typo top={1420} size={62} color={C.yellow} delay={30}>다른 세계의 자일 뿐</Typo>
    </AbsoluteFill>
  );
};

/* s9 — 확장: 여러분 잘못이 아니다 */
const S9: React.FC<{ dur: number }> = ({ dur }) => (
  <AbsoluteFill>
    <BgMesh tint={C.yellow} tint2={C.steel} />
    <Camera dur={dur} zoom={1.06}>
      <Scene ground={1470} groundCol="#26242a">
        <Person x={540} y={1560} height={370} outfit="student" expr="worried"
          pose="stand" tie="#3e5a78" />
      </Scene>
    </Camera>
    <Typo top={620} size={92} delay={2}>분류가 안 되는 건</Typo>
    <Typo top={840} size={116} color={C.yellow} delay={8}>당신 잘못이 아니다</Typo>
  </AbsoluteFill>
);

/* s10 — 다음 모순: 5표 (하드컷) */
const S10: React.FC<{ dur: number }> = ({ dur }) => (
  <AbsoluteFill>
    <BgMesh tint={C.amber} />
    <Camera dur={dur} zoom={1.06}>
      <Scene ground={1560} groundCol="#26242a" />
    </Camera>
    <Typo top={600} size={96} delay={2}>분류 말고 투표를</Typo>
    <Typo top={820} size={150} color={C.yellow} delay={8}>당신에게 5표</Typo>
  </AbsoluteFill>
);

export const EP11_SCENES = [S1, Anchor1946, S3, S4, S5, S6, S7, S8, S9, S10];
