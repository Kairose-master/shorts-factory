import React from "react";
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { theme } from "../../theme";
import { BgMesh, Camera } from "../../kit/layers";
import { Entrance, Stamp, Card } from "../../kit/ui";
import { Person } from "../../kit/people";
import { Skyline, Flag, Picket } from "../../kit/props";
import { Anchor1946, Scene, Sans, Typo } from "../common";

const C = theme.colors;

/* s1 — WTF: 한 사람, 두 개의 말풍선 */
const S1: React.FC<{ dur: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const b1 = spring({ frame: frame - 8, fps, config: theme.spring.bouncy });
  const b2 = spring({ frame: frame - 26, fps, config: theme.spring.bouncy });
  const bubble = (x: number, y: number, w: number, p: number, flip: boolean,
    l1: string, l2: string, col: string) => (
    <g opacity={p} transform={`scale(${0.7 + 0.3 * p})`}
      style={{ transformOrigin: `${x}px ${y + 90}px` }}>
      <rect x={x - w / 2} y={y} width={w} height={170} rx={26} fill="#e8e2d4"
        stroke={C.outline} strokeWidth={8} />
      <polygon points={flip ? `${x + 60},${y + 168} ${x + 130},${y + 240} ${x + 130},${y + 168}`
        : `${x - 60},${y + 168} ${x - 130},${y + 240} ${x - 130},${y + 168}`}
        fill="#e8e2d4" stroke={C.outline} strokeWidth={7} />
      <text x={x} y={y + 70} textAnchor="middle" fontFamily={theme.font.sans}
        fontSize={44} fill={C.ink}>{l1}</text>
      <text x={x} y={y + 134} textAnchor="middle" fontFamily={theme.font.sans}
        fontSize={46} fill={col}>{l2}</text>
    </g>
  );
  return (
    <AbsoluteFill>
      <BgMesh tint={C.red} tint2={C.steel} />
      <Camera dur={dur} zoom={1.05}>
        <Scene ground={1430} groundCol="#28262a">
          <Skyline y={1430} seed={71} minY={950} />
          <Person x={540} y={1480} height={420} outfit="suit_b" expr="neutral"
            pose="point_r" tie="#3e5a78" facing={0} />
          {bubble(300, 620, 470, b1, false, "미군기지를", "줄이자", "#4a6a90")}
          {bubble(790, 850, 470, b2, true, "일본군을", "키우자", C.red)}
        </Scene>
      </Camera>
      <Entrance delay={44} style={{ position: "absolute", top: 1268, width: "100%",
        textAlign: "center" }}>
        <span style={{ fontFamily: theme.font.serif, fontSize: 74, color: C.yellow,
          textShadow: "0 5px 22px #000" }}>같은 사람의 말</span>
      </Entrance>
    </AbsoluteFill>
  );
};

/* (미사용) 약속 씬 — v2.0에서 삭제 */
const S3Unused: React.FC<{ dur: number }> = ({ dur }) => (
  <AbsoluteFill>
    <BgMesh tint={C.yellow} />
    <Camera dur={dur} zoom={1.05}>
      <Scene ground={1470} groundCol="#26242a">
        <Person x={540} y={1570} height={360} outfit="student" expr="worried"
          pose="stand" tie="#3e5a78" />
      </Scene>
    </Camera>
    <Typo top={620} size={100} delay={3}>말한 쪽은 좌파</Typo>
    <Typo top={880} size={170} color={C.yellow} delay={11}>왜?</Typo>
  </AbsoluteFill>
);

/* s4 — 기존 질서 = 미군: 기지 + 안보 우산 */
const S3: React.FC<{ dur: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const up = spring({ frame: frame - 20, fps, config: theme.spring.heavy });
  return (
    <AbsoluteFill>
      <BgMesh tint={C.steel} />
      <Camera dur={dur} zoom={1.05}>
        <Scene ground={1400} groundCol="#28262a">
          {/* 우산 */}
          <g opacity={up}>
            <path d={`M 180 940 A 360 300 0 0 1 900 940 Z`} fill="#3e4a5c"
              stroke={C.outline} strokeWidth={9} />
            <line x1={540} y1={940} x2={540} y2={1130} stroke="#6c7080" strokeWidth={13} />
            <Sans x={540} y={880} size={56} color="#9ab8d2">안보 우산</Sans>
          </g>
          {/* 기지: 막사 + 철조망 */}
          <rect x={120} y={1230} width={380} height={170} rx={12} fill="#4a5058"
            stroke={C.outline} strokeWidth={7} />
          <path d="M 120 1230 L 310 1130 L 500 1230 Z" fill="#3e444e"
            stroke={C.outline} strokeWidth={7} />
          <Sans x={310} y={1330} size={44} color="#c8ccd8">미군 기지</Sans>
          <line x1={560} y1={1400} x2={1080} y2={1400} stroke="#57503f" strokeWidth={8} />
          {[0, 1, 2, 3].map((k) => (
            <line key={k} x1={600 + k * 130} y1={1400} x2={600 + k * 130} y2={1290}
              stroke="#57503f" strokeWidth={9} />
          ))}
          <path d="M 560 1300 q 130 -40 260 0 q 130 40 260 0" fill="none"
            stroke="#57503f" strokeWidth={7} />
          <Person x={880} y={1430} height={330} outfit="uniform" expr="neutral" hat="helmet"
            pose="stand" facing={-1} />
        </Scene>
      </Camera>
      <Typo top={555} size={86} delay={3}>기존 질서 = 미군</Typo>
    </AbsoluteFill>
  );
};

