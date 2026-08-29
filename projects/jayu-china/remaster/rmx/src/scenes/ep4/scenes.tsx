import React from "react";
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { theme } from "../../theme";
import { BgMesh, Camera } from "../../kit/layers";
import { Entrance, Stamp, Card, Breathe } from "../../kit/ui";
import { Person } from "../../kit/people";
import { ForestRow, Skyline, Train, Rail, Bridge, River, Ship, Crane, Containers, Flag, Picket, Smoke } from "../../kit/props";

const C = theme.colors;
const GROUND = "#2c2a2c";
const W = 1080, H = 1920;

/** SVG 씬 캔버스 + 지면. */
const Scene: React.FC<{ ground?: number; groundCol?: string; children: React.ReactNode }> =
({ ground, groundCol = GROUND, children }) => (
  <svg width={W} height={H} viewBox={`0 0 ${W} ${H}`}
    style={{ position: "absolute", inset: 0 }}>
    {ground !== undefined && (
      <>
        <rect x={0} y={ground} width={W} height={H - ground} fill={groundCol} />
        <rect x={0} y={ground - 6} width={W} height={14} fill="#3f434f" />
      </>
    )}
    {children}
  </svg>
);

const Serif: React.FC<{ x: number; y: number; size: number; color?: string;
  children: React.ReactNode }> = ({ x, y, size, color = C.paper, children }) => (
  <text x={x} y={y} textAnchor="middle" fontFamily={theme.font.serif} fontSize={size}
    fill={color} stroke="#000" strokeWidth={size * 0.09} paintOrder="stroke">{children}</text>
);
const Sans: React.FC<{ x: number; y: number; size: number; color?: string; anchor?: string;
  children: React.ReactNode }> = ({ x, y, size, color = C.paper, anchor = "middle", children }) => (
  <text x={x} y={y} textAnchor={anchor as never} fontFamily={theme.font.sans} fontSize={size}
    fill={color} stroke="#000" strokeWidth={size * 0.11} paintOrder="stroke">{children}</text>
);

/* s1 — WTF: 한중 악수 + 親中 스탬프 */
export const S1: React.FC<{ dur: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const pIn = (d: number) => spring({ frame: frame - d, fps, config: theme.spring.smooth });
  const p1 = pIn(2), p2 = pIn(5);
  return (
    <AbsoluteFill>
      <BgMesh />
      <Camera dur={dur} zoom={1.045}>
        <Scene ground={1364}>
          <Skyline y={1364} seed={41} minY={700} />
          <g opacity={p1} transform={`translate(${interpolate(p1, [0, 1], [-160, 0])},0)`}>
            <Person x={352} y={1392} height={560} outfit="suit_b" expr="smug" facing={1}
              pose="reach_r" tie="#3e5a78" />
          </g>
          <g opacity={p2} transform={`translate(${interpolate(p2, [0, 1], [160, 0])},0)`}>
            <Person x={716} y={1392} height={560} outfit="suit" expr="smug" facing={-1}
              pose="reach_l" tie="#983a2e" />
          </g>
          <Sans x={165} y={1000} size={42}>한국 보수당</Sans>
          <Sans x={925} y={1000} size={42} color="#ecc478">자유중국</Sans>
        </Scene>
      </Camera>
      <Entrance delay={4} from={-30} style={{ position: "absolute", top: 528, width: "100%",
        textAlign: "center" }}>
        <span style={{ fontFamily: theme.font.sans, fontSize: 54, color: C.paper,
          textShadow: "0 4px 16px #000, 0 0 6px #000" }}>한국 보수당은</span>
      </Entrance>
      <div style={{ position: "absolute", top: 665, width: "100%",
        display: "flex", justifyContent: "center" }}>
        <Stamp text="親中" delay={14} size={400} textColor={C.yellow} />
      </div>
    </AbsoluteFill>
  );
};

