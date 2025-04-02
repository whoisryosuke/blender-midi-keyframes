import {
  Environment,
  Lightformer,
  OrbitControls,
  Preload,
  Stats,
} from "@react-three/drei";
import { Canvas } from "@react-three/fiber";
import React from "react";
import DebugScene from "./DebugScene";
import RotatingRyoturia from "./RotatingRyoturia";
import RotatedPianoKeys from "./RotatedPianoKeys";

type Props = {};

const Scene = (props: Props) => {
  return (
    <Canvas style={{ pointerEvents: "none" }}>
      {/* <ambientLight position={[0, 3, 0]} intensity={1} /> */}
      {/* <ambientLight position={[3, 3, 3]} intensity={0.5} /> */}
      <Environment
        // background
        files="./img/studio_small_08_1k.hdr"
        {...props}
      >
        {/* Extra space lights if needed */}
      </Environment>
      <RotatedPianoKeys />

      <DebugScene />
    </Canvas>
  );
};

export default Scene;
