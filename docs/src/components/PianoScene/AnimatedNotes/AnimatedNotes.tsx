import React from "react";
import "./AnimatedNotes.css";
import DAWNotes from "./DAWNotes";

type Props = {};

const AnimatedNotes = (props: Props) => {
  return (
    <div className="AnimatedNotesContainer">
      <DAWNotes />
      <div>Blender Timeline</div>
    </div>
  );
};

export default AnimatedNotes;
