import React from "react";

type Props = {
  id: string;
  title: string;
  defaultTab: string;
};

const CodepenEmbed = ({ title, id, defaultTab = "js,result" }: Props) => {
  return (
    <div style={{ width: "100%", marginBottom: "16px" }}>
      <script src="https://public.codepenassets.com/embed/index.js" />
      <style>
        {`.cp_embed_wrapper {
            width: 100% !important;
          }`}
      </style>
      <p
        className="codepen"
        data-height="300"
        data-default-tab={defaultTab}
        data-slug-hash={id}
        data-pen-title={title}
        data-user="whoisryosuke"
        style={{
          width: "100%",
          height: "300px",
          boxSizing: "border-box",
          display: "flex",
          flex: 1,
          alignItems: "center",
          justifyContent: "center",
          border: "2px solid",
          margin: "1em 0",
          padding: "1em",
        }}
      >
        <span>
          See the Pen{" "}
          <a href="https://codepen.io/whoisryosuke/pen/azoVVWB">
            P5.js + MotionJS Example
          </a>{" "}
          by Ryosuke (
          <a href="https://codepen.io/whoisryosuke">@whoisryosuke</a>) on{" "}
          <a href="https://codepen.io">CodePen</a>.
        </span>
      </p>
    </div>
  );
};

export default CodepenEmbed;
