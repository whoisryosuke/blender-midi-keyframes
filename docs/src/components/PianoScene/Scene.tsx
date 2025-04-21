import {
  Environment,
  Lightformer,
  OrbitControls,
  Preload,
  Stats,
} from "@react-three/drei";
import { Canvas } from "@react-three/fiber";
import React, { useRef } from "react";
import DebugScene from "./DebugScene";
import RotatedPianoKeys from "./RotatedPianoKeys";

type Props = {};

const Scene = (props: Props) => {
  return (
    <Canvas style={{ pointerEvents: "none" }}>
      <pointLight position={[5, 3, 5]} intensity={1.5} castShadow />
      <directionalLight position={[0, 4, 4]} intensity={5} />
      <pointLight position={[-5, 0, 2]} intensity={0.7} />
      <directionalLight position={[0, 3, -5]} intensity={1} />
      <ambientLight position={[0, 0, 0]} intensity={1} />
      <RotatedPianoKeys />

      <DebugScene />
    </Canvas>
  );
};

export default Scene;
