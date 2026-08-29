import React from "react";
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { theme } from "../../theme";
import { BgMesh, Camera } from "../../kit/layers";
import { Entrance, Card } from "../../kit/ui";
import { Person } from "../../kit/people";
import { Skyline } from "../../kit/props";
import { Anchor1946, Scene, Sans, Typo } from "../common";

const C = theme.colors;
const PARTIES: [string, string][] = [["국민당", C.amber], ["진보당", "#6ea85c"],
  ["자치연합", "#4a6a90"], ["청년당", "#8a6ab0"], ["미래당", "#4fa8a8"]];

/* s1 — WTF: 5표 배지 + 부러지는 좌우 자 */
const S1: React.FC<{ dur: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const p = spring({ frame: frame - 4, fps, config: theme.spring.bouncy });
  const brk = spring({ frame: frame - 26, fps, config: theme.spring.bouncy });
  return (
    <AbsoluteFill>
      <BgMesh tint={C.amber} tint2={C.red} />
      <Camera dur={dur} zoom={1.05}>
        <Scene ground={1500} groundCol="#26242a">
          <Skyline y={1500} seed={121} minY={1180} />
          {/* 부러지는 좌우 자 */}
          <g transform={`translate(0, ${interpolate(brk, [0, 1], [0, 40])})`}>
            <g transform={`rotate(${interpolate(brk, [0, 1], [0, -13])} 330 1180)`}>
              <rect x={110} y={1160} width={430} height={40} rx={12} fill="#4a6a90"
                stroke={C.outline} strokeWidth={7} />
              <Sans x={200} y={1192} size={34} color="#dce8f4">左</Sans>
            </g>
            <g transform={`rotate(${interpolate(brk, [0, 1], [0, 15])} 750 1180)`}>
              <rect x={540} y={1160} width={430} height={40} rx={12} fill="#8c4634"
                stroke={C.outline} strokeWidth={7} />
              <Sans x={890} y={1192} size={34} color="#f4dcd4">右</Sans>
            </g>
          </g>
          <Person x={540} y={1560} height={340} outfit="student" expr="surprised"
            pose="hands_up" tie="#3e5a78" />
        </Scene>
      </Camera>
      <div style={{ position: "absolute", top: 590, width: "100%", textAlign: "center",
        opacity: p, transform: `scale(${interpolate(p, [0, 1], [0.6, 1])})` }}>
        <div style={{ display: "inline-block", background: "rgba(24,28,40,0.92)",
          border: `10px solid ${C.yellow}`, borderRadius: 30, padding: "24px 64px" }}>
          <span style={{ fontFamily: theme.font.serif, fontSize: 140, color: C.yellow }}>5票</span>
        </div>
      </div>
      <Typo top={900} size={58} delay={22} serif={false} color="#d8d0c2">현실의 좌우 자는 버리고 오세요</Typo>
    </AbsoluteFill>
  );
};

/* s3 — 근거1: 다섯 이슈 투표용지 */
const S3: React.FC<{ dur: number }> = ({ dur }) => {
  const issues: [string, string][] = [["經", "경제"], ["外", "외교"], ["福", "복지"],
    ["地", "지역"], ["技", "기술"]];
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return (
    <AbsoluteFill>
      <BgMesh tint={C.amber} />
      <Camera dur={dur} zoom={1.05}>
        <Scene ground={1620} groundCol="#26242a">
          {/* 투표용지 */}
          <rect x={190} y={640} width={700} height={880} rx={12} fill="#e8e2d4"
            stroke={C.outline} strokeWidth={9} />
          <text x={540} y={730} textAnchor="middle" fontFamily={theme.font.sans}
            fontSize={44} fill="#6e6250">投票用紙</text>
          {issues.map(([ch, ko], i) => {
            const y = 800 + i * 132;
            const p = spring({ frame: frame - 6 - i * 6, fps, config: theme.spring.snappy });
            return (
              <g key={ch} opacity={p}>
                <rect x={240} y={y} width={600} height={104} rx={10} fill="#f4efe4"
                  stroke="#b4aa8c" strokeWidth={4} />
                <text x={300} y={y + 72} fontFamily={theme.font.serif} fontSize={58}
                  fill={C.ink}>{ch}</text>
                <text x={390} y={y + 70} fontFamily={theme.font.sans} fontSize={46}
                  fill="#3a352c">{ko}</text>
                <rect x={730} y={y + 26} width={54} height={54} rx={6} fill="none"
                  stroke={C.ink} strokeWidth={5} />
              </g>
            );
          })}
        </Scene>
      </Camera>
      <Typo top={545} size={78} delay={2}>이슈는 다섯</Typo>
    </AbsoluteFill>
  );
};

