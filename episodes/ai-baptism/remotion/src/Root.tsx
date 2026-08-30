import React from 'react';
import {Composition, Still} from 'remotion';
import {Episode, SCENE_COMPONENTS} from './Episode';
import {Thumbnail} from './Thumbnail';
import {STORYBOARD} from './lib/beats';
import {FPS} from './theme';

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="Episode"
        component={Episode}
        durationInFrames={STORYBOARD.durationInFrames}
        fps={FPS}
        width={STORYBOARD.width}
        height={STORYBOARD.height}
        defaultProps={{narration: null, music: null}}
      />

      {/* One composition per scene so a single scene can be re-rendered and
          reviewed without waiting on the full 11:50. The scene components read
          their own absolute offset out of the storyboard, so mounting one at
          frame 0 gives exactly the frames it occupies in the episode. */}
      {STORYBOARD.scenes.map((scene) => (
        <Composition
          key={scene.id}
          id={`Scene-${scene.id}`}
          component={SCENE_COMPONENTS[scene.id]}
          durationInFrames={Math.round((scene.endSec - scene.startSec) * FPS)}
          fps={FPS}
          width={STORYBOARD.width}
          height={STORYBOARD.height}
        />
      ))}

      <Still id="Thumbnail" component={Thumbnail} width={1920} height={1080} />
    </>
  );
};
