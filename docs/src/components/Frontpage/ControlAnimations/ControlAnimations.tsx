import React from "react";
import "./ControlAnimations.css";

type Props = {};

const ControlAnimations = (props: Props) => {
  return (
    <div className="container">
      <div className="textbox">
        <h2>Control your animations</h2>
        <ul>
          <li>Select MIDI track</li>
          <li>Select octave (or condense all)</li>
          <li>Change animation type (move, rotate, or scale)</li>
          <li>Change animation parameters (distance, axis)</li>
        </ul>
      </div>

      <img
        src="/img/frontpage/panel.png"
        alt="The settings UI panel for the plugin in Blender"
      />
    </div>
  );
};

export default ControlAnimations;
