import React from "react";
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { theme } from "../../theme";
import { BgMesh, Camera } from "../../kit/layers";
import { Entrance, Card, Stamp } from "../../kit/ui";
import { Person } from "../../kit/people";
import { Skyline, Ship, Crane, Containers, Flag } from "../../kit/props";
import { Anchor1946, Scene, Sans, Typo, GROUND } from "../common";

const C = theme.colors;

/* s1 — WTF: 대만 섬 + 독립 X */
const S1: React.FC<{ dur: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const p = spring({ frame: frame - 4, fps, config: theme.spring.smooth });
  const x = spring({ frame: frame - 22, fps, config: theme.spring.bouncy });
  return (
    <AbsoluteFill>
      <BgMesh tint={C.steel} tint2={C.red} />
      <Camera dur={dur} zoom={1.05}>
        <Scene ground={1500} groundCol="#243038">
          <ellipse cx={540} cy={1120} rx={200} ry={300} fill="#4a5058"
            stroke={C.outline} strokeWidth={9} opacity={p} />
          <Sans x={540} y={1105} size={64}>臺灣</Sans>
          <g opacity={x}>
            <rect x={300} y={720} width={480} height={140} rx={18}
              fill="rgba(24,28,40,0.92)" stroke="#5a6072" strokeWidth={6} />
            <Sans x={470} y={772} size={62} color="#9a9eaa">독립</Sans>
            <line x1={640} y1={752} x2={740} y2={832} stroke={C.red} strokeWidth={14} strokeLinecap="round" />
            <line x1={740} y1={752} x2={640} y2={832} stroke={C.red} strokeWidth={14} strokeLinecap="round" />
          </g>
        </Scene>
      </Camera>
      <Entrance delay={2} from={-30} style={{ position: "absolute", top: 545, width: "100%",
        textAlign: "center" }}>
        <span style={{ fontFamily: theme.font.serif, fontSize: 76, color: C.paper,
          textShadow: "0 5px 22px #000" }}>최대 쟁점은</span>
      </Entrance>
    </AbsoluteFill>
  );
};

