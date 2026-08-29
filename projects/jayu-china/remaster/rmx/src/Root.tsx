import React from "react";
import { AbsoluteFill, Audio, Composition, Sequence, staticFile } from "remotion";
import ep4 from "./data/ep4.json";
import ep5 from "./data/ep5.json";
import ep6 from "./data/ep6.json";
import ep7 from "./data/ep7.json";
import ep8 from "./data/ep8.json";
import { EP4_SCENES } from "./scenes/ep4/scenes";
import { EP5_SCENES } from "./scenes/ep5/scenes";
import { EP6_SCENES } from "./scenes/ep6/scenes";
import { EP7_SCENES } from "./scenes/ep7/scenes";
import { EP8_SCENES } from "./scenes/ep8/scenes";
import { Fonts, Grade, Grain, Vignette } from "./kit/layers";
import ep9 from "./data/ep9.json";
import { EP9_SCENES } from "./scenes/ep9/scenes";
import ep10 from "./data/ep10.json";
import { EP10_SCENES } from "./scenes/ep10/scenes";
import ep11 from "./data/ep11.json";
import { EP11_SCENES } from "./scenes/ep11/scenes";
import ep12 from "./data/ep12.json";
import { EP12_SCENES } from "./scenes/ep12/scenes";
import s2e1 from "./data/s2e1.json";
import { S2E1_SCENES } from "./scenes/s2e1/scenes";
import { TitleBand, Chip } from "./kit/ui";

type EpData = typeof ep4;

const Episode: React.FC<{ data: EpData; scenes: readonly React.FC<{ dur: number }>[] }> =
({ data, scenes }) => (
  <AbsoluteFill style={{ background: "#0e1018" }}>
    <Fonts />
    {data.scenes.map((sc, i) => {
      const SceneComp = scenes[i];
      return (
        <Sequence key={sc.id} from={sc.from} durationInFrames={sc.dur} name={sc.id}>
          <SceneComp dur={sc.dur} />
          <Sequence from={Math.round(sc.lead * data.fps)} name={`${sc.id}-vo`}>
            <Audio src={staticFile(sc.wav)} />
          </Sequence>
          {sc.chips.map((c) => (
            <Sequence key={c.t} from={c.t} durationInFrames={c.d} name={`chip-${c.t}`}>
              <Chip text={c.text} />
            </Sequence>
          ))}
        </Sequence>
      );
    })}
    <TitleBand l1={data.title[0]} l2={data.title[1]} tag={data.tag}
      world={data.world} intro />
    <Grade /><Grain /><Vignette />
  </AbsoluteFill>
);

const EP4Comp: React.FC = () => <Episode data={ep4} scenes={EP4_SCENES} />;
const EP5Comp: React.FC = () => <Episode data={ep5 as EpData} scenes={EP5_SCENES} />;
const EP6Comp: React.FC = () => <Episode data={ep6 as EpData} scenes={EP6_SCENES} />;
const EP7Comp: React.FC = () => <Episode data={ep7 as EpData} scenes={EP7_SCENES} />;
const EP8Comp: React.FC = () => <Episode data={ep8 as EpData} scenes={EP8_SCENES} />;

const EP9Comp: React.FC = () => <Episode data={ep9 as EpData} scenes={EP9_SCENES} />;

const EP10Comp: React.FC = () => <Episode data={ep10 as EpData} scenes={EP10_SCENES} />;

const EP11Comp: React.FC = () => <Episode data={ep11 as EpData} scenes={EP11_SCENES} />;

const EP12Comp: React.FC = () => <Episode data={ep12 as EpData} scenes={EP12_SCENES} />;

const S2E1Comp: React.FC = () => <Episode data={s2e1 as EpData} scenes={S2E1_SCENES} />;

export const Root: React.FC = () => (
  <>
    <Composition id="EP4" component={EP4Comp}
      durationInFrames={ep4.durationInFrames} fps={ep4.fps} width={1080} height={1920} />
    <Composition id="EP5" component={EP5Comp}
      durationInFrames={ep5.durationInFrames} fps={ep5.fps} width={1080} height={1920} />
    <Composition id="EP6" component={EP6Comp}
      durationInFrames={ep6.durationInFrames} fps={ep6.fps} width={1080} height={1920} />
    <Composition id="EP7" component={EP7Comp}
      durationInFrames={ep7.durationInFrames} fps={ep7.fps} width={1080} height={1920} />
    <Composition id="EP8" component={EP8Comp}
      durationInFrames={ep8.durationInFrames} fps={ep8.fps} width={1080} height={1920} />
    <Composition id="EP9" component={EP9Comp}
      durationInFrames={ep9.durationInFrames} fps={ep9.fps} width={1080} height={1920} />
    <Composition id="EP10" component={EP10Comp}
      durationInFrames={ep10.durationInFrames} fps={ep10.fps} width={1080} height={1920} />
    <Composition id="EP11" component={EP11Comp}
      durationInFrames={ep11.durationInFrames} fps={ep11.fps} width={1080} height={1920} />
    <Composition id="EP12" component={EP12Comp}
      durationInFrames={ep12.durationInFrames} fps={ep12.fps} width={1080} height={1920} />
    <Composition id="S2E1" component={S2E1Comp}
      durationInFrames={s2e1.durationInFrames} fps={s2e1.fps} width={1080} height={1920} />
  </>
);
