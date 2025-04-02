import React, { PropsWithChildren } from "react";

type Props = {};

const Wrapper = ({ children }: PropsWithChildren<Props>) => {
  return <div>{children}</div>;
};

export default Wrapper;
