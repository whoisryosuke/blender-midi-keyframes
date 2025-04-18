import React from "react";
import "./GetCreativeWidget.css";

type Props = {};

const GetCreativeWidget = (props: Props) => {
  return (
    <div className="FrontpageContainer GetCreative">
      <div className="container">
        <div className="box">
          <div className="content">
            <h2>Get creative!</h2>
            <h3>Let your music flow</h3>
          </div>

          <a href="/docs/resources/showcase" className="oat-button ghost">
            Browse our showcase for inspiration
          </a>

          <img
            src="/img/frontpage/get-creative-curved-piano.png"
            aria-hidden="true"
            className="spacer"
          />
        </div>

        <img
          src="/img/frontpage/get-creative-curved-piano.png"
          alt="The settings UI panel for the plugin in Blender"
          className="piano"
        />
      </div>
    </div>
  );
};

export default GetCreativeWidget;
