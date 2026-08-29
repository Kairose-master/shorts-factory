import React from "react";
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { theme } from "../../theme";
import { BgMesh, Camera } from "../../kit/layers";
import { Entrance, Card, Stamp } from "../../kit/ui";
import { Person } from "../../kit/people";
import { Skyline, Train, Rail } from "../../kit/props";
import { Anchor1946, Scene, Sans, Typo } from "../common";

const C = theme.colors;

/* s1 — WTF: 보수 = 시장? 아니오 */
const S1: React.FC<{ dur: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const x = spring({ frame: frame - 20, fps, config: theme.spring.bouncy });
  return (
    <AbsoluteFill>
      <BgMesh tint={C.amber} tint2={C.green} />
      <Camera dur={dur} zoom={1.05}>
        <Scene ground={1440} groundCol="#26242a">
          <Skyline y={1440} seed={101} minY={980} />
          <Person x={330} y={1470} height={430} outfit="student" expr="surprised"
            pose="stand" tie="#3e5a78" facing={1} />
          <Person x={720} y={1470} height={410} outfit="student" expr="worried"
            pose="stand" tie="#3e5a78" facing={-1} />
          <Sans x={540} y={1520} size={38} color="#c8c4bc">2080년 난징대 캠퍼스</Sans>
          <g opacity={x}>
            <rect x={280} y={700} width={520} height={150} rx={18}
              fill="rgba(24,28,40,0.92)" stroke="#5a6072" strokeWidth={6} />
            <Sans x={480} y={758} size={60} color="#9a9eaa">보수 = 시장</Sans>
            <line x1={660} y1={730} x2={770} y2={822} stroke={C.red} strokeWidth={15} strokeLinecap="round" />
            <line x1={770} y1={730} x2={660} y2={822} stroke={C.red} strokeWidth={15} strokeLinecap="round" />
          </g>
        </Scene>
      </Camera>
      <Entrance delay={2} from={-30} style={{ position: "absolute", top: 555, width: "100%",
        textAlign: "center" }}>
        <span style={{ fontFamily: theme.font.serif, fontSize: 72, color: C.paper,
          textShadow: "0 5px 22px #000" }}>2080년 대학생에게</span>
      </Entrance>
    </AbsoluteFill>
  );
};

/* s3 — 근거1: 국가가 깐 철도·공단·연금 */
const S3: React.FC<{ dur: number }> = ({ dur }) => (
  <AbsoluteFill>
    <BgMesh tint={C.amber} />
    <Camera dur={dur} zoom={1.05}>
      <Scene ground={1500} groundCol="#26242a">
        <Rail x0={-40} x1={1120} y={1300} />
        <Train x={860} y={1300} scale={0.62} cars={2} roll={0} />
        {/* 공단 */}
        <g transform="translate(120,1120)">
          <rect x={0} y={0} width={300} height={180} fill="#4a4436" stroke={C.outline} strokeWidth={7} />
          {[0, 1, 2].map((k) => (
            <polygon key={k} points={`${k * 100},0 ${k * 100 + 50},-58 ${k * 100 + 100},0`}
              fill="#5a5244" stroke={C.outline} strokeWidth={6} />
          ))}
        </g>
        <Person x={640} y={1560} height={400} outfit="coat" expr="closed"
          pose="arms_cross" facing={0} />
        <Sans x={640} y={1610} size={38} color="#c8c4bc">할아버지 세대</Sans>
      </Scene>
    </Camera>
    <Typo top={545} size={78} delay={2}>국가가 깔았다</Typo>
    <div style={{ position: "absolute", top: 700, left: 0, right: 0, display: "flex",
      justifyContent: "center", gap: 26 }}>
      {["철도", "공단", "연금"].map((t, i) => (
        <Entrance key={t} delay={8 + i * 6}>
          <Card w={230} outline={C.amber} style={{ padding: "20px 10px" }}>
            <span style={{ fontSize: 48, color: C.yellow }}>{t}</span></Card>
        </Entrance>
      ))}
    </div>
  </AbsoluteFill>
);

