import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";
import { theme } from "../../theme";
import { BgMesh, Camera } from "../../kit/layers";
import { Entrance, Stamp, Card } from "../../kit/ui";
import { Person } from "../../kit/people";
import { Skyline, Train, Rail, Smoke } from "../../kit/props";
import { Anchor1946, Scene, Sans, Typo, GROUND } from "../common";

const C = theme.colors;

/* s1 — WTF: 밤 플랫폼의 유학생 + 平凡 스탬프 */
const S1: React.FC<{ dur: number }> = ({ dur }) => (
  <AbsoluteFill>
    <BgMesh tint={C.amber} tint2={C.steel} />
    <Camera dur={dur} zoom={1.045}>
      <Scene>
        <Skyline y={1200} seed={61} minY={700} />
        <Rail x0={-40} x1={1120} y={1235} />
        <Train x={880} y={1235} scale={0.8} cars={2} roll={0} />
        <rect x={0} y={1330} width={1080} height={590} fill="#33313a" />
        <rect x={0} y={1322} width={1080} height={16} fill="#454351" />
        <Sans x={215} y={1300} size={40} color="#d2c9a0">난징행 · 매일 밤</Sans>
        <Person x={620} y={1660} height={430} outfit="student" expr="smile"
          pose="hold_case" tie="#3e5a78" facing={1} />
      </Scene>
    </Camera>
    <Entrance delay={4} from={-30} style={{ position: "absolute", top: 528, width: "100%",
      textAlign: "center" }}>
      <span style={{ fontFamily: theme.font.sans, fontSize: 54, color: C.paper,
        textShadow: "0 4px 16px #000" }}>이 세계 청년에게 중국 유학은</span>
    </Entrance>
    <div style={{ position: "absolute", top: 645, width: "100%",
      display: "flex", justifyContent: "center" }}>
      <Stamp text="平凡" delay={14} size={380} textColor={C.yellow} />
    </div>
  </AbsoluteFill>
);

/* s3 — 약속 */
const S3: React.FC<{ dur: number }> = ({ dur }) => (
  <AbsoluteFill>
    <BgMesh tint={C.yellow} />
    <Camera dur={dur} zoom={1.05}>
      <Scene ground={1470} groundCol="#26242a">
        <Person x={540} y={1570} height={360} outfit="student" expr="worried"
          pose="stand" tie="#3e5a78" />
      </Scene>
    </Camera>
    <Typo top={620} size={104} delay={3}>정치는 싸운다</Typo>
    <Typo top={880} size={170} color={C.yellow} delay={11}>생활은?</Typo>
  </AbsoluteFill>
);

