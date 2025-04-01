import { Canvas } from "@react-three/fiber";
import React from "react";

type Props = {};

const Scene = (props: Props) => {
  return (
    <Canvas>
      <ambientLight position={[0, 3, 0]} intensity={1} />
      <mesh>
        <boxGeometry args={[1, 1]} />
        <meshPhysicalMaterial color="blue" />
      </mesh>
    </Canvas>
  );
};

export default Scene;
