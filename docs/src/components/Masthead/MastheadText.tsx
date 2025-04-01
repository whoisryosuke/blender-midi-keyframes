import React from "react";
import "./MastheadText.css";

type Props = {};

const MastheadText = (props: Props) => {
  return (
    <div className="masthead">
      <h1 className="title">
        Animations to the <span className="highlight">beat</span>
      </h1>
      <h2 className="subtitle">
        Import MIDI files into Blender and animate objects based on every note
        press
      </h2>
      <div className="buttons">
        <a href="#" className="oat-button">
          Download
        </a>
        <a href="#" className="oat-button ghost">
          See Examples
        </a>
      </div>
    </div>
  );
};

export default MastheadText;