/* s2 — 1946 갈림길 (시리즈 앵커) */
export const S2: React.FC<{ dur: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const grow = spring({ frame: frame - 6, fps, config: theme.spring.heavy });
  const jx = 540, jy = 1330;
  const bx = interpolate(grow, [0, 1], [0, 300]);
  const by = interpolate(grow, [0, 1], [0, 330]);
  return (
    <AbsoluteFill>
      <BgMesh tint={C.steel} tint2={C.amber} />
      <Camera dur={dur} zoom={1.06}>
        <Scene ground={1010} groundCol="#292628">
          <ForestRow y={1010} seed={46} color="#1f2c20" />
          {Array.from({ length: 8 }).map((_, i) => {
            const t = i / 7;
            return <rect key={i} x={jx - 84 + 30 * t} y={1740 - (1740 - jy) * t}
              width={168 - 60 * t} height={13} fill="#5e5030" />;
          })}
          <line x1={jx} y1={1740} x2={jx} y2={jy} stroke={C.outline} strokeWidth={26} />
          <line x1={jx} y1={1740} x2={jx} y2={jy} stroke="#787c8a" strokeWidth={15} />
          <line x1={jx} y1={jy} x2={jx - bx} y2={jy - by * 0.82} stroke={C.outline} strokeWidth={20} />
          <line x1={jx} y1={jy} x2={jx - bx} y2={jy - by * 0.82} stroke="#4c505e" strokeWidth={11} />
          <line x1={jx} y1={jy} x2={jx + bx} y2={jy - by * 0.82} stroke={C.outline} strokeWidth={24} />
          <line x1={jx} y1={jy} x2={jx + bx} y2={jy - by * 0.82} stroke={C.amber} strokeWidth={14} />
          <circle cx={jx} cy={jy} r={26} fill={C.paper} stroke={C.outline} strokeWidth={8} />
          {grow > 0.75 && (
            <>
              <Sans x={205} y={1090} size={46} color="#7c8090">공산당</Sans>
              <Sans x={880} y={1058} size={54} color={C.amber}>국민당 승리</Sans>
            </>
          )}
        </Scene>
      </Camera>
      <Entrance delay={2} style={{ position: "absolute", top: 560, width: "100%",
        textAlign: "center" }}>
        <span style={{ fontFamily: theme.font.serif, fontSize: 175, color: C.paper,
          textShadow: "0 6px 30px #000" }}>1946</span>
      </Entrance>
    </AbsoluteFill>
  );
};

/* s3 — 약속: 타이포 */
export const S3: React.FC<{ dur: number }> = ({ dur }) => (
  <AbsoluteFill>
    <BgMesh tint={C.yellow} />
    <Camera dur={dur} zoom={1.05}>
      <Scene ground={1430} groundCol="#26242a">
        <Person x={540} y={1500} height={400} outfit="student" expr="smile"
          pose="hands_up" tie="#3e5a78" waveArm />
      </Scene>
    </Camera>
    <Entrance delay={3} style={{ position: "absolute", top: 620, width: "100%", textAlign: "center" }}>
      <span style={{ fontFamily: theme.font.serif, fontSize: 140, color: C.paper,
        textShadow: "0 6px 26px #000" }}>이유는</span>
    </Entrance>
    <Entrance delay={9} style={{ position: "absolute", top: 850, width: "100%", textAlign: "center" }}>
      <span style={{ fontFamily: theme.font.serif, fontSize: 126, color: C.yellow,
        textShadow: "0 6px 26px #000" }}>역사가 달랐다</span>
    </Entrance>
  </AbsoluteFill>
);

/* s4 — 압록강 철교 보급 열차 */
export const S4: React.FC<{ dur: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const trainX = interpolate(frame, [0, dur], [-160, 980], { easing: theme.ease.inOut });
  return (
    <AbsoluteFill>
      <BgMesh tint={C.steel} />
      <Camera dur={dur} zoom={1.05} panX={-14}>
        <Scene>
          <ForestRow y={1150} seed={4} color="#20301f" />
          <River y0={1150} y1={1500} />
          <rect x={0} y={1500} width={1080} height={420} fill={GROUND} />
          <Bridge x0={-40} x1={1120} y={1120} />
          <g transform={`translate(${trainX},0)`}>
            <Train x={500} y={1114} scale={0.85} cars={2} roll={5} />
            <Smoke x={432} y={950} scale={0.9} />
          </g>
          <Sans x={210} y={1210} size={44} color="#8caabe">압록강</Sans>
          <Person x={250} y={1710} height={420} outfit="uniform" expr="smile" hat="helmet"
            facing={1} pose="wave" waveArm />
          <Person x={452} y={1730} height={390} outfit="uniform" expr="surprised" hat="helmet"
            facing={1} pose="stand" />
        </Scene>
      </Camera>
      <Entrance delay={10} style={{ position: "absolute", top: 580, width: "100%",
        display: "flex", justifyContent: "center" }}>
        <Card w={520} outline="#666c7e">
          <div style={{ display: "flex", alignItems: "center", justifyContent: "center", gap: 30 }}>
            <span style={{ fontSize: 60, color: "#9a9eaa" }}>중공군</span>
            <svg width={110} height={80}><line x1={10} y1={10} x2={100} y2={70} stroke={C.red} strokeWidth={13} strokeLinecap="round" />
              <line x1={100} y1={10} x2={10} y2={70} stroke={C.red} strokeWidth={13} strokeLinecap="round" /></svg>
          </div>
        </Card>
      </Entrance>
    </AbsoluteFill>
  );
};

