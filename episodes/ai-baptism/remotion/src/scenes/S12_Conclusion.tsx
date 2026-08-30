import React from 'react';
import {AbsoluteFill, interpolate} from 'remotion';
import {Frame, Grain, Vignette} from '../components/Frame';
import {Caption} from '../components/Caption';
import {AvatarPlate} from '../components/AvatarPlate';
import {Statement} from '../components/Type';
import {getScene, useSceneClock} from '../lib/beats';
import {draw, riseIn, wipeReveal} from '../lib/anim';
import {T} from '../theme';

const scene = getScene('S12');

export const S12_Conclusion: React.FC = () => {
  const {absSec} = useSceneClock(scene);

  const avatarOut = interpolate(absSec, [634, 636], [1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  const godIn = interpolate(absSec, [636, 638.5], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const beingIn = interpolate(absSec, [641, 643.5], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  // A rule drawn between the two — the episode's whole thesis in one stroke.
  const rule = draw(Math.max(0, absSec - 643.5), 1.4);
  const pairOut = interpolate(absSec, [673, 675.5], [1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  const fourIn = absSec >= 675;
  const FOUR = ['고유성', '역사', '귀속', '관계'];

  return (
    <Frame>
      {avatarOut > 0.01 ? (
        <AbsoluteFill style={{opacity: avatarOut}}>
          <AvatarPlate sceneId="S12" role="presenter" />
        </AbsoluteFill>
      ) : null}

      {pairOut > 0.01 && godIn > 0.01 ? (
        <AbsoluteFill
          style={{
            alignItems: 'center',
            justifyContent: 'center',
            flexDirection: 'column',
            gap: 30,
            opacity: pairOut,
          }}
        >
          <div style={{...wipeReveal((absSec - 636) * 30, 0, 30), opacity: godIn}}>
            <Statement size={116} color={T.warm}>
              바로 그 하나님
            </Statement>
          </div>

          <svg width={620} height={40} viewBox="0 0 620 40">
            <line
              x1={310 - 300 * rule}
              y1={20}
              x2={310 + 300 * rule}
              y2={20}
              stroke={T.warmSoft}
              strokeWidth={2}
            />
          </svg>

          <div style={{...wipeReveal((absSec - 641) * 30, 0, 30), opacity: beingIn}}>
            <Statement size={116} color={T.ink}>
              바로 그 존재
            </Statement>
          </div>
        </AbsoluteFill>
      ) : null}

      {fourIn ? (
        <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center'}}>
          <div style={{display: 'flex', gap: 46, alignItems: 'baseline'}}>
            {FOUR.map((w, i) => (
              <React.Fragment key={w}>
                {i > 0 ? (
                  <span
                    style={{
                      fontSize: 54,
                      color: T.inkFaint,
                      ...riseIn((absSec - 675) * 30, i * 12 - 6, 0),
                    }}
                  >
                    ·
                  </span>
                ) : null}
                <div style={riseIn((absSec - 675) * 30, i * 12, 30)}>
                  <Statement size={94} color={T.warm}>
                    {w}
                  </Statement>
                </div>
              </React.Fragment>
            ))}
          </div>
        </AbsoluteFill>
      ) : null}

      <Vignette />
      <Grain />
      <Caption scene={scene} />
    </Frame>
  );
};
