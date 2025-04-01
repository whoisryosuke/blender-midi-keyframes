import React, { lazy, Suspense } from "react";

const Scene = lazy(() => import("./Scene"));

type Props = {};

const PianoScene = (props: Props) => {
  return (
    <Suspense>
      <Scene />
    </Suspense>
  );
};

export default PianoScene;
