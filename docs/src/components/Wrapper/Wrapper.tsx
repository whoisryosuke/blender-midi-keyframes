import React, { PropsWithChildren } from "react";

type Props = {};

const Wrapper = ({ children }: PropsWithChildren<Props>) => {
  return (
    <div>
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link
          rel="preconnect"
          href="https://fonts.gstatic.com"
          crossOrigin="anonymous"
        />
        <link
          href="https://fonts.googleapis.com/css2?family=Inter+Tight:ital,wght@0,100..900;1,100..900&display=swap"
          rel="stylesheet"
        ></link>
      </head>
      {children}
    </div>
  );
};

export default Wrapper;
