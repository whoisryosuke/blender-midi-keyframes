import React from "react";
import MastheadText from "../Masthead/MastheadText";
import AnimatedNotes from "../PianoScene/AnimatedNotes/AnimatedNotes";
import PianoScene from "../PianoScene/PianoScene";
import ControlAnimations from "./widgets/ControlAnimations/ControlAnimations";
import "./shared/FrontpageWidgets.css";
import ExportWidget from "./ExportWidget";

type Props = {};

const Frontpage = (props: Props) => {
  return (
    <main style={{ display: "flex", flex: 1, flexDirection: "column" }}>
      <MastheadText />
      <div
        style={{
          width: "100%",
          height: 600,
          marginTop: -50,
          position: "relative",
        }}
      >
        <AnimatedNotes />
        <PianoScene />
      </div>
      <ControlAnimations />
      <ExportWidget />
    </main>
  );
};

export default Frontpage;
