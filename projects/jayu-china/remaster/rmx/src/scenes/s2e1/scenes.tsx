import React from "react";
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { theme } from "../../theme";
import { BgMesh, Camera } from "../../kit/layers";
import { Entrance, Card, Stamp } from "../../kit/ui";
import { Person } from "../../kit/people";
import { Skyline, Flag, Smoke } from "../../kit/props";
import { DecompressBox } from "../../kit/decompress";
import { Anchor1946, Scene, Sans, Typo } from "../common";

const C = theme.colors;

/** 책 — 시즌2의 반복 소품. */
const Book: React.FC<{ x: number; y: number; s?: number; title?: string;
  col?: string; rot?: number }> = ({ x, y, s = 1, title = "資本", col = "#8c3a2e", rot = 0 }) => (
  <g transform={`translate(${x},${y}) rotate(${rot}) scale(${s})`}>
    <rect x={-90} y={-120} width={180} height={240} rx={8} fill={col}
      stroke={C.outline} strokeWidth={8} />
    <rect x={-90} y={-120} width={26} height={240} fill="#5e2820" stroke={C.outline} strokeWidth={6} />
    <rect x={-40} y={-84} width={110} height={64} rx={5} fill="none"
      stroke="#e0d4c0" strokeWidth={4} />
    <text x={15} y={-38} textAnchor="middle" fontFamily={theme.font.serif}
      fontSize={44} fill="#e8dcc8">{title}</text>
  </g>
);

/* s1 — WTF: 무너진 깃발 옆, 강의실 책상 위의 책 */
const S1: React.FC<{ dur: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const fall = spring({ frame: frame - 2, fps, config: theme.spring.heavy });
  const rise = spring({ frame: frame - 14, fps, config: theme.spring.smooth });
  return (
    <AbsoluteFill>
      <BgMesh tint={C.red} tint2={C.steel} />
      <Camera dur={dur} zoom={1.05}>
        <Scene ground={1440} groundCol="#28262a">
          <Skyline y={1440} seed={201} minY={1000} />
          {/* 쓰러지는 혁명 깃발 */}
          <g transform={`rotate(${interpolate(fall, [0, 1], [0, 74])} 210 1440)`}
            opacity={interpolate(fall, [0, 1], [1, 0.45])}>
            <Flag x={210} y={1440} w={210} color="#8c3a2e" h={520} />
          </g>
          {/* 강의실 책상 + 책 */}
          <g opacity={rise} transform={`translate(0, ${interpolate(rise, [0, 1], [50, 0])})`}>
            <rect x={560} y={1250} width={420} height={30} rx={8} fill="#57503f"
              stroke={C.outline} strokeWidth={7} />
            <rect x={600} y={1280} width={26} height={160} fill="#4a4436" />
            <rect x={914} y={1280} width={26} height={160} fill="#4a4436" />
            <Book x={770} y={1150} s={0.72} title="資本" rot={-5} />
          </g>
        </Scene>
      </Camera>
      <Entrance delay={2} from={-30} style={{ position: "absolute", top: 528, width: "100%",
        textAlign: "center" }}>
        <span style={{ fontFamily: theme.font.sans, fontSize: 52, color: C.paper,
          textShadow: "0 4px 16px #000" }}>이 세계의 마르크스는</span>
      </Entrance>
      <div style={{ position: "absolute", top: 645, width: "100%",
        display: "flex", justifyContent: "center" }}>
        <Stamp text="大學에" delay={16} size={430} textColor={C.yellow} />
      </div>
    </AbsoluteFill>
  );
};