/* s3 — 근거1: 존재의 질문이 없다 */
const S3: React.FC<{ dur: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const fade = interpolate(frame, [16, 52], [1, 0.12],
    { easing: theme.ease.inOut, extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <AbsoluteFill>
      <BgMesh tint={C.steel} />
      <Camera dur={dur} zoom={1.05}>
        <Scene ground={1520} groundCol="#243038">
          <g opacity={fade}>
            <rect x={120} y={780} width={380} height={150} rx={18}
              fill="rgba(34,26,28,0.9)" stroke={C.red} strokeWidth={6} />
            <Sans x={310} y={834} size={50} color="#e68c80">분리의 공포</Sans>
            <rect x={580} y={780} width={380} height={150} rx={18}
              fill="rgba(34,26,28,0.9)" stroke={C.red} strokeWidth={6} />
            <Sans x={770} y={834} size={50} color="#e68c80">병합의 위협</Sans>
          </g>
          <Person x={540} y={1540} height={400} outfit="student" expr="neutral"
            pose="stand" tie="#3e5a78" />
        </Scene>
      </Camera>
      <Typo top={545} size={82} delay={2}>둘 다 없다</Typo>
      <Typo top={1080} size={62} delay={30} serif={false} color="#d8d0c2">존재를 묻는 질문이 없다</Typo>
    </AbsoluteFill>
  );
};

/* s4 — 미니 페이오프: 빈 자리를 생활이 채운다 → 쟁점은 난징과의 거리 */
const S4: React.FC<{ dur: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const p = spring({ frame: frame - 20, fps, config: theme.spring.snappy });
  return (
    <AbsoluteFill>
      <BgMesh tint={C.amber} tint2={C.steel} />
      <Camera dur={dur} zoom={1.05}>
        <Scene ground={1500} groundCol="#243038">
          {/* 난징 ↔ 대만, 거리 자 */}
          <circle cx={230} cy={1000} r={80} fill="#5c4a2e" stroke={C.outline} strokeWidth={8} />
          <Sans x={230} y={1022} size={46} color={C.amber}>南京</Sans>
          <ellipse cx={860} cy={1060} rx={90} ry={140} fill="#4a5058"
            stroke={C.outline} strokeWidth={8} />
          <Sans x={860} y={1078} size={44}>臺灣</Sans>
          <line x1={320} y1={1030} x2={760} y2={1050} stroke={C.outline} strokeWidth={18} />
          <line x1={320} y1={1030} x2={760} y2={1050} stroke={C.yellow} strokeWidth={10}
            strokeDasharray="24 16" />
          <g opacity={p}>
            <rect x={410} y={1130} width={280} height={92} rx={14}
              fill="rgba(24,28,40,0.92)" stroke={C.yellow} strokeWidth={6} />
            <Sans x={550} y={1166} size={44} color={C.yellow}>거리</Sans>
          </g>
        </Scene>
      </Camera>
      <Typo top={545} size={76} delay={2}>그 자리를 생활이 채운다</Typo>
      <Entrance delay={28} style={{ position: "absolute", top: 700, width: "100%",
        textAlign: "center" }}>
        <span style={{ fontFamily: theme.font.serif, fontSize: 72, color: C.yellow,
          textShadow: "0 5px 22px #000" }}>쟁점은 난징과의 거리</span>
      </Entrance>
    </AbsoluteFill>
  );
};

/* s5 — 근거2: 세금·항만·교과서 3카드 */
const S5: React.FC<{ dur: number }> = () => (
  <AbsoluteFill>
    <BgMesh tint={C.amber} />
    <Scene ground={1600} groundCol="#26242a">
      <Skyline y={1600} seed={95} minY={1400} />
    </Scene>
    <Typo top={545} size={78} delay={2}>세 가지 쟁점</Typo>
    <div style={{ position: "absolute", top: 720, left: 0, right: 0, display: "flex",
      flexDirection: "column", alignItems: "center", gap: 34 }}>
      {[["稅", "세금을 얼마나 남길지"], ["港", "항만을 누가 운영할지"],
        ["書", "교과서를 어디서 정할지"]].map(([ch, t], i) => (
        <Entrance key={ch} delay={6 + i * 9}>
          <Card w={720} outline={i === 0 ? C.amber : "#5a6072"}>
            <div style={{ display: "flex", alignItems: "center", justifyContent: "center", gap: 28 }}>
              <span style={{ fontFamily: theme.font.serif, fontSize: 66, color: C.amber }}>{ch}</span>
              <span style={{ fontSize: 46, whiteSpace: "nowrap" }}>{t}</span>
            </div>
          </Card>
        </Entrance>
      ))}
    </div>
  </AbsoluteFill>
);

/* s6 — 근거3: 가오슝 항만, 린원제 */
const S6: React.FC<{ dur: number }> = ({ dur }) => (
  <AbsoluteFill>
    <BgMesh tint={C.steel} tint2={C.amber} />
    <Camera dur={dur} zoom={1.05} panX={-10}>
      <Scene>
        <Ship x={760} y={1100} scale={0.82} />
        <rect x={0} y={1240} width={1080} height={680} fill={GROUND} />
        <rect x={0} y={1232} width={1080} height={16} fill="#3f434f" />
        <Crane x={880} y={1232} dir={-1} scale={0.86} />
        <Containers x={80} y={1232} />
        <Person x={360} y={1630} height={460} outfit="worker" expr="neutral" hat="cap"
          pose="stand" facing={1} />
      </Scene>
    </Camera>
    <Typo top={545} size={72} delay={2}>투표 기준은</Typo>
    <div style={{ position: "absolute", top: 700, left: 0, right: 0, display: "flex",
      justifyContent: "center", gap: 40 }}>
      <Entrance delay={10}><Card w={330} outline="#5a6072">
        <span style={{ fontSize: 50, color: "#7c8090", textDecoration: "line-through" }}>국기</span></Card></Entrance>
      <Entrance delay={16}><Card w={400} outline={C.yellow}>
        <span style={{ fontSize: 50, color: C.yellow, whiteSpace: "nowrap" }}>하역료 배분</span></Card></Entrance>
    </div>
    <Entrance delay={26} style={{ position: "absolute", top: 1620, width: "100%",
      display: "flex", justifyContent: "center" }}>
      <div style={{ background: "#0d0b0a", borderRadius: 14, padding: "14px 30px",
        fontFamily: theme.font.sans, fontSize: 38, color: C.paper }}>
        린원제 (44) · 가오슝 항만 노동자</div>
    </Entrance>
  </AbsoluteFill>
);

/* s7 — Second Hook: 대만·홍콩의 공통 구호 = 자치 */
const S7: React.FC<{ dur: number }> = ({ dur }) => (
  <AbsoluteFill>
    <BgMesh tint={C.green} tint2={C.steel} />
    <Camera dur={dur} zoom={1.05}>
      <Scene ground={1560} groundCol="#243038">
        <ellipse cx={280} cy={1120} rx={110} ry={165} fill="#4a5058"
          stroke={C.outline} strokeWidth={8} />
        <Sans x={280} y={1138} size={46}>臺灣</Sans>
        <ellipse cx={820} cy={1150} rx={95} ry={110} fill="#4a5058"
          stroke={C.outline} strokeWidth={8} />
        <Sans x={820} y={1168} size={46}>香港</Sans>
        <Flag x={280} y={960} w={200} color="#4a6a4a" h={280} />
        <Flag x={820} y={1000} w={-200} color="#4a6a4a" h={280} />
      </Scene>
    </Camera>
    <Typo top={545} size={72} delay={2}>두 섬의 공통 구호</Typo>
    <div style={{ position: "absolute", top: 690, width: "100%",
      display: "flex", justifyContent: "center" }}>
      <Stamp text="自治" delay={12} size={300} color="#4a6a4a" textColor={C.greenText} />
    </div>
  </AbsoluteFill>
);

/* s8 — 본 페이오프: 안보의 언어 → 회계의 언어 */
const S8: React.FC<{ dur: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const p = spring({ frame: frame - 24, fps, config: theme.spring.smooth });
  return (
    <AbsoluteFill>
      <BgMesh />
      <Camera dur={dur} zoom={1.04}>
        <Scene ground={1600} groundCol="#26242a">
          <Skyline y={1600} seed={99} minY={1400} />
        </Scene>
      </Camera>
      <Typo top={545} size={76} delay={2}>사라진 게 아니라</Typo>
      <div style={{ position: "absolute", top: 730, left: 0, right: 0, display: "flex",
        flexDirection: "column", alignItems: "center", gap: 24 }}>
        <Entrance delay={8}>
          <Card w={620} outline="#5a6072">
            <span style={{ fontSize: 52, color: C.paper, whiteSpace: "nowrap" }}>안보의 언어</span></Card>
        </Entrance>
        <div style={{ opacity: p }}>
          <svg width={60} height={70}>
            <line x1={30} y1={0} x2={30} y2={44} stroke={C.amber} strokeWidth={10} />
            <polygon points="30,66 10,42 50,42" fill={C.amber} />
          </svg>
        </div>
        <Entrance delay={26}>
          <Card w={620} outline={C.yellow}>
            <span style={{ fontSize: 52, color: C.yellow, whiteSpace: "nowrap" }}>회계의 언어</span></Card>
        </Entrance>
      </div>
      <Typo top={1300} size={46} delay={40} serif={false} color="#d8d0c2">번역됐을 뿐이다</Typo>
    </AbsoluteFill>
  );
};

/* s9 — 확장: 표를 던질 차례 */
const S9: React.FC<{ dur: number }> = ({ dur }) => (
  <AbsoluteFill>
    <BgMesh tint={C.yellow} tint2={C.amber} />
    <Camera dur={dur} zoom={1.06}>
      <Scene ground={1470} groundCol="#26242a">
        <Person x={540} y={1560} height={370} outfit="student" expr="smile"
          pose="reach_r" tie="#3e5a78" facing={0} />
      </Scene>
    </Camera>
    <Typo top={620} size={96} delay={2}>이 지형 위에서</Typo>
    <Typo top={840} size={124} color={C.yellow} delay={8}>표를 던질 차례</Typo>
  </AbsoluteFill>
);

/* s10 — 다음 모순 (하드컷) */
const S10: React.FC<{ dur: number }> = ({ dur }) => (
  <AbsoluteFill>
    <BgMesh tint={C.amber} tint2={C.green} />
    <Camera dur={dur} zoom={1.06}>
      <Scene ground={1560} groundCol="#26242a" />
    </Camera>
    <Typo top={620} size={90} delay={2}>2080년 대학생에게</Typo>
    <Typo top={830} size={130} color={C.yellow} delay={8}>보수는</Typo>
    <Typo top={1060} size={110} delay={14}>시장이 아니다</Typo>
  </AbsoluteFill>
);

export const EP9_SCENES = [S1, Anchor1946, S3, S4, S5, S6, S7, S8, S9, S10];