/* s4 — 미니 페이오프: 두 표만에 벌써 다른 당 */
const S4: React.FC<{ dur: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const p2 = spring({ frame: frame - 26, fps, config: theme.spring.snappy });
  return (
    <AbsoluteFill>
      <BgMesh tint={C.steel} tint2={C.amber} />
      <Camera dur={dur} zoom={1.05}>
        <Scene ground={1560} groundCol="#26242a">
          {/* 두 이슈 카드 → 서로 다른 당으로 화살표 */}
          <g>
            <rect x={130} y={820} width={360} height={150} rx={18} fill="rgba(24,28,40,0.92)"
              stroke={C.amber} strokeWidth={6} />
            <Sans x={310} y={878} size={54} color={C.amber}>經 경제</Sans>
            <rect x={590} y={820} width={360} height={150} rx={18} fill="rgba(24,28,40,0.92)"
              stroke="#4a6a90" strokeWidth={6} />
            <Sans x={770} y={878} size={54} color="#9ab8d2">外 외교</Sans>
          </g>
          <g opacity={p2}>
            <line x1={310} y1={990} x2={310} y2={1120} stroke={C.amber} strokeWidth={11} />
            <polygon points="310,1150 288,1108 332,1108" fill={C.amber} />
            <rect x={150} y={1160} width={320} height={110} rx={14} fill="#5c4a2e"
              stroke={C.outline} strokeWidth={6} />
            <Sans x={310} y={1230} size={44}>국민당</Sans>
            <line x1={770} y1={990} x2={770} y2={1120} stroke="#4a6a90" strokeWidth={11} />
            <polygon points="770,1150 748,1108 792,1108" fill="#4a6a90" />
            <rect x={610} y={1160} width={320} height={110} rx={14} fill="#31465e"
              stroke={C.outline} strokeWidth={6} />
            <Sans x={770} y={1230} size={44}>자치연합</Sans>
          </g>
        </Scene>
      </Camera>
      <Typo top={545} size={72} delay={2}>여기까지 두 표</Typo>
      <Typo top={1400} size={66} color={C.yellow} delay={34}>벌써 다른 당입니다</Typo>
    </AbsoluteFill>
  );
};

/* s5 — 근거2: 복지·지역 선택지 */
const S5: React.FC<{ dur: number }> = () => (
  <AbsoluteFill>
    <BgMesh tint={C.green} tint2={C.steel} />
    <Scene ground={1600} groundCol="#26242a">
      <Skyline y={1600} seed={125} minY={1420} />
    </Scene>
    <Typo top={545} size={78} delay={2}>남은 이슈</Typo>
    <div style={{ position: "absolute", top: 720, left: 0, right: 0, display: "flex",
      flexDirection: "column", alignItems: "center", gap: 30 }}>
      {[["福 복지", "연금은 성역인가 개혁인가"], ["地 지역", "세금은 난징인가 성인가"]]
        .map(([h, t], i) => (
        <Entrance key={h} delay={6 + i * 12}>
          <Card w={780} outline={i ? "#4a6a90" : "#6ea85c"}>
            <div style={{ fontSize: 52, color: i ? "#9ab8d2" : C.greenText }}>{h}</div>
            <div style={{ fontSize: 42, marginTop: 12, whiteSpace: "nowrap" }}>{t}</div>
          </Card>
        </Entrance>
      ))}
    </div>
  </AbsoluteFill>
);

