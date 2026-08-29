import React from "react";
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { theme } from "../../theme";
import { BgMesh, Camera } from "../../kit/layers";
import { Entrance, Stamp, Card } from "../../kit/ui";
import { Person } from "../../kit/people";
import { Skyline, Ship, Crane, Containers, Flag, Picket, Smoke } from "../../kit/props";
import { Anchor1946, Scene, Sans, Typo, GROUND } from "../common";

const C = theme.colors;

/* s1 — WTF: 진보의 반중 시위 + 反中 스탬프 */
const S1: React.FC<{ dur: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const p1 = spring({ frame: frame - 2, fps, config: theme.spring.smooth });
  return (
    <AbsoluteFill>
      <BgMesh tint={C.green} tint2={C.red} />
      <Camera dur={dur} zoom={1.05}>
        <Scene ground={1400} groundCol="#26282a">
          <Skyline y={1400} seed={51} minY={880} />
          <g opacity={p1}>
            <Picket x={340} top={880} w={430} h={190} poleTo={1240}>
              <text x={340} y={955} textAnchor="middle" fontFamily={theme.font.sans}
                fontSize={46} fill={C.ink}>중국 자본을</text>
              <text x={340} y={1022} textAnchor="middle" fontFamily={theme.font.sans}
                fontSize={52} fill={C.red}>막아라</text>
            </Picket>
            <Person x={340} y={1450} height={420} outfit="worker" expr="shout" hat="cap"
              pose="hold_sign" facing={0} />
            <Person x={790} y={1450} height={440} outfit="suit_r" expr="shout"
              pose="hands_up" facing={0} waveArm />
            <Sans x={790} y={1210} size={40} color="#a4d29a">진보당</Sans>
          </g>
        </Scene>
      </Camera>
      <Entrance delay={4} from={-30} style={{ position: "absolute", top: 528, width: "100%",
        textAlign: "center" }}>
        <span style={{ fontFamily: theme.font.sans, fontSize: 54, color: C.paper,
          textShadow: "0 4px 16px #000" }}>이 구호를 외치는 쪽은</span>
      </Entrance>
      <div style={{ position: "absolute", top: 640, width: "100%",
        display: "flex", justifyContent: "center" }}>
        <Stamp text="反中" delay={14} size={380} textColor={C.yellow} />
      </div>
    </AbsoluteFill>
  );
};