/* s3 — 근거1: 텅 빈 광장에 남은 질문 */
const S3: React.FC<{ dur: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const q = spring({ frame: frame - 22, fps, config: theme.spring.bouncy });
  return (
    <AbsoluteFill>
      <BgMesh tint={C.steel} />
      <Camera dur={dur} zoom={1.05}>
        <Scene ground={1400} groundCol="#28262a">
          <Skyline y={1400} seed={203} minY={980} />
          {/* 부러진 깃대만 남은 광장 */}
          <line x1={300} y1={1400} x2={318} y2={1150} stroke="#5a5450" strokeWidth={14} />
          <line x1={318} y1={1150} x2={392} y2={1096} stroke="#5a5450" strokeWidth={12} />
          <Sans x={286} y={1340} size={36} color="#8a8a92">조직은 남지 않았다</Sans>
          {/* 남은 질문 말풍선 */}
          <g opacity={q} transform={`scale(${interpolate(q, [0, 1], [0.72, 1])})`}
            style={{ transformOrigin: "700px 1160px" }}>
            <rect x={470} y={1050} width={520} height={200} rx={28} fill="#e8e2d4"
              stroke={C.outline} strokeWidth={8} />
            <polygon points="560,1248 520,1330 620,1248" fill="#e8e2d4"
              stroke={C.outline} strokeWidth={7} />
            <text x={730} y={1130} textAnchor="middle" fontFamily={theme.font.sans}
              fontSize={44} fill={C.ink}>왜 어떤 사람은</text>
            <text x={730} y={1200} textAnchor="middle" fontFamily={theme.font.sans}
              fontSize={48} fill={C.red}>계속 가난한가</text>
          </g>
        </Scene>
      </Camera>
      <Typo top={545} size={80} delay={2}>남은 건 질문이었다</Typo>
    </AbsoluteFill>
  );
};

/* s4 — 미니 페이오프: 정당 간판이 내려가고 대학 간판이 올라간다 */
const S4: React.FC<{ dur: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const sw = spring({ frame: frame - 14, fps, config: theme.spring.heavy });
  const pay = spring({ frame: frame - 40, fps, config: theme.spring.snappy });
  return (
    <AbsoluteFill>
      <BgMesh tint={C.amber} tint2={C.steel} />
      <Camera dur={dur} zoom={1.05}>
        <Scene ground={1500} groundCol="#28262a">
          {/* 간판 기둥 */}
          <rect x={250} y={900} width={24} height={600} fill="#4a4436" />
          <rect x={806} y={900} width={24} height={600} fill="#4a4436" />
          {/* 내려가는 정당 간판 */}
          <g transform={`translate(0, ${interpolate(sw, [0, 1], [0, 330])})`}
            opacity={interpolate(sw, [0, 1], [1, 0.28])}>
            <rect x={120} y={940} width={290} height={120} rx={12} fill="#5e2820"
              stroke={C.outline} strokeWidth={7} />
            <Sans x={265} y={1018} size={46} color="#e0c0b4">공산당</Sans>
          </g>
          {/* 올라오는 대학 간판 */}
          <g transform={`translate(0, ${interpolate(sw, [0, 1], [330, 0])})`} opacity={sw}>
            <rect x={676} y={940} width={290} height={120} rx={12} fill="#3e4a5c"
              stroke={C.outline} strokeWidth={7} />
            <Sans x={821} y={1018} size={46} color="#c8dcee">大學</Sans>
          </g>
        </Scene>
      </Camera>
      <Typo top={545} size={74} delay={2}>정당은 사라져도</Typo>
      <div style={{ position: "absolute", top: 1230, width: "100%", textAlign: "center",
        opacity: pay, transform: `translateY(${interpolate(pay, [0, 1], [28, 0])}px)` }}>
        <span style={{ fontFamily: theme.font.serif, fontSize: 72, color: C.yellow,
          textShadow: "0 5px 22px #000" }}>학문으로 남았다</span>
      </div>
    </AbsoluteFill>
  );
};

