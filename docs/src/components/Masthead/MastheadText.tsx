import React from "react";
import "./MastheadText.css";
import { motion } from "motion/react";

type Props = {};

const MastheadText = (props: Props) => {
  return (
    <div className="masthead">
      <h1 className="title">
        Animations to the{" "}
        <motion.div
          className="highlight"
          initial={{ scale: 1 }}
          animate={{
            scale: [1, 1.2, 1, 1, 1.2, 1],
            y: [0, -10, 0, 0, 0, 0],
          }}
          transition={{ duration: 1.42, repeat: Infinity }}
        >
          beat
        </motion.div>
      </h1>
      <h2 className="subtitle">
        Import MIDI files into Blender and animate objects based on every note
        press
      </h2>
      <div className="buttons">
        <a
          href="https://github.com/whoisryosuke/blender-midi-keyframes/releases"
          className="oat-button"
          target="_blank"
        >
          Download
        </a>
        <a
          href="/blender-midi-motion/docs/getting-started"
          className="oat-button ghost"
        >
          Get Started
        </a>
      </div>
    </div>
  );
};

export default MastheadText;