/* s6 — 근거3: 기술 + 세어보세요 */
const S6: React.FC<{ dur: number }> = ({ dur }) => (
  <AbsoluteFill>
    <BgMesh tint={C.steel} tint2={C.green} />
    <Camera dur={dur} zoom={1.05}>
      <Scene ground={1560} groundCol="#26242a">
        <Person x={540} y={1520} height={380} outfit="student" expr="worried"
          pose="stand" tie="#3e5a78" />
      </Scene>
    </Camera>
    <Entrance delay={3} style={{ position: "absolute", top: 560, width: "100%",
      display: "flex", justifyContent: "center" }}>
      <Card w={740} outline="#4fa8a8">
        <div style={{ fontSize: 52, color: "#7fd0d0" }}>技 기술</div>
        <div style={{ fontSize: 42, marginTop: 12, whiteSpace: "nowrap" }}>인공지능은 누가 규제하나</div>
      </Card>
    </Entrance>
    <Typo top={880} size={82} color={C.yellow} delay={24}>다 던졌다면</Typo>
    <Typo top={1030} size={82} color={C.yellow} delay={30}>세어 보세요</Typo>
  </AbsoluteFill>
);

/* s7 — Second Hook: 표가 흩어지고 승자는 연합 */
const S7: React.FC<{ dur: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const counts = [2, 1, 1, 0, 1];
  return (
    <AbsoluteFill>
      <BgMesh tint={C.amber} />
      <Camera dur={dur} zoom={1.04}>
        <Scene ground={1520} groundCol="#26242a">
          {PARTIES.map(([name, col], i) => {
            const x = 150 + i * 195;
            return (
              <g key={name}>
                <rect x={x - 70} y={1180} width={140} height={140} rx={12}
                  fill="rgba(24,28,40,0.9)" stroke={col} strokeWidth={6} />
                <text x={x} y={1370} textAnchor="middle" fontFamily={theme.font.sans}
                  fontSize={30} fill={col} stroke="#000" strokeWidth={4}
                  paintOrder="stroke">{name}</text>
                {Array.from({ length: counts[i] }).map((_, k) => {
                  const p = spring({ frame: frame - 8 - (i * 2 + k) * 6, fps,
                    config: theme.spring.bouncy });
                  return (
                    <g key={k} opacity={p}
                      transform={`translate(0, ${interpolate(p, [0, 1], [-260, 0])})`}>
                      <rect x={x - 44} y={1200 + k * 56} width={88} height={44} rx={8}
                        fill={col} stroke={C.outline} strokeWidth={5} />
                      <text x={x} y={1232 + k * 56} textAnchor="middle"
                        fontFamily={theme.font.sans} fontSize={26} fill="#f2e9dc">票</text>
                    </g>
                  );
                })}
              </g>
            );
          })}
        </Scene>
      </Camera>
      <Typo top={545} size={74} delay={2}>표는 흩어진다</Typo>
      <Typo top={700} size={64} color={C.yellow} delay={34}>승자는 연합입니다</Typo>
    </AbsoluteFill>
  );
};

