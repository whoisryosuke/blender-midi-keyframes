import React from "react";

type Props = {};

const ExportWidget = (props: Props) => {
  return (
    <div className="FrontpageContainer">
      <div className="textbox center">
        <h2>Export to web or games</h2>

        <video
          title="An animated piano imported into an Unreal Engine project rotating on a turn table while playing"
          controls
        >
          <source src="/videos/export-to-unreal.mp4" type="video/mp4" />
          You're missing out on a cool video.
        </video>
      </div>
    </div>
  );
};

export default ExportWidget;