/* s5 — 근거2: 공장이 늘수록 커지는 질문 (난징대 강의실) */
const S5: React.FC<{ dur: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const grow = interpolate(frame, [10, 60], [0, 1],
    { easing: theme.ease.inOut, extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <AbsoluteFill>
      <BgMesh tint={C.amber} />
      <Camera dur={dur} zoom={1.05}>
        <Scene ground={1520} groundCol="#332f2a">
          {/* 공장 라인 — 점점 늘어남 */}
          {[0, 1, 2, 3].map((k) => (
            <g key={k} opacity={grow > k * 0.25 ? 1 : 0}
              transform={`translate(${60 + k * 250}, 1180)`}>
              <rect x={0} y={0} width={190} height={140} fill="#4a4436"
                stroke={C.outline} strokeWidth={6} />
              {[0, 1].map((j) => (
                <polygon key={j} points={`${j * 95},0 ${j * 95 + 48},-46 ${j * 95 + 95},0`}
                  fill="#5a5244" stroke={C.outline} strokeWidth={5} />
              ))}
              <rect x={150} y={-110} width={26} height={70} fill="#57503f"
                stroke={C.outline} strokeWidth={5} />
            </g>
          ))}
          <Smoke x={230} y={1080} scale={0.6} />
          {/* 칠판 */}
          <rect x={210} y={640} width={660} height={330} rx={16} fill="#2e4436"
            stroke="#6e6250" strokeWidth={14} />
          <text x={540} y={790} textAnchor="middle" fontFamily={theme.font.sans}
            fontSize={54} fill="#dce8dc">왜 어떤 사람은</text>
          <text x={540} y={880} textAnchor="middle" fontFamily={theme.font.sans}
            fontSize={58} fill={C.yellow}
            style={{ opacity: Math.min(1, grow * 1.6) }}>계속 가난한가</text>
          <Sans x={540} y={1030} size={38} color="#c8c4bc">南京大學 강의실</Sans>
        </Scene>
      </Camera>
    </AbsoluteFill>
  );
};

/* s6 — 근거3: 무기가 아니라 각주로 */
const S6: React.FC<{ dur: number }> = ({ dur }) => (
  <AbsoluteFill>
    <BgMesh tint={C.steel} tint2={C.amber} />
    <Camera dur={dur} zoom={1.04}>
      <Scene ground={1580} groundCol="#26242a">
        <Skyline y={1580} seed={206} minY={1420} />
      </Scene>
    </Camera>
    <Typo top={545} size={72} delay={2}>무기가 아니라 각주로</Typo>
    <div style={{ position: "absolute", top: 720, left: 0, right: 0, display: "flex",
      flexDirection: "column", alignItems: "center", gap: 30 }}>
      {[["1970s", "노동사 연구"], ["1980s", "문화 비평"]].map(([y, t], i) => (
        <Entrance key={y} delay={6 + i * 11}>
          <Card w={700} outline={i ? "#5a6072" : C.amber}>
            <div style={{ display: "flex", alignItems: "center", justifyContent: "center", gap: 30 }}>
              <span style={{ fontFamily: theme.font.serif, fontSize: 52,
                color: i ? "#9a9eaa" : C.amber }}>{y}</span>
              <span style={{ fontSize: 50, whiteSpace: "nowrap" }}>{t}</span>
            </div>
          </Card>
        </Entrance>
      ))}
    </div>
    {/* 각주 기호가 붙은 페이지 */}
    <Entrance delay={30} style={{ position: "absolute", top: 1080, width: "100%",
      display: "flex", justifyContent: "center" }}>
      <div style={{ background: "#e8e2d4", border: `7px solid ${theme.colors.outline}`,
        borderRadius: 10, padding: "26px 40px", width: 520, transform: "rotate(-2deg)" }}>
        {[1, 2, 3].map((k) => (
          <div key={k} style={{ height: 12, background: "#c4bca8", borderRadius: 6,
            marginBottom: 14, width: k === 3 ? "62%" : "100%" }} />
        ))}
        <div style={{ borderTop: "3px solid #a49c88", marginTop: 18, paddingTop: 14,
          fontFamily: theme.font.sans, fontSize: 30, color: "#4a443a" }}>
          註) 馬克思, 1867.
        </div>
      </div>
    </Entrance>
  </AbsoluteFill>
);