/* s4 — 미니 페이오프: 세대의 기억이 묶는다 */
const S4: React.FC<{ dur: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const p = spring({ frame: frame - 24, fps, config: theme.spring.snappy });
  return (
    <AbsoluteFill>
      <BgMesh tint={C.steel} tint2={C.amber} />
      <Camera dur={dur} zoom={1.05}>
        <Scene ground={1520} groundCol="#26242a">
          {/* 기억의 밧줄이 공약들을 묶는다 */}
          <ellipse cx={540} cy={1080} rx={330} ry={190} fill="none"
            stroke={C.amber} strokeWidth={16} strokeDasharray="30 18" />
          <Sans x={540} y={880} size={46} color={C.amber}>세대의 기억</Sans>
          {[["철도", 360, 1030], ["연금", 720, 1030], ["공단", 540, 1200]].map(([t, x, y]) => (
            <g key={t as string}>
              <circle cx={x as number} cy={y as number} r={68} fill="#3a3630"
                stroke={C.outline} strokeWidth={7} />
              <Sans x={x as number} y={(y as number) + 16} size={40}>{t}</Sans>
            </g>
          ))}
        </Scene>
      </Camera>
      <Typo top={545} size={74} delay={2}>논리가 아니라</Typo>
      <div style={{ position: "absolute", top: 1360, width: "100%", textAlign: "center",
        opacity: p, transform: `translateY(${interpolate(p, [0, 1], [26, 0])}px)` }}>
        <span style={{ fontFamily: theme.font.serif, fontSize: 74, color: C.yellow,
          textShadow: "0 5px 22px #000" }}>그래서 보수의 뜻이 다르다</span>
      </div>
    </AbsoluteFill>
  );
};

/* s5 — 근거2: 복지를 공기처럼 */
const S5: React.FC<{ dur: number }> = ({ dur }) => (
  <AbsoluteFill>
    <BgMesh tint={C.green} tint2={C.steel} />
    <Camera dur={dur} zoom={1.05}>
      <Scene ground={1500} groundCol="#26242a">
        {/* 공기 = 은은한 원들 */}
        {[[300, 900, 90], [780, 860, 110], [540, 1080, 140], [220, 1180, 80],
          [880, 1160, 96]].map(([x, y, r], i) => (
          <circle key={i} cx={x} cy={y} r={r} fill="rgba(110,168,92,0.16)"
            stroke="#4a6a4a" strokeWidth={5} />
        ))}
        <Sans x={540} y={1096} size={46} color={C.greenText}>복지</Sans>
        <Person x={540} y={1560} height={380} outfit="student" expr="smile"
          pose="stand" tie="#3e5a78" />
      </Scene>
    </Camera>
    <Typo top={545} size={76} delay={2}>공기처럼 마시며 태어났다</Typo>
    <Typo top={700} size={58} delay={16} serif={false} color="#d8d0c2">이념이 아니라 원래 있던 것</Typo>
  </AbsoluteFill>
);

/* s6 — 근거3: 천위팅의 정의 */
const S6: React.FC<{ dur: number }> = ({ dur }) => (
  <AbsoluteFill>
    <BgMesh tint={C.amber} />
    <Camera dur={dur} zoom={1.05}>
      <Scene ground={1480} groundCol="#332f2a">
        {/* 캠퍼스 정문 */}
        <rect x={140} y={880} width={44} height={600} fill="#4a4436" stroke={C.outline} strokeWidth={6} />
        <rect x={896} y={880} width={44} height={600} fill="#4a4436" stroke={C.outline} strokeWidth={6} />
        <rect x={120} y={820} width={840} height={64} rx={10} fill="#57503f"
          stroke={C.outline} strokeWidth={7} />
        <Sans x={540} y={838} size={44} color="#d2c9a0">南京大學</Sans>
        <Person x={400} y={1500} height={420} outfit="student" expr="smug"
          pose="point_r" tie="#3e5a78" facing={1} />
      </Scene>
    </Camera>
    <Entrance delay={10} style={{ position: "absolute", top: 1020, right: 90, width: 440 }}>
      <div style={{ background: "#e8e2d4", border: `7px solid ${C.outline}`, borderRadius: 14,
        transform: "rotate(2deg)", padding: "24px 26px", textAlign: "center" }}>
        <div style={{ fontFamily: theme.font.sans, fontSize: 34, color: "#6e6250" }}>보수 아저씨 =</div>
        <div style={{ fontFamily: theme.font.sans, fontSize: 46, color: C.ink, marginTop: 10 }}>
          연금에 손대지<br />말라는 사람</div>
      </div>
    </Entrance>
    <Entrance delay={24} style={{ position: "absolute", top: 1620, width: "100%",
      display: "flex", justifyContent: "center" }}>
      <div style={{ background: "#0d0b0a", borderRadius: 14, padding: "14px 30px",
        fontFamily: theme.font.sans, fontSize: 38, color: C.paper }}>
        천위팅 (20) · 난징대 2학년</div>
    </Entrance>
  </AbsoluteFill>
);

