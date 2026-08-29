import React from "react";
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { theme } from "../../theme";
import { BgMesh, Camera } from "../../kit/layers";
import { Entrance, Card } from "../../kit/ui";
import { Person } from "../../kit/people";
import { Skyline, Flag } from "../../kit/props";
import { Anchor1946, Scene, Sans, Typo } from "../common";

const C = theme.colors;

/* s1 — WTF: 1950 보수 / 2050 진보, 같은 성조기 방향 */
const S1: React.FC<{ dur: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const p1 = spring({ frame: frame - 4, fps, config: theme.spring.smooth });
  const p2 = spring({ frame: frame - 22, fps, config: theme.spring.smooth });
  return (
    <AbsoluteFill>
      <BgMesh tint={C.amber} tint2={C.steel} />
      <Camera dur={dur} zoom={1.05}>
        <Scene ground={1430} groundCol="#28262a">
          <g opacity={p1}>
            <rect x={90} y={600} width={430} height={130} rx={18} fill="rgba(24,28,40,0.9)"
              stroke={C.amber} strokeWidth={6} />
            <Sans x={305} y={648} size={54} color={C.amber}>1950 · 보수</Sans>
            <Person x={250} y={1450} height={430} outfit="suit" expr="neutral"
              pose="point_r" tie="#983a2e" facing={1} />
          </g>
          <g opacity={p2}>
            <rect x={560} y={600} width={430} height={130} rx={18} fill="rgba(24,28,40,0.9)"
              stroke="#4a6a4a" strokeWidth={6} />
            <Sans x={775} y={648} size={54} color={C.greenText}>2050 · 진보</Sans>
            <Person x={830} y={1450} height={430} outfit="worker" expr="shout" hat="cap"
              pose="point_r" facing={1} />
          </g>
          {/* 둘 다 같은 곳(친미)을 가리킴 */}
          <g opacity={Math.min(p1, 1)}>
            <circle cx={540} cy={905} r={92} fill="rgba(62,90,120,0.4)"
              stroke="#9ab8d2" strokeWidth={7} />
            <Sans x={540} y={880} size={58} color="#c8dcee">親美</Sans>
          </g>
        </Scene>
      </Camera>
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
    <Typo top={620} size={94} delay={3}>같은 친미가</Typo>
    <Typo top={850} size={110} color={C.yellow} delay={10}>왜 자리를 옮겼나</Typo>
  </AbsoluteFill>
);

/* s4 — 1950: 미국 = 반공 질서의 축 */
const S3: React.FC<{ dur: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const spin = interpolate(frame, [0, dur], [0, 26]);
  const p = spring({ frame: frame - 10, fps, config: theme.spring.heavy });
  return (
    <AbsoluteFill>
      <BgMesh tint={C.steel} />
      <Camera dur={dur} zoom={1.05}>
        <Scene ground={1460} groundCol="#28262a">
          {/* 축(허브) + 위성 */}
          <g opacity={p}>
            <circle cx={540} cy={1000} r={140} fill="#3e4a5c" stroke={C.outline} strokeWidth={9} />
            <Sans x={540} y={975} size={64} color="#c8dcee">美</Sans>
            <Sans x={540} y={1055} size={38} color="#9ab8d2">반공 질서의 축</Sans>
            <g transform={`rotate(${spin} 540 1000)`}>
              {[0, 1, 2, 3].map((k) => {
                const a = (Math.PI * 2 * k) / 4 + 0.6;
                const x = 540 + Math.cos(a) * 300, y = 1000 + Math.sin(a) * 300;
                return (
                  <g key={k}>
                    <line x1={540} y1={1000} x2={x} y2={y} stroke="#57606f" strokeWidth={7} />
                    <circle cx={x} cy={y} r={46} fill="#4a5058" stroke={C.outline} strokeWidth={7} />
                  </g>
                );
              })}
            </g>
          </g>
          <Person x={220} y={1490} height={370} outfit="suit" expr="smug"
            pose="point_r" tie="#983a2e" facing={1} />
          <Sans x={220} y={1540} size={38} color="#c8c4bc">1950의 보수</Sans>
        </Scene>
      </Camera>
      <Typo top={555} size={90} delay={3}>1950 · 축은 미국</Typo>
    </AbsoluteFill>
  );
};

/* s5 — 그때의 반미 = 급진 */
const S4: React.FC<{ dur: number }> = ({ dur }) => (
  <AbsoluteFill>
    <BgMesh tint={C.red} />
    <Camera dur={dur} zoom={1.055}>
      <Scene ground={1450} groundCol="#28262a">
        <Person x={540} y={1470} height={430} outfit="worker" expr="shout" hat="cap"
          pose="hands_up" facing={0} waveArm />
      </Scene>
    </Camera>
    <Typo top={555} size={92} delay={2}>그때의 반미는 급진</Typo>
    <Typo top={730} size={72} color={C.yellow} delay={22}>축이 어디냐가</Typo>
    <Typo top={880} size={72} color={C.yellow} delay={28}>이름을 정한다</Typo>
  </AbsoluteFill>
);

/* s6 — 축의 이동: 미국 → 자유중국 */
const S5: React.FC<{ dur: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const shift = spring({ frame: frame - 30, fps, config: theme.spring.heavy });
  return (
    <AbsoluteFill>
      <BgMesh tint={C.amber} tint2={C.steel} />
      <Camera dur={dur} zoom={1.05}>
        <Scene ground={1520} groundCol="#26242a">
          {/* 왼쪽: 美 (줄어듦) / 오른쪽: 自由中國 (커짐) */}
          <g opacity={interpolate(shift, [0, 1], [1, 0.45])}
            transform={`scale(${interpolate(shift, [0, 1], [1, 0.72])})`}
            style={{ transformOrigin: "260px 1000px" }}>
            <circle cx={260} cy={1000} r={130} fill="#3e4a5c" stroke={C.outline} strokeWidth={9} />
            <Sans x={260} y={1028} size={64} color="#9ab8d2">美</Sans>
          </g>
          <g transform={`scale(${interpolate(shift, [0, 1], [0.7, 1.12])})`}
            style={{ transformOrigin: "760px 1000px" }}>
            <circle cx={760} cy={1000} r={170} fill="#5c4a2e" stroke={C.outline} strokeWidth={9} />
            <Sans x={760} y={985} size={58} color={C.amber}>自由中國</Sans>
            <Sans x={760} y={1058} size={36} color="#ecc478">동아시아의 기존 질서</Sans>
          </g>
          <g opacity={shift}>
            <line x1={400} y1={1000} x2={545} y2={1000} stroke={C.amber} strokeWidth={13} />
            <polygon points="575,1000 533,978 533,1022" fill={C.amber} />
          </g>
        </Scene>
      </Camera>
      <Typo top={555} size={88} delay={3}>축이 옮겨간다</Typo>
    </AbsoluteFill>
  );
};

/* s7 — 미국 = 균형추, 개혁의 지렛대 */
const S6: React.FC<{ dur: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const tilt = interpolate(spring({ frame: frame - 24, fps, config: theme.spring.heavy }),
    [0, 1], [8, -7]);
  return (
    <AbsoluteFill>
      <BgMesh tint={C.green} tint2={C.steel} />
      <Camera dur={dur} zoom={1.05}>
        <Scene ground={1520} groundCol="#28262a">
          {/* 지렛대 */}
          <g transform={`rotate(${tilt} 540 1240)`}>
            <rect x={120} y={1226} width={840} height={26} rx={12} fill="#6e6250"
              stroke={C.outline} strokeWidth={7} />
            <circle cx={260} cy={1180} r={72} fill="#3e4a5c" stroke={C.outline} strokeWidth={8} />
            <Sans x={260} y={1202} size={48} color="#9ab8d2">美</Sans>
            <circle cx={850} cy={1180} r={95} fill="#5c4a2e" stroke={C.outline} strokeWidth={8} />
            <Sans x={850} y={1200} size={40} color={C.amber}>기존 질서</Sans>
          </g>
          <polygon points="540,1250 470,1450 610,1450" fill="#57503f"
            stroke={C.outline} strokeWidth={7} />
        </Scene>
      </Camera>
      <Typo top={560} size={88} delay={3}>미국 = 균형추</Typo>
      <Typo top={730} size={62} color={C.greenText} delay={14} serif={false}>도전하는 쪽의 지렛대</Typo>
    </AbsoluteFill>
  );
};

/* s8 — 2050 집회: 한 깃발에 세 단어, 색은 진보 */
const S7: React.FC<{ dur: number }> = ({ dur }) => (
  <AbsoluteFill>
    <BgMesh tint={C.green} />
    <Camera dur={dur} zoom={1.05}>
      <Scene ground={1450} groundCol="#26282a">
        <Skyline y={1450} seed={88} minY={940} />
        <Flag x={230} y={1450} w={330} color="#4a6a4a" h={700} />
        <text x={420} y={830} textAnchor="middle" fontFamily={theme.font.sans}
          fontSize={40} fill="#dcecd8">자유무역 · 미국 · 개혁</text>
        <Person x={330} y={1480} height={400} outfit="worker" expr="shout" hat="cap"
          pose="hands_up" waveArm />
        <Person x={640} y={1480} height={380} outfit="student" expr="shout"
          pose="hands_up" tie="#3e5a78" />
        <Sans x={850} y={1180} size={44} color={C.greenText}>깃발의 색은 진보</Sans>
      </Scene>
    </Camera>
    <Typo top={555} size={82} delay={3}>2050년의 집회</Typo>
  </AbsoluteFill>
);

/* s9 — Payoff */
const S8: React.FC<{ dur: number }> = () => (
  <AbsoluteFill>
    <BgMesh tint={C.amber} />
    <Scene ground={1600} groundCol="#26242a">
      <Skyline y={1600} seed={89} minY={1400} />
    </Scene>
    <Typo top={555} size={86} delay={3}>친미는 이념이 아니다</Typo>
    <div style={{ position: "absolute", top: 760, left: 0, right: 0, display: "flex",
      flexDirection: "column", alignItems: "center", gap: 0 }}>
      {[["미국이 변한 게 아니라", "#5a6072", C.paper],
        ["질서의 중심이 이동", C.amber, C.amber],
        ["같은 방향 = 반대편", C.yellow, C.yellow]].map(([t, oc, tc], i) => (
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
            <Card w={680} outline={oc}>
              <span style={{ fontSize: 50, color: tc, whiteSpace: "nowrap" }}>{t}</span>
            </Card>
          </Entrance>
        </React.Fragment>
      ))}
    </div>
    <Typo top={1330} size={46} delay={44} serif={false} color="#d8d0c2">축이 움직이면, 같은 방향도 반대편이 된다</Typo>
  </AbsoluteFill>
);

/* s10 — 확장: 낯설게 받는 곳 (대만 예고) */
const S9: React.FC<{ dur: number }> = ({ dur }) => (
  <AbsoluteFill>
    <BgMesh tint={C.red} tint2={C.steel} />
    <Camera dur={dur} zoom={1.06}>
      <Scene ground={1500} groundCol="#26242a">
        <ellipse cx={540} cy={1150} rx={190} ry={95} fill="#4a5058"
          stroke={C.outline} strokeWidth={8} transform="rotate(-35 540 1150)" />
        <text x={540} y={1165} textAnchor="middle" fontFamily={theme.font.sans}
          fontSize={46} fill={C.paper} stroke="#000" strokeWidth={5}
          paintOrder="stroke">臺灣</text>
        <circle cx={540} cy={1150} r={250} fill="none" stroke={C.yellow}
          strokeWidth={9} strokeDasharray="30 22" />
      </Scene>
    </Camera>
    <Typo top={590} size={88} delay={3}>이 질문이 가장</Typo>
    <Typo top={770} size={100} color={C.yellow} delay={10}>낯선 곳</Typo>
  </AbsoluteFill>
);

/* s11 — 다음 모순 (하드컷) */
const S10: React.FC<{ dur: number }> = ({ dur }) => (
  <AbsoluteFill>
    <BgMesh tint={C.yellow} tint2={C.steel} />
    <Camera dur={dur} zoom={1.06}>
      <Scene ground={1560} groundCol="#26242a" />
    </Camera>
    <Typo top={600} size={88} delay={2}>이 세계 대만 선거의</Typo>
    <Typo top={790} size={110} delay={8}>최대 쟁점은</Typo>
    <Typo top={1030} size={130} color={C.yellow} delay={14}>독립이 아니다</Typo>
  </AbsoluteFill>
);

export const EP8_SCENES = [S1, Anchor1946, S3, S4, S5, S6, S7, S8, S9, S10];
void S3Unused;