/* s5 — 같은 편: 두 병사 + 깃발 + 同盟 */
export const S5: React.FC<{ dur: number }> = ({ dur }) => (
  <AbsoluteFill>
    <BgMesh />
    <Camera dur={dur} zoom={1.055}>
      <Scene ground={1360}>
        <Flag x={165} y={1360} w={240} color="#b07a32" />
        <Flag x={915} y={1360} w={-240} color="#4a5c78" />
        <Person x={442} y={1382} height={470} outfit="uniform" expr="smile" hat="helmet"
          facing={1} pose="stand" />
        <Person x={644} y={1382} height={440} outfit="uniform" expr="smile" hat="helmet"
          facing={-1} pose="stand" />
        <Sans x={215} y={1035} size={40} color="#ecc478">자유중국군</Sans>
        <Sans x={870} y={1035} size={40}>한국군</Sans>
      </Scene>
    </Camera>
    <div style={{ position: "absolute", top: 545, width: "100%",
      display: "flex", justifyContent: "center" }}>
      <Stamp text="同盟" delay={8} size={300} />
    </div>
    <Entrance delay={16} style={{ position: "absolute", top: 800, width: "100%", textAlign: "center" }}>
      <span style={{ fontFamily: theme.font.serif, fontSize: 78, color: C.paper,
        textShadow: "0 5px 22px #000" }}>같은 편의 기억</span>
    </Entrance>
  </AbsoluteFill>
);