/* s3 — 근거1: 항만 매입 / 공장 유출 */
const S3: React.FC<{ dur: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const fx = interpolate(frame, [20, dur], [0, 260],
    { easing: theme.ease.inOut, extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <AbsoluteFill>
      <BgMesh tint={C.red} tint2={C.steel} />
      <Camera dur={dur} zoom={1.045}>
        <Scene>
          <Ship x={250} y={1060} scale={0.62} />
          <rect x={0} y={1150} width={1080} height={770} fill={GROUND} />
          <rect x={0} y={1142} width={1080} height={16} fill="#3f434f" />
          <Crane x={205} y={1142} dir={1} scale={0.66} />
          <Containers x={330} y={1142} />
          {/* 공장이 오른쪽으로 밀려나감 */}
          <g transform={`translate(${fx},0)`} opacity={interpolate(fx, [0, 260], [1, 0.55])}>
            <g transform="translate(640,1330)">
              <rect x={0} y={0} width={330} height={190} fill="#4a4436" stroke={C.outline} strokeWidth={7} />
              {[0, 1, 2].map((k) => (
                <polygon key={k} points={`${k * 110},0 ${k * 110 + 55},-64 ${k * 110 + 110},0`}
                  fill="#5a5244" stroke={C.outline} strokeWidth={6} />
              ))}
              <rect x={250} y={-150} width={34} height={90} fill="#57503f" stroke={C.outline} strokeWidth={5} />
              <rect x={40} y={70} width={70} height={70} fill="#786848" />
              <rect x={150} y={70} width={70} height={70} fill="#786848" />
            </g>
            <Smoke x={905} y={1170} scale={0.7} />
          </g>
          <Sans x={250} y={1610} size={46} color="#e68c80">中資가 사들이고</Sans>
          <Sans x={790} y={1610} size={46} color="#9a9eaa">공장은 떠난다</Sans>
        </Scene>
      </Camera>
      <Entrance delay={6} style={{ position: "absolute", top: 555, width: "100%",
        textAlign: "center" }}>
        <span style={{ fontFamily: theme.font.serif, fontSize: 88, color: C.paper,
          textShadow: "0 5px 22px #000" }}>통합의 청구서</span>
      </Entrance>
    </AbsoluteFill>
  );
};

/* s4 — 미니 페이오프: 시소 + '반대하는 쪽이 진보' */
const S4: React.FC<{ dur: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const tilt = interpolate(spring({ frame: frame - 14, fps, config: theme.spring.heavy }),
    [0, 1], [0, 11]);
  return (
    <AbsoluteFill>
      <BgMesh tint={C.amber} tint2={C.red} />
      <Camera dur={dur} zoom={1.05}>
        <Scene ground={1520} groundCol="#28262a">
          <g transform={`rotate(${-tilt} 540 1300)`}>
            <rect x={100} y={1286} width={880} height={26} rx={12} fill="#6e6250"
              stroke={C.outline} strokeWidth={7} />
            <g transform={`rotate(${tilt} 280 1286)`}>
              <Person x={280} y={1292} height={400} outfit="suit" expr="smug"
                pose="hold_case" tie="#983a2e" />
            </g>
            <g transform={`rotate(${tilt} 800 1286)`}>
              <Person x={800} y={1292} height={400} outfit="worker" expr="worried" hat="cap"
                pose="stand" />
            </g>
          </g>
          <polygon points="540,1312 470,1520 610,1520" fill="#57503f" stroke={C.outline} strokeWidth={7} />
          <Sans x={180} y={1000} size={52} color={C.amber}>수혜 → 재계</Sans>
          <Sans x={880} y={1210} size={52} color="#e68c80">청구서 → 노동</Sans>
        </Scene>
      </Camera>
      <Typo top={545} size={80} delay={2}>기울어진 통합</Typo>
      {/* 미니 페이오프 — 훅 질문에 대한 짧은 답 */}
      <Entrance delay={30} style={{ position: "absolute", top: 690, width: "100%",
        textAlign: "center" }}>
        <span style={{ fontFamily: theme.font.serif, fontSize: 70, color: C.greenText,
          textShadow: "0 5px 22px #000" }}>반대하는 쪽이 진보</span>
      </Entrance>
    </AbsoluteFill>
  );
};

/* s5 — 근거2: 문 닫은 조선소, 박성호 */
const S5: React.FC<{ dur: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const shut = interpolate(frame, [18, 44], [0, 1],
    { easing: theme.ease.out, extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <AbsoluteFill>
      <BgMesh tint={C.steel} tint2={C.red} />
      <Camera dur={dur} zoom={1.05}>
        <Scene ground={1420} groundCol="#28262a">
          {/* 조선소 게이트 */}
          <rect x={130} y={760} width={820} height={40} fill="#57503f"
            stroke={C.outline} strokeWidth={7} />
          <rect x={150} y={800} width={44} height={620} fill="#4a4436"
            stroke={C.outline} strokeWidth={6} />
          <rect x={886} y={800} width={44} height={620} fill="#4a4436"
            stroke={C.outline} strokeWidth={6} />
          <Crane x={700} y={1420} dir={-1} scale={0.62} />
          {/* 닫히는 문 */}
          <g>
            <rect x={194 - 350 * (1 - shut)} y={860} width={346} height={560}
              fill="#3e444e" stroke={C.outline} strokeWidth={7} />
            <rect x={540 + 346 * (1 - shut)} y={860} width={346} height={560}
              fill="#3e444e" stroke={C.outline} strokeWidth={7} />
          </g>
          {/* 폐쇄 안내문 */}
          <g opacity={shut} transform="rotate(-4 540 1120)">
            <rect x={380} y={1050} width={320} height={140} rx={10} fill="#e8e2d4"
              stroke={C.outline} strokeWidth={7} />
            <text x={540} y={1112} textAnchor="middle" fontFamily={theme.font.sans}
              fontSize={46} fill={C.red}>조업 중단</text>
            <text x={540} y={1160} textAnchor="middle" fontFamily={theme.font.sans}
              fontSize={30} fill="#6e6250">인천 조선소</text>
          </g>
          <Person x={300} y={1620} height={420} outfit="worker" expr="worried" hat="cap"
            pose="stand" facing={1} />
        </Scene>
      </Camera>
      <Typo top={555} size={80} delay={2}>청구서를 받은 사람</Typo>
      <Entrance delay={26} style={{ position: "absolute", top: 1640, width: "100%",
        display: "flex", justifyContent: "center" }}>
        <div style={{ background: "#0d0b0a", borderRadius: 14, padding: "14px 30px",
          fontFamily: theme.font.sans, fontSize: 38, color: C.paper }}>
          박성호 (52) · 인천 조선소 용접공</div>
      </Entrance>
    </AbsoluteFill>
  );
};

/* s6 — 네 가지 말 (2×2 카드) */
const S6: React.FC<{ dur: number }> = () => {
  const items = [["産", "산업주권"], ["勞", "노동"], ["文", "문화자율"], ["外", "외교다변화"]];
  return (
    <AbsoluteFill>
      <BgMesh />
      <Scene ground={1600} groundCol="#26242a">
        <Skyline y={1600} seed={56} minY={1400} />
      </Scene>
      <div style={{ position: "absolute", top: 590, left: 90, right: 90, display: "grid",
        gridTemplateColumns: "1fr 1fr", gap: 40 }}>
        {items.map(([ch, lab], i) => (
          <Entrance key={ch} delay={6 + i * 7}>
            <Card outline={i % 3 === 0 ? C.amber : "#5a6072"} style={{ padding: "40px 20px" }}>
              <div style={{ fontFamily: theme.font.serif, fontSize: 120, color: C.amber }}>{ch}</div>
              <div style={{ fontSize: 52, marginTop: 16 }}>{lab}</div>
            </Card>
          </Entrance>
        ))}
      </div>
    </AbsoluteFill>
  );
};

/* (미사용) 등식 씬 — v2.0에서 미니 페이오프로 대체 */
const S7Unused: React.FC<{ dur: number }> = ({ dur }) => (
  <AbsoluteFill>
    <BgMesh tint={C.green} />
    <Camera dur={dur} zoom={1.055}>
      <Scene ground={1470} groundCol="#26242a">
        <Person x={540} y={1560} height={380} outfit="worker" expr="shout" hat="cap"
          pose="hands_up" waveArm />
      </Scene>
    </Camera>
    <Typo top={600} size={104} delay={3}>기존 질서와</Typo>
    <Typo top={790} size={116} delay={9}>싸우는 쪽</Typo>
    <Typo top={1020} size={160} color={C.greenText} delay={16}>= 진보</Typo>
  </AbsoluteFill>
);

/* s8 — 뒤집힌 장면: 노조 깃발 主權 / 재계 사설 開放 */
const S7: React.FC<{ dur: number }> = ({ dur }) => (
  <AbsoluteFill>
    <BgMesh tint={C.steel} tint2={C.green} />
    <Camera dur={dur} zoom={1.05}>
      <Scene ground={1430} groundCol="#28262a">
        <Flag x={175} y={1430} w={270} color="#4a6a4a" h={620} />
        <Sans x={330} y={905} size={72} color={C.paper}>主權</Sans>
        <Person x={300} y={1450} height={400} outfit="worker" expr="shout" hat="cap"
          pose="hands_up" />
      </Scene>
    </Camera>
    <Entrance delay={14} style={{ position: "absolute", top: 700, right: 90, width: 420 }}>
      <div style={{ background: "#e8e2d4", border: `7px solid ${C.outline}`, borderRadius: 8,
        transform: "rotate(3deg)", padding: "26px 24px", textAlign: "center",
        boxShadow: "0 24px 60px -18px rgba(0,0,0,0.65)" }}>
        <div style={{ fontFamily: theme.font.sans, fontSize: 38, color: "#6e6250",
          borderBottom: "3px solid #6e6250", paddingBottom: 10 }}>自由日報 · 사설</div>
        <div style={{ fontFamily: theme.font.serif, fontSize: 120, color: C.ink,
          marginTop: 18 }}>開放</div>
        <div style={{ fontFamily: theme.font.sans, fontSize: 34, color: "#4a443a",
          marginTop: 10 }}>재계는 개방을 원한다</div>
      </div>
    </Entrance>
    <Typo top={555} size={80} delay={3}>뒤집힌 장면</Typo>
  </AbsoluteFill>
);

/* s9 — Payoff: 지킨다=보수 / 저항한다=진보 */
const S8: React.FC<{ dur: number }> = () => (
  <AbsoluteFill>
    <BgMesh tint={C.amber} tint2={C.green} />
    <Scene ground={1560} groundCol="#26242a">
      <Skyline y={1560} seed={59} minY={1360} />
    </Scene>
    <Typo top={555} size={82} delay={3}>反中은 유전자가 아니다</Typo>
    <div style={{ position: "absolute", top: 760, left: 0, right: 0, display: "flex",
      justifyContent: "center", gap: 60 }}>
      <Entrance delay={14}>
        <div style={{ textAlign: "center" }}>
          <svg width={280} height={330}>
            <Person x={140} y={320} height={300} outfit="suit" expr="smug" tie="#983a2e"
              pose="hold_case" />
          </svg>
          <Card w={430} outline={C.amber}><span style={{ fontSize: 44, color: C.yellow,
            whiteSpace: "nowrap" }}>지킨다 = 보수</span></Card>
        </div>
      </Entrance>
      <Entrance delay={20}>
        <div style={{ textAlign: "center" }}>
          <svg width={280} height={330}>
            <Person x={140} y={320} height={300} outfit="worker" expr="shout" hat="cap"
              pose="hands_up" />
          </svg>
          <Card w={460} outline="#4a6a4a"><span style={{ fontSize: 44, color: C.greenText,
            whiteSpace: "nowrap" }}>저항한다 = 진보</span></Card>
        </div>
      </Entrance>
    </div>
    <Typo top={1310} size={44} delay={40} serif={false} color="#d8d0c2">무엇에 의존하는지가, 누가 저항하는지를 정한다</Typo>
  </AbsoluteFill>
);

/* s10 — 정당은 싸우고, 청년은 떠난다 */
const S9: React.FC<{ dur: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const walk = interpolate(frame, [10, dur], [0, 240],
    { easing: theme.ease.inOut, extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <AbsoluteFill>
      <BgMesh tint={C.red} tint2={C.steel} />
      <Camera dur={dur} zoom={1.045}>
        <Scene ground={1430} groundCol="#26242a">
          <Person x={250} y={1450} height={400} outfit="suit_r" expr="shout"
            pose="point_r" facing={1} />
          <Person x={560} y={1450} height={400} outfit="suit_b" expr="shout"
            pose="point_l" facing={-1} tie="#3e5a78" />
          <g transform={`translate(${walk},0)`}>
            <Person x={800} y={1460} height={380} outfit="student" expr="closed"
              pose="hold_case" tie="#3e5a78" facing={1} />
          </g>
          <Sans x={250} y={940} size={52} color="#e68c80">막아라!</Sans>
          <Sans x={560} y={940} size={52} color="#9ab8d2">열어라!</Sans>
        </Scene>
      </Camera>
      <Typo top={555} size={82} delay={3}>정당은 싸우고</Typo>
      <Typo top={700} size={72} color={C.yellow} delay={20}>청년은 떠난다</Typo>
    </AbsoluteFill>
  );
};

/* s11 — 다음 모순: 중국 유학 (하드컷) */
const S10: React.FC<{ dur: number }> = ({ dur }) => (
  <AbsoluteFill>
    <BgMesh tint={C.yellow} tint2={C.steel} />
    <Camera dur={dur} zoom={1.06}>
      <Scene ground={1520} groundCol="#26242a">
        <Person x={860} y={1560} height={360} outfit="student" expr="smile"
          pose="hold_case" tie="#3e5a78" facing={1} />
      </Scene>
    </Camera>
    <Typo top={560} size={84} delay={2}>이 세계의 대학생에겐</Typo>
    <Typo top={740} size={136} color={C.yellow} delay={7}>중국 유학이</Typo>
    <Typo top={980} size={112} delay={13}>미국 유학만큼</Typo>
    <Typo top={1180} size={104} delay={18}>자연스럽다</Typo>
  </AbsoluteFill>
);

export const EP5_SCENES = [S1, Anchor1946, S3, S4, S5, S6, S7, S8, S9, S10];
void S7Unused;
