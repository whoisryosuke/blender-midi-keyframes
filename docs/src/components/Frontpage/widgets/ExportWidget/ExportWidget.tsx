import React from "react";
import "./ExportWidget.css";
import ScrollFadeUpRepeat from "@site/src/components/animations/ScrollFadeUp";

type Props = {};

const ExportWidget = (props: Props) => {
  return (
    <div className="FrontpageContainer ExportWidget">
      <div className="container">
        <div className="textbox center">
          <ScrollFadeUpRepeat>
            <h2 className="subtitle">Export your animation to</h2>
          </ScrollFadeUpRepeat>
          <div className="buttons">
            <ScrollFadeUpRepeat delay={1}>
              <a href="/docs/exporting/unreal" className="oat-button">
                Unreal Engine
              </a>
            </ScrollFadeUpRepeat>
            <ScrollFadeUpRepeat delay={1.5}>
              <a href="/docs/exporting/godot" className="oat-button ghost">
                Godot
              </a>
            </ScrollFadeUpRepeat>
            <ScrollFadeUpRepeat delay={2}>
              <a href="/docs/exporting/threejs" className="oat-button ghost">
                ThreeJS
              </a>
            </ScrollFadeUpRepeat>
          </div>

          <ScrollFadeUpRepeat delay={1.2}>
            <video
              title="An animated piano imported into an Unreal Engine project rotating on a turn table while playing"
              controls
            >
              <source
                src="/blender-midi-motion/videos/export-to-unreal.mp4"
                type="video/mp4"
              />

              <img
                src="/img/frontpage/export-unreal-engine.png"
                alt="An animated piano in Unreal Engine imported from a GLTF file"
              />
            </video>
          </ScrollFadeUpRepeat>
          <a
            href="/docs/category/export-animations"
            className="oat-button ghost"
          >
            Read our export guides
          </a>
        </div>
      </div>
    </div>
  );
};

export default ExportWidget;
