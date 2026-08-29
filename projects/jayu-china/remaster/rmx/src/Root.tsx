import React from "react";
import { AbsoluteFill, Audio, Composition, Sequence, staticFile } from "remotion";
import ep4 from "./data/ep4.json";
import { EP4_SCENES } from "./scenes/ep4/scenes";
import { Fonts, Grade, Grain, Vignette } from "./kit/layers";
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

export const Root: React.FC = () => (
  <Composition id="EP4" component={EP4Comp}
    durationInFrames={ep4.durationInFrames} fps={ep4.fps} width={1080} height={1920} />
);
