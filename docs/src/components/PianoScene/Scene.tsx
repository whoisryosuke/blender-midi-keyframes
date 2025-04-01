import { OrbitControls, Preload, Stats } from "@react-three/drei";
import { Canvas } from "@react-three/fiber";
import React from "react";
import DebugScene from "./DebugScene";
import RotatingRyoturia from "./RotatingRyoturia";

type Props = {};

const Scene = (props: Props) => {
  return (
    <Canvas>
      <ambientLight position={[0, 3, 0]} intensity={1} />
      <RotatingRyoturia />

      <DebugScene />
    </Canvas>
  );
};

export default Scene;