/* s8 — 본 페이오프: 좌우 축 X → 다섯 이슈 축 */
const S8: React.FC<{ dur: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const swap = spring({ frame: frame - 26, fps, config: theme.spring.heavy });
  return (
    <AbsoluteFill>
      <BgMesh tint={C.steel} tint2={C.amber} />
      <Camera dur={dur} zoom={1.05}>
        <Scene ground={1560} groundCol="#26242a">
          {/* 좌우 가로축 (사라짐) */}
          <g opacity={1 - swap}>
            <line x1={140} y1={1100} x2={940} y2={1100} stroke="#787c8a" strokeWidth={16} />
            <line x1={380} y1={1020} x2={700} y2={1180} stroke={C.red} strokeWidth={14} strokeLinecap="round" />
            <line x1={700} y1={1020} x2={380} y2={1180} stroke={C.red} strokeWidth={14} strokeLinecap="round" />
          </g>
          {/* 다섯 이슈 세로축 */}
          <g opacity={swap}>
            {["經", "外", "福", "地", "技"].map((ch, i) => {
              const x = 190 + i * 175;
              return (
                <g key={ch}>
                  <line x1={x} y1={1300} x2={x} y2={900} stroke={C.amber} strokeWidth={10} />
                  <circle cx={x} cy={880} r={40} fill="#5c4a2e" stroke={C.outline} strokeWidth={6} />
                  <text x={x} y={896} textAnchor="middle" fontFamily={theme.font.serif}
                    fontSize={40} fill={C.yellow}>{ch}</text>
                </g>
              );
            })}
          </g>
        </Scene>
      </Camera>
      <Typo top={545} size={70} delay={2}>134년의 다른 역사</Typo>
      <Typo top={1400} size={60} color={C.yellow} delay={34}>좌우는 이 판의 축이 아니었다</Typo>
    </AbsoluteFill>
  );
};

/* s9 — 확장: 시즌 결산 스트립 */
const S9: React.FC<{ dur: number }> = () => (
  <AbsoluteFill>
    <BgMesh />
    <Scene ground={1600} groundCol="#26242a">
      <Skyline y={1600} seed={129} minY={1440} />
    </Scene>
    <Typo top={545} size={72} delay={2}>시즌 내내 실패한 이유</Typo>
    <div style={{ position: "absolute", top: 720, left: 0, right: 0, display: "flex",
      flexDirection: "column", alignItems: "center", gap: 18 }}>
      {[["EP2", "복지 = 보수"], ["EP3", "민영화 = 진보"], ["EP5", "반중 = 진보"],
        ["EP9", "영토 = 회계"], ["EP10", "세대 = 위치"]].map(([ep, t], i) => (
        <Entrance key={ep} delay={4 + i * 6}>
          <div style={{ display: "flex", alignItems: "center", gap: 22,
            background: "rgba(24,28,40,0.88)", border: "5px solid #5a6072",
            borderRadius: 16, padding: "14px 34px" }}>
            <span style={{ fontFamily: theme.font.sans, fontSize: 34, color: C.amber }}>{ep}</span>
            <span style={{ fontFamily: theme.font.sans, fontSize: 44, color: C.paper,
              whiteSpace: "nowrap" }}>{t}</span>
          </div>
        </Entrance>
      ))}
    </div>
  </AbsoluteFill>
);

/* s10 — 시즌2 예고: 질문만 남긴다 (정본 §13) */
const S10: React.FC<{ dur: number }> = ({ dur }) => (
  <AbsoluteFill>
    <BgMesh tint={C.yellow} tint2={C.steel} />
    <Camera dur={dur} zoom={1.06}>
      <Scene ground={1560} groundCol="#26242a" />
    </Camera>
    <Typo top={600} size={80} delay={2}>왜 우리는 자꾸</Typo>
    <Typo top={780} size={110} color={C.yellow} delay={8}>한 줄로 세우려</Typo>
    <Typo top={960} size={110} color={C.yellow} delay={12}>했을까?</Typo>
    <Entrance delay={26} style={{ position: "absolute", top: 1200, width: "100%",
      display: "flex", justifyContent: "center" }}>
      <Card w={720} outline={C.amber}>
        <span style={{ fontSize: 46, color: C.amber, whiteSpace: "nowrap" }}>
          시즌 2 「자유중국의 철학」</span></Card>
    </Entrance>
  </AbsoluteFill>
);

export const EP12_SCENES = [S1, Anchor1946, S3, S4, S5, S6, S7, S8, S9, S10];
