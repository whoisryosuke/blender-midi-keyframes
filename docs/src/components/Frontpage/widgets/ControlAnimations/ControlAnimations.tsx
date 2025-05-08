import React from "react";
import ControlAnimationBlock from "./ControlAnimationBlock";
import "./ControlAnimations.css";
import ScrollFadeUpRepeat from "@site/src/components/animations/ScrollFadeUp";
import { motion } from "motion/react";

type Props = {};

const ControlAnimations = (props: Props) => {
  return (
    <div className="FrontpageContainer ControlAnimations">
      <div className="container">
        <div className="textbox">
          <ScrollFadeUpRepeat>
            <h2>
              <span className="highlight">Control</span> your animations
            </h2>
          </ScrollFadeUpRepeat>
          <div className="blocks">
            <ControlAnimationBlock
              icon="select_track"
              title="Select Track"
              subtitle="Import single or multi-track MIDI files"
              index={0}
            />
            <ControlAnimationBlock
              icon="select_octave"
              title="Select Octave"
              subtitle="Isolate to specific octave or condense all of them into one track"
              index={1}
            />
            <ControlAnimationBlock
              icon="animation_type"
              title="Scale, Rotate, or Move objects"
              subtitle="For keyframe animations"
              index={2}
            />
            <ControlAnimationBlock
              icon="animation_mode"
              title="Use Keyframes or Actions"
              subtitle="Assign action animations for each key"
              index={3}
            />
            <ControlAnimationBlock
              icon="export"
              title="Export animation to GLTF"
              subtitle="Import into your favorite 3D engine"
              index={4}
            />
            <ControlAnimationBlock
              icon="object"
              title="Animate any object"
              subtitle="Assign any object to any piano key"
              index={5}
            />
          </div>
        </div>

        <motion.img
          src="/blender-midi-motion/img/frontpage/panel.png"
          alt="The settings UI panel for the plugin in Blender"
          initial={{
            opacity: 0,
            x: 42,
          }}
          whileInView={{
            opacity: 1,
            x: 0,
          }}
          transition={{
            duration: 1,
          }}
          viewport={{ once: true }}
        />
      </div>
    </div>
  );
};

export default ControlAnimations;