/* s7 — Second Hook: 우파도 같은 책을 읽는다 */
const S7: React.FC<{ dur: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const p = spring({ frame: frame - 24, fps, config: theme.spring.snappy });
  return (
    <AbsoluteFill>
      <BgMesh tint={C.red} tint2={C.amber} />
      <Camera dur={dur} zoom={1.05}>
        <Scene ground={1460} groundCol="#28262a">
          <Person x={300} y={1480} height={420} outfit="student" expr="closed"
            pose="stand" tie="#3e5a78" facing={1} />
          <Person x={800} y={1480} height={420} outfit="suit" expr="closed"
            pose="stand" tie="#983a2e" facing={-1} />
          <Book x={318} y={1330} s={0.40} title="資本" rot={-8} />
          <Book x={782} y={1330} s={0.40} title="資本" rot={8} />
          <Sans x={300} y={1540} size={36} color="#9ab8d2">좌파 학자</Sans>
          <Sans x={800} y={1540} size={36} color="#e0b09c">우파 학자</Sans>
        </Scene>
      </Camera>
      <Typo top={545} size={74} delay={2}>우파도 그를 읽는다</Typo>
      <div style={{ position: "absolute", top: 700, width: "100%", textAlign: "center",
        opacity: p }}>
        <Card w={640} outline={C.amber} style={{ margin: "0 auto" }}>
          <span style={{ fontSize: 44, color: C.amber, whiteSpace: "nowrap" }}>
            개발국가를 비판하려고</span>
        </Card>
      </div>
    </AbsoluteFill>
  );
};

/* s8 — 본 페이오프: 해압축 상자 (정본 연출 시그니처) */
const S8: React.FC<{ dur: number }> = () => (
  <AbsoluteFill>
    <BgMesh tint={C.amber} tint2={C.steel} />
    <Scene ground={1620} groundCol="#26242a">
      <Skyline y={1620} seed={208} minY={1480} />
      {/* 이긴 이념 — 잠긴 채 굳음 */}
      <DecompressBox label="三民主義" incidents={[]} x={296} y={1330}
        delay={4} open={false} w={340} />
      {/* 진 이념 — 열려서 incident가 쏟아짐 */}
      <DecompressBox label="馬克思" incidents={["노동사", "문화비평", "각주"]}
        x={716} y={1330} delay={14} open w={340} />
    </Scene>
    <Typo top={545} size={68} delay={2}>이긴 곳에서 굳고</Typo>
    <Typo top={676} size={68} color={C.yellow} delay={8}>진 곳에서 자란다</Typo>
  </AbsoluteFill>
);

/* s9 — 확장: 이긴 쪽은? */
const S9: React.FC<{ dur: number }> = ({ dur }) => (
  <AbsoluteFill>
    <BgMesh tint={C.yellow} tint2={C.amber} />
    <Camera dur={dur} zoom={1.06}>
      <Scene ground={1470} groundCol="#26242a">
        <Person x={540} y={1560} height={370} outfit="student" expr="worried"
          pose="stand" tie="#3e5a78" />
      </Scene>
    </Camera>
    <Typo top={620} size={92} delay={2}>그럼 이긴 쪽의</Typo>
    <Typo top={840} size={124} color={C.yellow} delay={7}>이념은?</Typo>
  </AbsoluteFill>
);

/* s10 — 다음 모순: 삼민주의는 성경이 되었다 (하드컷) */
const S10: React.FC<{ dur: number }> = ({ dur }) => (
  <AbsoluteFill>
    <BgMesh tint={C.amber} />
    <Camera dur={dur} zoom={1.06}>
      <Scene ground={1560} groundCol="#26242a">
        <Book x={540} y={1300} s={1.05} title="三民" col="#8a6a2e" rot={0} />
      </Scene>
    </Camera>
    <Typo top={600} size={96} delay={2}>승리한 삼민주의는</Typo>
    <Typo top={820} size={140} color={C.yellow} delay={8}>성경이 되었다</Typo>
  </AbsoluteFill>
);

export const S2E1_SCENES = [S1, Anchor1946, S3, S4, S5, S6, S7, S8, S9, S10];
