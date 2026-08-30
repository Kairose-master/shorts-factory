import React from 'react';
import {AbsoluteFill, interpolate} from 'remotion';
import {Frame, Grain, Vignette} from '../components/Frame';
import {Caption} from '../components/Caption';
import {AvatarPlate} from '../components/AvatarPlate';
import {Statement} from '../components/Type';
import {getScene, useSceneClock} from '../lib/beats';
import {riseIn} from '../lib/anim';
import {T} from '../theme';

const scene = getScene('S05');

/**
 * The structural turn of the episode: the old questions do not get refuted,
 * they get moved aside and dimmed. That is the honest gesture — the script
 * says they are important — and it is also the better piece of motion.
 */
export const S05_QuestionSwap: React.FC = () => {
  const {absSec} = useSceneClock(scene);

  const oldIn = interpolate(absSec, [154, 158], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const second = interpolate(absSec, [157.5, 160], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  // Slide left + dim, not erase.
  const shift = interpolate(absSec, [170, 174], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: (t) => 1 - Math.pow(1 - t, 3),
  });
  const newQ = interpolate(absSec, [180, 184], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  const avatarOpacity = interpolate(absSec, [152, 155], [1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <Frame>
      {avatarOpacity > 0.01 ? (
        <AbsoluteFill style={{opacity: avatarOpacity}}>
          <AvatarPlate sceneId="S05" role="presenter" />
        </AbsoluteFill>
      ) : null}

      <AbsoluteFill
        style={{
          alignItems: 'center',
          justifyContent: 'center',
          transform: `translateX(${-shift * 520}px)`,
          opacity: oldIn * (1 - shift * 0.8),
        }}
      >
        <div style={{display: 'flex', flexDirection: 'column', gap: 34}}>
          <Statement size={62} color={T.inkDim}>
            AI에게 의식이 있는가?
          </Statement>
          <div style={{opacity: second}}>
            <Statement size={62} color={T.inkDim}>
              AI도 사람인가?
            </Statement>
          </div>
          {shift > 0.05 ? (
            <div style={{opacity: shift}}>
              <Statement size={62} color={T.cold}>
                AI에게 세례를 줄 수 있는가?
              </Statement>
            </div>
          ) : null}
        </div>
      </AbsoluteFill>

      {newQ > 0.01 ? (
        <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center'}}>
          <div style={{...riseIn((absSec - 180) * 30, 0, 44), opacity: newQ}}>
            <Statement size={82} color={T.warm}>
              {'이 존재와 하나님 사이에는\n무슨 일이 있었는가?'}
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