/* s6 — 대륙 종단 철도 지도 */
export const S6: React.FC<{ dur: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const stops = [["부산", 780, 1330], ["서울", 600, 1080], ["신의주", 448, 850], ["난징", 268, 640]] as const;
  const draw = interpolate(frame, [6, 40], [0, 1],
    { easing: theme.ease.inOut, extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <AbsoluteFill>
      <BgMesh tint={C.amber} />
      <Camera dur={dur} zoom={1.05}>
        <Scene ground={1470} groundCol="#26242a">
          <Skyline y={1470} seed={6} minY={1180} />
          <polyline
            points={stops.map(([, x, y]) => `${x},${y}`).join(" ")}
            fill="none" stroke={C.outline} strokeWidth={24} strokeLinejoin="round"
            strokeDasharray={1400} strokeDashoffset={1400 * (1 - draw)} />
          <polyline
            points={stops.map(([, x, y]) => `${x},${y}`).join(" ")}
            fill="none" stroke={C.amber} strokeWidth={13} strokeLinejoin="round"
            strokeDasharray={1400} strokeDashoffset={1400 * (1 - draw)} />
          {stops.map(([name, x, y], i) => {
            const big = i === 0 || i === 3;
            const p = spring({ frame: frame - 8 - i * 7, fps, config: theme.spring.snappy });
            return (
              <g key={name} opacity={p} transform={`scale(${0.7 + 0.3 * p})`}
                style={{ transformOrigin: `${x}px ${y}px` }}>
                <circle cx={x} cy={y} r={big ? 24 : 15} fill={big ? C.amber : "#969aa6"}
                  stroke={C.outline} strokeWidth={6} />
                <Sans x={i === 0 ? x - 44 : x + 44} y={y + (i === 0 ? -46 : 14)}
                  size={big ? 56 : 44} color={big ? C.yellow : C.paper}
                  anchor={i === 0 ? "end" : "start"}>{name}</Sans>
              </g>
            );
          })}
          <Train x={1035} y={1470} scale={0.42} cars={1} drive={0} />
        </Scene>
      </Camera>
      <Entrance delay={3} style={{ position: "absolute", top: 555, width: "100%", textAlign: "center" }}>
        <span style={{ fontFamily: theme.font.serif, fontSize: 92, color: C.paper,
          textShadow: "0 5px 22px #000" }}>수출길 = 대륙</span>
      </Entrance>
    </AbsoluteFill>
  );
};

/* s7 — 부산항 재계: 김도현 */
export const S7: React.FC<{ dur: number }> = ({ dur }) => (
  <AbsoluteFill>
    <BgMesh tint={C.steel} tint2={C.amber} />
    <Camera dur={dur} zoom={1.05} panX={10}>
      <Scene>
        <Ship x={810} y={1120} scale={0.88} />
        <rect x={0} y={1255} width={1080} height={665} fill={GROUND} />
        <rect x={0} y={1247} width={1080} height={16} fill="#3f434f" />
        <Crane x={790} y={1247} dir={-1} scale={0.92} />
        <Containers x={70} y={1247} />
        <Breathe><g /></Breathe>
        <Person x={370} y={1650} height={490} outfit="suit" expr="smug" facing={1}
          pose="hold_case" tie="#983a2e" />
      </Scene>
    </Camera>
    <Entrance delay={4} style={{ position: "absolute", top: 555, width: "100%", textAlign: "center" }}>
      <span style={{ fontFamily: theme.font.serif, fontSize: 84, color: C.paper,
        textShadow: "0 5px 22px #000" }}>지킬 것이 많은 쪽</span>
    </Entrance>
    <Entrance delay={26} style={{ position: "absolute", top: 1560, width: "100%",
      display: "flex", justifyContent: "center" }}>
      <div style={{ background: "#0d0b0a", borderRadius: 14, padding: "14px 30px",
        fontFamily: theme.font.sans, fontSize: 38, color: C.paper }}>
        김도현 (58) · 부산 물류가문 3대</div>
    </Entrance>
  </AbsoluteFill>
);

/* s8 — 반공의 방향: 나침반 바늘 → 모스크바 */
export const S8: React.FC<{ dur: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const swing = spring({ frame: frame - 26, fps, config: { damping: 9, stiffness: 90 } });
  const ang = interpolate(swing, [0, 1], [115, -38]);
  return (
    <AbsoluteFill>
      <BgMesh tint={C.red} tint2={C.steel} />
      <Camera dur={dur} zoom={1.05}>
        <Scene ground={1400} groundCol="#28262a">
          <Person x={540} y={1430} height={430} outfit="coat" expr="closed" facing={0}
            pose="arms_cross" />
          <Sans x={830} y={1230} size={38} color="#c8c4bc">이 세계의 반공 보수</Sans>
        </Scene>
      </Camera>
      <Entrance delay={2} style={{ position: "absolute", top: 545, width: "100%", textAlign: "center" }}>
        <span style={{ fontFamily: theme.font.serif, fontSize: 84, color: C.paper,
          textShadow: "0 5px 22px #000" }}>反共의 방향</span>
      </Entrance>
      <div style={{ position: "absolute", top: 740, left: 0, right: 0, display: "flex",
        justifyContent: "center", gap: 120 }}>
        <Entrance delay={10}><Card w={330} outline="#5a6072">
          <span style={{ fontSize: 56, color: "#7c8090" }}>베이징</span></Card></Entrance>
        <Entrance delay={14}><Card w={360} outline={C.red}>
          <span style={{ fontSize: 56, color: "#e68c80" }}>모스크바</span></Card></Entrance>
      </div>
      <svg width={1080} height={1920} style={{ position: "absolute", inset: 0 }}>
        <circle cx={540} cy={700} r={25} fill={C.paper} stroke={C.outline} strokeWidth={7} />
        <g transform={`rotate(${ang} 540 700)`} opacity={Math.min(1, frame / 26)}>
          <line x1={540} y1={700} x2={540} y2={880} stroke={C.red} strokeWidth={15} strokeLinecap="round" />
          <polygon points="540,910 516,872 564,872" fill={C.red} />
        </g>
      </svg>
    </AbsoluteFill>
  );
};

/* s9 — Payoff: 인과 사슬 캐스케이드 */
export const S9: React.FC<{ dur: number }> = () => {
  const steps = [["중공군 없는 전쟁", "#5a6072", C.paper], ["적대 기억 없음", "#5a6072", C.paper],
    ["동맹 + 대륙경제", C.amber, C.amber], ["보수 = 친중", C.yellow, C.yellow]] as const;
  return (
    <AbsoluteFill>
      <BgMesh />
      <Scene ground={1560} groundCol="#26242a">
        <Skyline y={1560} seed={9} minY={1340} />
      </Scene>
      <div style={{ position: "absolute", top: 545, left: 0, right: 0, display: "flex",
        flexDirection: "column", alignItems: "center", gap: 0 }}>
        {steps.map(([t, oc, tc], i) => (
          <React.Fragment key={t}>
            {i > 0 && (
              <Entrance delay={6 + i * 9} from={16}>
                <svg width={40} height={62}>
                  <line x1={20} y1={0} x2={20} y2={40} stroke={C.amber} strokeWidth={9} />
                  <polygon points="20,60 4,38 36,38" fill={C.amber} />
                </svg>
              </Entrance>
            )}
            <Entrance delay={4 + i * 9}>
              <Card w={660} outline={oc}><span style={{ fontSize: 52, color: tc }}>{t}</span></Card>
            </Entrance>
          </React.Fragment>
        ))}
        <Entrance delay={46}>
          <div style={{ marginTop: 30, fontFamily: theme.font.sans, fontSize: 46,
            color: "#d8d0c2", textShadow: "0 4px 16px #000" }}>기억이 다르면 묶음이 다르다</div>
        </Entrance>
      </div>
    </AbsoluteFill>
  );
};

/* s10 — 확장: 질문 */
export const S10: React.FC<{ dur: number }> = ({ dur }) => (
  <AbsoluteFill>
    <BgMesh tint={C.yellow} tint2={C.red} />
    <Camera dur={dur} zoom={1.06}>
      <Scene ground={1450} groundCol="#26242a">
        <Person x={540} y={1560} height={360} outfit="student" expr="worried"
          pose="stand" tie="#3e5a78" />
      </Scene>
    </Camera>
    {[["그럼, 누가", 610, 120, C.paper, 3], ["중국 의존을", 810, 120, C.paper, 9],
      ["비판할까?", 1010, 140, C.yellow, 15]].map(([t, y, fs, col, d]) => (
      <Entrance key={t as string} delay={d as number}
        style={{ position: "absolute", top: y as number, width: "100%", textAlign: "center" }}>
        <span style={{ fontFamily: theme.font.serif, fontSize: fs as number, color: col as string,
          textShadow: "0 6px 26px #000" }}>{t}</span>
      </Entrance>
    ))}
  </AbsoluteFill>
);

/* s11 — 다음 모순: 진보의 피켓 (하드컷) */
export const S11: React.FC<{ dur: number }> = ({ dur }) => (
  <AbsoluteFill>
    <BgMesh tint={C.green} tint2={C.steel} />
    <Camera dur={dur} zoom={1.07}>
      <Scene ground={1400} groundCol="#26282a">
        <Skyline y={1400} seed={11} minY={880} />
        <Picket x={355} top={585} w={520} h={230} poleTo={1140}>
          <text x={355} y={678} textAnchor="middle" fontFamily={theme.font.sans}
            fontSize={58} fill={C.ink}>중국 자본을</text>
          <text x={355} y={764} textAnchor="middle" fontFamily={theme.font.sans}
            fontSize={66} fill={C.red}>막아라</text>
        </Picket>
        <Person x={355} y={1450} height={420} outfit="worker" expr="shout" hat="cap"
          pose="hold_sign" facing={0} />
        <Person x={800} y={1450} height={440} outfit="suit_r" expr="shout"
          pose="hands_up" facing={0} waveArm />
      </Scene>
    </Camera>
    <Entrance delay={5} style={{ position: "absolute", top: 620, left: 620, right: 0,
      textAlign: "center" }}>
      <div style={{ fontFamily: theme.font.serif, fontSize: 92, color: C.greenText,
        textShadow: "0 5px 22px #000", lineHeight: 1.35 }}>진보의<br />구호</div>
    </Entrance>
  </AbsoluteFill>
);

export const EP4_SCENES = [S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, S11];
