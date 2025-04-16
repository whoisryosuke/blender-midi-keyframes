import React from "react";
import DAWExample from "./DAWExample";
import "./ImportNotesWidget.css";

type Props = {};

const ImportNotesWidget = (props: Props) => {
  return (
    <div className="FrontpageContainer ImportNotes">
      <div className="container">
        <DAWExample />
        <div className="textbox">
          <h3 className="subtitle">Import notes as</h3>
          <h2>Keyframes or Actions</h2>
        </div>
      </div>
    </div>
  );
};

export default ImportNotesWidget;
