import React from 'react';
import {AbsoluteFill, Audio, Sequence, staticFile} from 'remotion';
import {STORYBOARD} from './lib/beats';
import {SceneTransition} from './components/Transition';
import {FPS, loadFonts, T} from './theme';

import {S01_ColdOpenChurch} from './scenes/S01_ColdOpenChurch';
import {S02_ObjectionStack} from './scenes/S02_ObjectionStack';
import {S03_DecadeTimeline} from './scenes/S03_DecadeTimeline';
import {S04_FaithDetector} from './scenes/S04_FaithDetector';
import {S05_QuestionSwap} from './scenes/S05_QuestionSwap';
import {S05B_BaptismTraditions} from './scenes/S05B_BaptismTraditions';
import {S06_PerfectDuplicate} from './scenes/S06_PerfectDuplicate';
import {S07_EventTimeline} from './scenes/S07_EventTimeline';
import {S08_Incarnation} from './scenes/S08_Incarnation';
import {S09_JesusDuplicate} from './scenes/S09_JesusDuplicate';
import {S10_StatSheet} from './scenes/S10_StatSheet';
import {S11_AIConfession} from './scenes/S11_AIConfession';
import {S12_Conclusion} from './scenes/S12_Conclusion';
import {S13_EndCallback} from './scenes/S13_EndCallback';

export const SCENE_COMPONENTS: Record<string, React.FC> = {
  S01: S01_ColdOpenChurch,
  S02: S02_ObjectionStack,
  S03: S03_DecadeTimeline,
  S04: S04_FaithDetector,
  S05: S05_QuestionSwap,
  S05B: S05B_BaptismTraditions,
  S06: S06_PerfectDuplicate,
  S07: S07_EventTimeline,
  S08: S08_Incarnation,
  S09: S09_JesusDuplicate,
  S10: S10_StatSheet,
  S11: S11_AIConfession,
  S12: S12_Conclusion,
  S13: S13_EndCallback,
};

export type EpisodeProps = {
  /** Narration WAV under public/audio/. Absent until the audio stage has run. */
  narration?: string | null;
  /** Music bed under public/audio/. */
  music?: string | null;
};

export const Episode: React.FC<EpisodeProps> = ({narration, music}) => {
  loadFonts();

  return (
    <AbsoluteFill style={{backgroundColor: T.bg}}>
      {STORYBOARD.scenes.map((scene, i) => {
        const Comp = SCENE_COMPONENTS[scene.id];
        if (!Comp) {
          throw new Error(`no component registered for scene ${scene.id}`);
        }
        const prev = STORYBOARD.scenes[i - 1];
        return (
          <Sequence
            key={scene.id}
            name={`${scene.id} · ${scene.title}`}
            from={Math.round(scene.startSec * FPS)}
            durationInFrames={Math.round((scene.endSec - scene.startSec) * FPS)}
          >
            <SceneTransition scene={scene} prevTransition={prev?.transitionOut}>
              <Comp />
            </SceneTransition>
          </Sequence>
        );
      })}

      {/* Audio is attached at episode level, not per scene: the mix is one
          continuous track built against the storyboard, so splitting it per
          scene would let drift accumulate at every seam. `narration` is
          normally the MIXED track — narration and bed already balanced and
          ducked by scripts/assemble_audio.py — so `music` stays unset rather
          than layering a second bed over it. */}
      {narration ? <Audio src={staticFile(`audio/${narration}`)} /> : null}
      {music ? <Audio src={staticFile(`audio/${music}`)} volume={0.16} /> : null}
    </AbsoluteFill>
  );
};
