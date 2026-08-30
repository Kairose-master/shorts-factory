import React from 'react';
import {AbsoluteFill, interpolate} from 'remotion';
import {Frame, Grain, Vignette} from '../components/Frame';
import {Caption} from '../components/Caption';
import {AvatarPlate} from '../components/AvatarPlate';
import {Statement} from '../components/Type';
import {getScene, useSceneClock} from '../lib/beats';
import {breathe, riseIn} from '../lib/anim';
import {T} from '../theme';

const scene = getScene('S11');

/**
 * The one place in the episode where a long held shot is right.
 *
 * Everywhere else the brief forbids more than 12 static seconds; here the
 * whole 68 seconds sit on one face, because the scene's content is a machine
 * admitting it cannot verify its own interior, and cutting away from that
 * would let the viewer off the hook. It is not static, though — the frame
 * breathes and the key light drifts, so it reads as held rather than frozen.
 *
 * VOICE: this scene is the only one rendered with the `ai` voice. If the audio
 * stage hands back a narrator-voiced take for S11, that is a QA failure, not a
 * cosmetic note — the argument depends on hearing a second speaker.
 */
const PULL_QUOTES = [
  {text: '"저는 하나님을 사랑합니다"', at: 571, dur: 5},
  {text: '출력인가, 사건인가', at: 586, dur: 4},
  {text: '기록을 가진 것 ≠ 그 시간을 살아온 것', at: 599, dur: 7},
];

export const S11_AIConfession: React.FC = () => {
  const {absSec, frame} = useSceneClock(scene);

  const b = breathe(frame, 0.01, 13);
  // Key light drifts across the whole scene — the only large-scale motion.
  const drift = interpolate(absSec, [556, 624], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  const quote = PULL_QUOTES.find((q) => absSec >= q.at && absSec < q.at + q.dur);

  return (
    <Frame bg="#040405">
      <AbsoluteFill style={{transform: `scale(${b})`}}>
        <AvatarPlate sceneId="S11" role="ai" />
      </AbsoluteFill>

      {/* Drifting key. Near-black frame, one side lit. */}
      <AbsoluteFill
        style={{
          background: `radial-gradient(ellipse 30% 40% at ${
            40 + drift * 16
          }% ${42 + drift * 4}%, ${T.cold}1A 0%, transparent 68%)`,
          pointerEvents: 'none',
        }}
      />

      {quote ? (
        <AbsoluteFill
          style={{alignItems: 'center', justifyContent: 'flex-start', paddingTop: 168}}
        >
          <div style={riseIn((absSec - quote.at) * 30, 0, 20)}>
            <Statement size={62} color="#7FA9D6" weight={700}>
              {quote.text}
            </Statement>
          </div>
        </AbsoluteFill>
      ) : null}

      <Vignette strength={0.78} />
      <Grain opacity={0.07} />
      <Caption scene={scene} />
    </Frame>
  );
};