/* s7 — Second Hook: 시장화 = 급진 */
const S7: React.FC<{ dur: number }> = ({ dur }) => (
  <AbsoluteFill>
    <BgMesh tint={C.red} tint2={C.green} />
    <Camera dur={dur} zoom={1.05}>
      <Scene ground={1480} groundCol="#26242a">
        <Person x={540} y={1500} height={420} outfit="suit_r" expr="shout"
          pose="hands_up" facing={0} waveArm />
      </Scene>
    </Camera>
    <Entrance delay={4} style={{ position: "absolute", top: 560, width: "100%",
      display: "flex", justifyContent: "center" }}>
      <Card w={760} outline="#5a6072">
        <span style={{ fontSize: 50, whiteSpace: "nowrap" }}>복지를 줄이고 시장에 맡기자</span></Card>
    </Entrance>
    <div style={{ position: "absolute", top: 760, width: "100%",
      display: "flex", justifyContent: "center" }}>
      <Stamp text="急進" delay={20} size={340} textColor={C.yellow} />
    </div>
  </AbsoluteFill>
);

/* s8 — 본 페이오프: 내용이 아니라 위치 */
const S8: React.FC<{ dur: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const p = spring({ frame: frame - 18, fps, config: theme.spring.smooth });
  return (
    <AbsoluteFill>
      <BgMesh />
      <Camera dur={dur} zoom={1.04}>
        <Scene ground={1600} groundCol="#26242a">
          <Skyline y={1600} seed={108} minY={1400} />
          {/* 위치 다이어그램: 먼저 와 있던 것 기준 */}
          <line x1={140} y1={1180} x2={940} y2={1180} stroke={C.outline} strokeWidth={16} />
          <line x1={140} y1={1180} x2={940} y2={1180} stroke="#787c8a" strokeWidth={8} />
          <g opacity={p}>
            <circle cx={360} cy={1180} r={62} fill="#5c4a2e" stroke={C.outline} strokeWidth={7} />
            <Sans x={360} y={1198} size={40} color={C.yellow}>지키면</Sans>
            <Sans x={360} y={1300} size={44} color={C.amber}>보수</Sans>
            <circle cx={720} cy={1180} r={62} fill="#2e4436" stroke={C.outline} strokeWidth={7} />
            <Sans x={720} y={1198} size={40} color={C.greenText}>바꾸면</Sans>
            <Sans x={720} y={1300} size={44} color={C.greenText}>진보</Sans>
          </g>
        </Scene>
      </Camera>
      <Typo top={545} size={80} delay={2}>내용이 아니라 위치</Typo>
      <Typo top={720} size={56} delay={30} serif={false} color="#d8d0c2">무엇이 먼저 와 있었느냐</Typo>
    </AbsoluteFill>
  );
};

/* s9 — 확장: 라벨만 보고는 모른다 */
const S9: React.FC<{ dur: number }> = ({ dur }) => (
  <AbsoluteFill>
    <BgMesh tint={C.yellow} tint2={C.red} />
    <Camera dur={dur} zoom={1.06}>
      <Scene ground={1470} groundCol="#26242a">
        <Person x={540} y={1560} height={370} outfit="student" expr="worried"
          pose="stand" tie="#3e5a78" />
      </Scene>
    </Camera>
    <Typo top={620} size={92} delay={2}>라벨만 보고는</Typo>
    <Typo top={840} size={124} color={C.yellow} delay={8}>알 수 없다</Typo>
  </AbsoluteFill>
);

/* s10 — 다음 모순 (하드컷) */
const S10: React.FC<{ dur: number }> = ({ dur }) => (
  <AbsoluteFill>
    <BgMesh tint={C.steel} tint2={C.red} />
    <Camera dur={dur} zoom={1.06}>
      <Scene ground={1500} groundCol="#26242a">
        <Person x={540} y={1520} height={420} outfit="suit_b" expr="neutral"
          pose="stand" tie="#3e5a78" facing={0} />
      </Scene>
    </Camera>
    <Typo top={620} size={104} delay={2}>이 정치인은</Typo>
    <Typo top={830} size={116} color={C.yellow} delay={8}>좌파일까요,</Typo>
    <Typo top={1010} size={116} color={C.yellow} delay={13}>우파일까요?</Typo>
  </AbsoluteFill>
);

export const EP10_SCENES = [S1, Anchor1946, S3, S4, S5, S6, S7, S8, S9, S10];
