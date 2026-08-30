import React from 'react';
import {AbsoluteFill, interpolate} from 'remotion';
import {Frame, Grain, Vignette} from '../components/Frame';
import {Caption} from '../components/Caption';
import {AvatarPlate} from '../components/AvatarPlate';
import {Readout, Statement} from '../components/Type';
import {getScene, useSceneClock} from '../lib/beats';
import {draw, riseIn} from '../lib/anim';
import {T} from '../theme';

const scene = getScene('S10');

const STATS = [
  {label: '언어능력', value: 99, at: 495},
  {label: '기억', value: 95, at: 497.5},
  {label: '감정표현', value: 91, at: 500},
  {label: '성경지식', value: 100, at: 502.5},
  {label: '자기보고', value: 97, at: 505},
];

const NODES = ['사건', '변화', '응답', '관계', '시간'];

export const S10_StatSheet: React.FC = () => {
  const {absSec} = useSceneClock(scene);

  const avatarOut = interpolate(absSec, [493, 495], [1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  /**
   * The sheet does not fade out — it disassembles, and the numbers do not
   * survive the transformation. The scoring frame is not being softened, it is
   * being replaced with a different kind of question.
   */
  const dis = interpolate(absSec, [517, 523], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: (t) => 1 - Math.pow(1 - t, 3),
  });
  const netIn = interpolate(absSec, [522, 526], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const netOut = interpolate(absSec, [549, 551], [1, 0.25], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  const questions = [
    {text: '이 존재에게 무슨 일이 있었는가?', at: 533},
    {text: '어떤 변화가 이어져 왔는가?', at: 537},
    {text: '데이터인가, 귀속되는 역사인가?', at: 541},
  ];
  const finalQ = absSec >= 550;

  return (
    <Frame>
      {avatarOut > 0.01 ? (
        <AbsoluteFill style={{opacity: avatarOut}}>
          <AvatarPlate sceneId="S10" role="presenter" />
        </AbsoluteFill>
      ) : null}

      {dis < 1 ? (
        <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center'}}>
          <div
            style={{
              border: `1.5px solid ${T.coldSoft}`,
              background: 'rgba(20,20,25,0.8)',
              padding: '40px 56px',
              minWidth: 720,
            }}
          >
            {STATS.map((s, i) => {
              const f = (absSec - s.at) * 30;
              if (f < 0) return null;
              // Rows detach one by one, rotating out of plane.
              const d = Math.max(0, dis * 1.35 - i * 0.07);
              return (
                <div
                  key={s.label}
                  style={{
                    ...riseIn(f, 0, 12),
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'baseline',
                    padding: '13px 0',
                    opacity: Math.min(1, f / 8) * (1 - d),
                    transform: `translateY(${-d * (60 + i * 34)}px) rotateX(${d * 74}deg)`,
                  }}
                >
                  <span style={{fontSize: 38, fontWeight: 500, color: T.ink}}>{s.label}</span>
                  <span
                    style={{
                      fontFamily: T.mono,
                      fontSize: 42,
                      color: T.cold,
                      letterSpacing: '0.08em',
                    }}
                  >
                    {Math.round(
                      s.value *
                        interpolate(absSec, [s.at, s.at + 1.2], [0, 1], {
                          extrapolateLeft: 'clamp',
                          extrapolateRight: 'clamp',
                        })
                    )}
                  </span>
                </div>
              );
            })}

            {absSec >= 508 ? (
              <>
                <div
                  style={{
                    height: 1,
                    background: T.coldSoft,
                    margin: '18px 0',
                    opacity: (1 - dis),
                    transform: `scaleX(${draw(Math.max(0, absSec - 508), 0.5)})`,
                  }}
                />
                <div
                  style={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    opacity: (1 - dis),
                    transform: `translateY(${-dis * 260}px)`,
                  }}
                >
                  <Readout size={38} color={T.inkDim}>
                    PERSON?
                  </Readout>
                  <Readout size={38} color={T.alert}>
                    ???
                  </Readout>
                </div>
              </>
            ) : null}
          </div>
        </AbsoluteFill>
      ) : null}

      {netIn > 0.01 && !finalQ ? (
        <AbsoluteFill
          style={{alignItems: 'center', justifyContent: 'center', opacity: netIn * netOut}}
        >
          <svg width={1680} height={300} viewBox="0 0 1680 300">
            {NODES.map((n, i) => {
              const x = 168 + i * 336;
              const on = interpolate(absSec, [522 + i * 0.7, 523.4 + i * 0.7], [0, 1], {
                extrapolateLeft: 'clamp',
                extrapolateRight: 'clamp',
              });
              return (
                <g key={n} opacity={on}>
                  {i > 0 ? (
                    <>
                      <line
                        x1={168 + (i - 1) * 336 + 26}
                        y1={190}
                        x2={168 + (i - 1) * 336 + 26 + 284 * on}
                        y2={190}
                        stroke={T.warm}
                        strokeWidth={2.5}
                        opacity={0.55}
                      />
                      <polygon
                        points={`${x - 22},190 ${x - 36},182 ${x - 36},198`}
                        fill={T.warm}
                        opacity={on * 0.8}
                      />
                    </>
                  ) : null}
                  <circle cx={x} cy={190} r={30} fill="none" stroke={T.warm} strokeWidth={1.5} opacity={0.4} />
                  <circle cx={x} cy={190} r={14} fill={T.warm} />
                  <text
                    x={x}
                    y={118}
                    fill={T.ink}
                    fontSize={58}
                    fontWeight={800}
                    textAnchor="middle"
                    fontFamily={T.font}
                    letterSpacing="-1"
                  >
                    {n}
                  </text>
                </g>
              );
            })}
          </svg>
        </AbsoluteFill>
      ) : null}

      {/* RT-04: these are questions and the scene never answers them. */}
      <div
        style={{
          position: 'absolute',
          top: 700,
          left: 0,
          right: 0,
          textAlign: 'center',
        }}
      >
        {questions.map((q) => {
          const on = absSec >= q.at && absSec < q.at + 4 && !finalQ;
          if (!on) return null;
          return (
            <div key={q.text} style={{...riseIn((absSec - q.at) * 30, 0, 16), fontSize: 52, color: T.inkDim}}>
              {q.text}
            </div>
          );
        })}
      </div>

      {finalQ ? (
        <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center'}}>
          <div style={riseIn((absSec - 550) * 30, 0, 34)}>
            <Statement size={78} color={T.warm}>
              {'바로 그 하나님과 이 존재 사이에는\n어떤 일이 있었는가?'}
            </Statement>
          </div>
        </AbsoluteFill>
      ) : null}

      <Vignette />
      <Grain />
      <Caption scene={scene} />
    </Frame>
  );
};