/* s4 — 국경이 아니라 노선: 밤기차 출발 */
const S4: React.FC<{ dur: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const dx = interpolate(frame, [30, dur], [0, 900],
    { easing: theme.ease.in, extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <AbsoluteFill>
      <BgMesh tint={C.steel} />
      <Camera dur={dur} zoom={1.045}>
        <Scene>
          <Skyline y={1230} seed={64} minY={760} />
          <Rail x0={-40} x1={1120} y={1265} />
          <g transform={`translate(${dx},0)`}>
            <Train x={760} y={1265} scale={0.9} cars={2} roll={dx > 0 ? 6 : 0} />
            <Smoke x={700} y={1080} scale={0.9} />
          </g>
          <rect x={0} y={1360} width={1080} height={560} fill="#33313a" />
          <rect x={0} y={1352} width={1080} height={16} fill="#454351" />
          <Person x={250} y={1640} height={380} outfit="student" expr="smile"
            pose="wave" tie="#3e5a78" facing={1} waveArm />
          <Person x={450} y={1660} height={360} outfit="suit_b" expr="smile"
            pose="hold_case" tie="#3e5a78" facing={1} />
        </Scene>
      </Camera>
      <Typo top={555} size={86} delay={4}>국경이 아니라 노선</Typo>
      <Entrance delay={20} style={{ position: "absolute", top: 700, width: "100%",
        display: "flex", justifyContent: "center" }}>
        <Card w={560} outline="#5a6072">
          <span style={{ fontSize: 46, whiteSpace: "nowrap" }}>부산 → 난징 · 매일 밤 출발</span>
        </Card>
      </Entrance>
    </AbsoluteFill>
  );
};

/* s5 — 언어: 초등 교실 칠판 中國語 */
const S5: React.FC<{ dur: number }> = ({ dur }) => (
  <AbsoluteFill>
    <BgMesh tint={C.green} tint2={C.amber} />
    <Camera dur={dur} zoom={1.05}>
      <Scene ground={1480} groundCol="#332f2a">
        {/* 칠판 */}
        <rect x={150} y={620} width={780} height={520} rx={18} fill="#2e4436"
          stroke="#6e6250" strokeWidth={16} />
        <text x={540} y={840} textAnchor="middle" fontFamily={theme.font.serif}
          fontSize={150} fill="#e6e2d2">中國語</text>
        <text x={540} y={980} textAnchor="middle" fontFamily={theme.font.sans}
          fontSize={54} fill="#c2d8c6">1교시 · 초등 정규 과목</text>
        <rect x={150} y={1140} width={780} height={26} fill="#6e6250" stroke={C.outline} strokeWidth={5} />
        <Person x={860} y={1520} height={400} outfit="suit_b" expr="smile"
          pose="point_l" tie="#3e5a78" facing={-1} />
        <Person x={300} y={1560} height={320} outfit="student" expr="surprised"
          pose="hands_up" tie="#3e5a78" />
      </Scene>
    </Camera>
  </AbsoluteFill>
);

/* s6 — 일자리: 승진 계단 */
const S6: React.FC<{ dur: number }> = ({ dur }) => {
  const steps = [["서울 본사", "#5a6072", C.paper], ["대륙 지사", C.amber, C.yellow]];
  return (
    <AbsoluteFill>
      <BgMesh tint={C.amber} />
      <Camera dur={dur} zoom={1.05}>
        <Scene ground={1560} groundCol="#26242a">
          {[0, 1, 2, 3].map((k) => (
            <rect key={k} x={140 + k * 200} y={1560 - (k + 1) * 170} width={800 - k * 200}
              height={(k + 1) * 170} fill={k === 3 ? "#4a4436" : "#3a3630"}
              stroke={C.outline} strokeWidth={6} transform={`translate(${0},0)`} />
          ))}
          <Person x={480} y={1220} height={380} outfit="suit" expr="smug"
            pose="point_r" tie="#983a2e" facing={1} />
          <polygon points="900,760 860,880 940,880" fill={C.amber} stroke={C.outline} strokeWidth={6} />
          <line x1={900} y1={880} x2={900} y2={1010} stroke={C.amber} strokeWidth={16} />
        </Scene>
      </Camera>
      <Typo top={555} size={90} delay={3}>승진 코스</Typo>
      <div style={{ position: "absolute", top: 710, left: 0, right: 0, display: "flex",
        justifyContent: "center", gap: 46 }}>
        {steps.map(([t, oc, tc], i) => (
          <Entrance key={t} delay={12 + i * 8}>
            <Card w={i ? 420 : 360} outline={oc}>
              <span style={{ fontSize: 50, color: tc, whiteSpace: "nowrap" }}>{t} {i ? "↑" : ""}</span>
            </Card>
          </Entrance>
        ))}
      </div>
    </AbsoluteFill>
  );
};

/* s7 — 문화: 차트 + 드라마 */
const S7: React.FC<{ dur: number }> = () => (
  <AbsoluteFill>
    <BgMesh tint={C.red} tint2={C.amber} />
    <Scene ground={1600} groundCol="#26242a">
      <Skyline y={1600} seed={67} minY={1400} />
    </Scene>
    <Entrance delay={5} style={{ position: "absolute", top: 580, left: 110, width: 520 }}>
      <div style={{ background: "rgba(24,28,40,0.9)", border: "6px solid #5a6072",
        borderRadius: 20, padding: "26px 34px", fontFamily: theme.font.sans }}>
        <div style={{ fontSize: 40, color: "#9a9eaa", marginBottom: 16 }}>주간 차트</div>
        {[["1", "상하이 밴드", C.amber], ["2", "부산 힙합", C.paper],
          ["3", "난징 발라드", C.paper]].map(([n, t, col]) => (
          <div key={n} style={{ display: "flex", gap: 22, fontSize: 46, marginTop: 12 }}>
            <span style={{ color: C.amber, fontFamily: theme.font.serif }}>{n}</span>
            <span style={{ color: col as string }}>{t}</span>
          </div>
        ))}
      </div>
    </Entrance>
    <Entrance delay={16} style={{ position: "absolute", top: 1000, right: 100, width: 460 }}>
      <div style={{ background: "rgba(24,28,40,0.9)", border: `6px solid ${C.amber}`,
        borderRadius: 20, padding: "30px 34px", fontFamily: theme.font.sans,
        transform: "rotate(-2deg)", textAlign: "center" }}>
        <div style={{ fontSize: 42, color: "#9a9eaa" }}>주말 드라마</div>
        <div style={{ fontSize: 58, color: C.yellow, marginTop: 12 }}>항저우 로케</div>
      </div>
    </Entrance>
  </AbsoluteFill>
);

/* s8 — 같은 식탁: 아버지와 딸 */
const S8: React.FC<{ dur: number }> = ({ dur }) => (
  <AbsoluteFill>
    <BgMesh tint={C.amber} tint2={C.green} />
    <Camera dur={dur} zoom={1.055}>
      <Scene ground={1500} groundCol="#332f2a">
        {/* 식탁 + 전등 */}
        <line x1={540} y1={420} x2={540} y2={700} stroke="#454351" strokeWidth={10} />
        <polygon points="540,700 470,790 610,790" fill="#6e6250" stroke={C.outline} strokeWidth={6} />
        <circle cx={540} cy={800} r={26} fill="#ffe8a0" opacity={0.9} />
        <rect x={250} y={1210} width={580} height={34} rx={10} fill="#57503f"
          stroke={C.outline} strokeWidth={7} />
        <rect x={300} y={1244} width={30} height={240} fill="#4a4436" />
        <rect x={750} y={1244} width={30} height={240} fill="#4a4436" />
        <Person x={215} y={1490} height={400} outfit="worker" expr="closed" hat="cap"
          pose="stand" facing={1} />
        <Person x={880} y={1490} height={380} outfit="student" expr="smile"
          pose="stand" tie="#3e5a78" facing={-1} />
        {/* 소품: 피켓(아버지) / 서류(딸) */}
        <rect x={120} y={1130} width={150} height={90} rx={8} fill="#e8e2d4"
          stroke={C.outline} strokeWidth={5} transform="rotate(-8 195 1175)" />
        <text x={195} y={1188} textAnchor="middle" fontFamily={theme.font.sans}
          fontSize={30} fill={C.red} transform="rotate(-8 195 1175)">규제하라</text>
        <rect x={810} y={1120} width={140} height={100} rx={6} fill="#ded8ca"
          stroke={C.outline} strokeWidth={5} transform="rotate(6 880 1170)" />
        <text x={880} y={1165} textAnchor="middle" fontFamily={theme.font.sans}
          fontSize={26} fill={C.ink} transform="rotate(6 880 1170)">南京 면접</text>
        <Sans x={215} y={1550} size={38} color="#c8c4bc">아버지 박성호</Sans>
        <Sans x={880} y={1550} size={38} color="#c8c4bc">딸 박지은</Sans>
      </Scene>
    </Camera>
    <Typo top={555} size={84} delay={4}>같은 식탁</Typo>
  </AbsoluteFill>
);

/* s9 — Payoff: 정치는 진영을, 생활은 노선을 */
const S9: React.FC<{ dur: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const draw = interpolate(frame, [24, 70], [0, 1],
    { easing: theme.ease.inOut, extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <AbsoluteFill>
      <BgMesh />
      <Camera dur={dur} zoom={1.05}>
        <Scene ground={1620} groundCol="#26242a">
          <polyline points="800,1400 640,1220 480,1060 330,900"
            fill="none" stroke={C.outline} strokeWidth={22} strokeLinejoin="round"
            strokeDasharray={1200} strokeDashoffset={1200 * (1 - draw)} />
          <polyline points="800,1400 640,1220 480,1060 330,900"
            fill="none" stroke={C.amber} strokeWidth={12} strokeLinejoin="round"
            strokeDasharray={1200} strokeDashoffset={1200 * (1 - draw)} />
          <circle cx={800} cy={1400} r={22} fill={C.amber} stroke={C.outline} strokeWidth={6} />
          <circle cx={330} cy={900} r={22} fill={C.amber} stroke={C.outline} strokeWidth={6} />
          <Sans x={860} y={1400} size={44} anchor="start" color={C.yellow}>부산</Sans>
          <Sans x={330} y={860} size={44} color={C.yellow}>난징</Sans>
        </Scene>
      </Camera>
      <Typo top={560} size={76} delay={3}>정치는 진영을</Typo>
      <Typo top={705} size={76} color={C.yellow} delay={10}>생활은 노선을</Typo>
    </AbsoluteFill>
  );
};

/* s10 — 확장: 같은 지도, 반대 방향 (일본 예고) */
const S10: React.FC<{ dur: number }> = ({ dur }) => (
  <AbsoluteFill>
    <BgMesh tint={C.red} tint2={C.steel} />
    <Camera dur={dur} zoom={1.05}>
      <Scene ground={1580} groundCol="#26242a">
        {/* 간이 지도: 대륙(좌) — 한국(중) — 일본(우) */}
        <path d="M 80 800 q 200 -120 320 40 q 60 120 -40 260 q -180 80 -280 -60 Z"
          fill="#3a4048" stroke={C.outline} strokeWidth={7} />
        <rect x={470} y={880} width={130} height={260} rx={40} fill="#4a5058"
          stroke={C.outline} strokeWidth={7} />
        <ellipse cx={840} cy={1120} rx={150} ry={70} fill="#4a5058"
          stroke={C.outline} strokeWidth={7} transform="rotate(-30 840 1120)" />
        <Sans x={230} y={930} size={46} color="#ecc478">自由中國</Sans>
        <Sans x={535} y={1010} size={40}>한국</Sans>
        <Sans x={880} y={1130} size={40} color="#e68c80">일본</Sans>
        {/* 한국→대륙 화살표 (앰버), 일본→반대 (레드) */}
        <line x1={465} y1={990} x2={330} y2={950} stroke={C.amber} strokeWidth={13} />
        <polygon points="310,944 360,928 356,972" fill={C.amber} />
        <line x1={790} y1={1090} x2={900} y2={1030} stroke={C.red} strokeWidth={13} />
        <polygon points="920,1018 872,1016 894,1060" fill={C.red} />
      </Scene>
    </Camera>
    <Typo top={555} size={82} delay={3}>같은 지도, 반대 방향</Typo>
  </AbsoluteFill>
);

/* s11 — 다음 모순: 일본 좌파 재무장 (하드컷) */
const S11: React.FC<{ dur: number }> = ({ dur }) => (
  <AbsoluteFill>
    <BgMesh tint={C.red} />
    <Camera dur={dur} zoom={1.06}>
      <Scene ground={1560} groundCol="#26242a" />
    </Camera>
    <Typo top={600} size={92} delay={2}>이 세계의 일본에선</Typo>
    <Typo top={790} size={150} color={C.yellow} delay={7}>좌파가</Typo>
    <Typo top={1050} size={104} delay={13}>재무장을 외칩니다</Typo>
  </AbsoluteFill>
);

export const EP6_SCENES = [S1, Anchor1946, S3, S4, S5, S6, S7, S8, S9, S10, S11];