/* s5 — 우파는 지킨다 */
const S4: React.FC<{ dur: number }> = ({ dur }) => (
  <AbsoluteFill>
    <BgMesh tint={C.amber} />
    <Camera dur={dur} zoom={1.05}>
      <Scene ground={1430} groundCol="#28262a">
        <Flag x={200} y={1430} w={250} color="#3e5a78" h={600} />
        <Person x={560} y={1450} height={460} outfit="suit" expr="smug"
          pose="arms_cross" tie="#983a2e" facing={0} />
        <Sans x={560} y={1500} size={40} color="#c8c4bc">이 세계 일본의 우파</Sans>
      </Scene>
    </Camera>
    <Typo top={555} size={84} delay={2}>지키는 쪽이 우파</Typo>
    <Typo top={720} size={66} color={C.greenText} delay={24}>그래서 좌파가</Typo>
    <Typo top={860} size={66} color={C.greenText} delay={30}>미군을 밀어낸다</Typo>
  </AbsoluteFill>
);

/* s6 — 좌파의 말: 자율 3종 */
const S5: React.FC<{ dur: number }> = () => (
  <AbsoluteFill>
    <BgMesh tint={C.green} />
    <Scene ground={1600} groundCol="#26242a">
      <Skyline y={1600} seed={76} minY={1400} />
    </Scene>
    <Typo top={555} size={92} delay={3}>좌파의 말 = 自律</Typo>
    <div style={{ position: "absolute", top: 760, left: 0, right: 0, display: "flex",
      flexDirection: "column", alignItems: "center", gap: 36 }}>
      {["기지 반대", "주권 회복", "대미 자립"].map((t, i) => (
        <Entrance key={t} delay={12 + i * 8}>
          <Card w={520} outline={i === 2 ? "#4a6a4a" : "#5a6072"}>
            <span style={{ fontSize: 56, color: i === 2 ? C.greenText : C.paper,
              whiteSpace: "nowrap" }}>{t}</span>
          </Card>
        </Entrance>
      ))}
    </div>
  </AbsoluteFill>
);

