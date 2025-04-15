import React from "react";
import ControlAnimationBlock from "./ControlAnimationBlock";
import "./ControlAnimations.css";

type Props = {};

const ControlAnimations = (props: Props) => {
  return (
    <div className="FrontpageContainer ControlAnimations">
      <div className="textbox">
        <h2>
          <span className="highlight">Control</span> your
          <br /> animations
        </h2>
        <div className="blocks">
          <ControlAnimationBlock
            icon="select_track"
            title="Select Track"
            subtitle="Import single or multi-track MIDI files"
          />
          <ControlAnimationBlock
            icon="select_octave"
            title="Select Octave"
            subtitle="Isolate to specific octave or condense all of them into one track"
          />
          <ControlAnimationBlock
            icon="animation_type"
            title="Move, Scale, or Rotate objects"
            subtitle="For keyframe animations"
          />
          <ControlAnimationBlock
            icon="animation_mode"
            title="Use Keyframes or Actions"
            subtitle="Assign action animations for each key"
          />
          <ControlAnimationBlock
            icon="export"
            title="Export animation to GLTF"
            subtitle="Import into your favorite 3D engine"
          />
          <ControlAnimationBlock
            icon="object"
            title="Animate any object"
            subtitle="Assign any object to any piano key"
          />
        </div>
      </div>

      <img
        src="/img/frontpage/panel.png"
        alt="The settings UI panel for the plugin in Blender"
      />
    </div>
  );
};

export default ControlAnimations;