/* s7 — 자율의 값 = 자주국방 */
const S6: React.FC<{ dur: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const gap = interpolate(frame, [16, 60], [0, 150],
    { easing: theme.ease.inOut, extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <AbsoluteFill>
      <BgMesh tint={C.red} tint2={C.green} />
      <Camera dur={dur} zoom={1.05}>
        <Scene ground={1400} groundCol="#28262a">
          {/* 우산이 걷히고 공백 */}
          <g transform={`translate(${-gap * 2.2},${-gap * 0.7}) rotate(${-gap * 0.06} 300 800)`}>
            <path d={`M 60 900 A 320 270 0 0 1 700 900 Z`} fill="#3e4a5c"
              stroke={C.outline} strokeWidth={9} opacity={0.9} />
          </g>
          <g opacity={Math.min(1, gap / 90)}>
            <circle cx={560} cy={1030} r={150} fill="none" stroke={C.red}
              strokeWidth={11} strokeDasharray="26 18" />
            <Sans x={560} y={1002} size={52} color="#e68c80">공백</Sans>
          </g>
        </Scene>
      </Camera>
      <Typo top={555} size={84} delay={3}>미군이 나가면?</Typo>
      <Entrance delay={40} style={{ position: "absolute", top: 1250, width: "100%",
        textAlign: "center" }}>
        <span style={{ fontFamily: theme.font.serif, fontSize: 88, color: C.yellow,
          textShadow: "0 5px 22px #000" }}>자율의 값 = 자주국방</span>
      </Entrance>
    </AbsoluteFill>
  );
};

/* s8 — 도쿄 평화 집회의 군비 증강 서명 부스 */
const S7: React.FC<{ dur: number }> = ({ dur }) => (
  <AbsoluteFill>
    <BgMesh tint={C.green} tint2={C.red} />
    <Camera dur={dur} zoom={1.05}>
      <Scene ground={1440} groundCol="#26282a">
        <Skyline y={1440} seed={78} minY={920} />
        {/* 부스 */}
        <rect x={300} y={1080} width={480} height={44} fill="#6e6250" stroke={C.outline} strokeWidth={7} />
        <rect x={330} y={1124} width={34} height={320} fill="#57503f" />
        <rect x={716} y={1124} width={34} height={320} fill="#57503f" />
        <rect x={280} y={960} width={520} height={120} rx={12} fill="#e8e2d4"
          stroke={C.outline} strokeWidth={8} />
        <text x={540} y={1012} textAnchor="middle" fontFamily={theme.font.sans}
          fontSize={40} fill={C.ink}>反戰 서명 · 再武裝 서명</text>
        <text x={540} y={1058} textAnchor="middle" fontFamily={theme.font.sans}
          fontSize={34} fill={C.red}>같은 부스입니다</text>
        <Person x={410} y={1470} height={360} outfit="student" expr="smile"
          pose="reach_r" tie="#3e5a78" facing={1} />
        <Person x={690} y={1470} height={370} outfit="worker" expr="smile" hat="cap"
          pose="reach_l" facing={-1} />
        <Picket x={150} top={780} w={260} h={150} poleTo={1200}>
          <text x={150} y={870} textAnchor="middle" fontFamily={theme.font.sans}
            fontSize={44} fill="#3e6a4a">反戰</text>
        </Picket>
        <Picket x={935} top={780} w={280} h={150} poleTo={1200}>
          <text x={935} y={870} textAnchor="middle" fontFamily={theme.font.sans}
            fontSize={44} fill={C.red}>再武裝</text>
        </Picket>
      </Scene>
    </Camera>
    <Typo top={555} size={80} delay={3}>도쿄 평화 집회</Typo>
  </AbsoluteFill>
);

/* s9 — Payoff: 원칙 같음, 질서 다름 → 결론 뒤집힘 */
const S8: React.FC<{ dur: number }> = () => (
  <AbsoluteFill>
    <BgMesh />
    <Scene ground={1600} groundCol="#26242a">
      <Skyline y={1600} seed={79} minY={1400} />
    </Scene>
    <Typo top={555} size={80} delay={3}>좌파가 변한 게 아니다</Typo>
    <div style={{ position: "absolute", top: 740, left: 0, right: 0, display: "flex",
      flexDirection: "column", alignItems: "center", gap: 0 }}>
      {[["원칙: 自律", "#5a6072", C.paper], ["질서: 미군이 기존 질서", C.amber, C.amber],
        ["결론: 재무장", C.yellow, C.yellow]].map(([t, oc, tc], i) => (
        <React.Fragment key={t}>
          {i > 0 && (
            <Entrance delay={10 + i * 10} from={16}>
              <svg width={40} height={56}>
                <line x1={20} y1={0} x2={20} y2={36} stroke={C.amber} strokeWidth={9} />
                <polygon points="20,54 4,34 36,34" fill={C.amber} />
              </svg>
            </Entrance>
          )}
          <Entrance delay={8 + i * 10}>
            <Card w={700} outline={oc}>
              <span style={{ fontSize: 50, color: tc, whiteSpace: "nowrap" }}>{t}</span>
            </Card>
          </Entrance>
        </React.Fragment>
      ))}
    </div>
    <Typo top={1330} size={46} delay={44} serif={false} color="#d8d0c2">원칙이 같아도, 질서가 다르면 결론이 뒤집힌다</Typo>
  </AbsoluteFill>
);

/* s10 — 확장: 그럼 친미는 보수일까? */
const S9: React.FC<{ dur: number }> = ({ dur }) => (
  <AbsoluteFill>
    <BgMesh tint={C.yellow} tint2={C.red} />
    <Camera dur={dur} zoom={1.06}>
      <Scene ground={1470} groundCol="#26242a">
        <Person x={540} y={1570} height={360} outfit="student" expr="worried"
          pose="stand" tie="#3e5a78" />
      </Scene>
    </Camera>
    <Typo top={620} size={100} delay={3}>그럼 이 세계의</Typo>
    <Typo top={820} size={130} color={C.yellow} delay={9}>친미는</Typo>
    <Typo top={1060} size={110} delay={15}>보수일까?</Typo>
  </AbsoluteFill>
);

/* s11 — 다음 모순 (하드컷) */
const S10: React.FC<{ dur: number }> = ({ dur }) => (
  <AbsoluteFill>
    <BgMesh tint={C.amber} tint2={C.steel} />
    <Camera dur={dur} zoom={1.06}>
      <Scene ground={1560} groundCol="#26242a" />
    </Camera>
    <Typo top={590} size={86} delay={2}>1950년의 친미는 보수</Typo>
    <Typo top={780} size={86} color={C.yellow} delay={8}>2050년의 친미는 진보</Typo>
    <Typo top={1030} size={112} delay={15}>동시에 존재합니다</Typo>
  </AbsoluteFill>
);

export const EP7_SCENES = [S1, Anchor1946, S3, S4, S5, S6, S7, S8, S9, S10];
void S3Unused;
