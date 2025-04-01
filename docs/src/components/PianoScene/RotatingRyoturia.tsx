import React, { useRef } from "react";
import { Group } from "three";
import Ryoturia from "../Ryoturia/Ryoturia";
import { useFrame } from "@react-three/fiber";
import { lerp } from "three/src/math/MathUtils.js";

type Props = {};

const ROTATE_START = -Math.PI / 10;
const ROTATE_END = ROTATE_START + 0.001;

const RotatingRyoturia = (props: Props) => {
  const containerRef = useRef<Group>(null);

  useFrame(({ clock }) => {
    const animate = Math.sin(clock.elapsedTime) * 100;
    const animateY = Math.cos(clock.elapsedTime) * 200;

    // containerRef.current.rotation.x =
    //   lerp(ROTATE_START, ROTATE_END, animateY) + 0.5;
    containerRef.current.rotation.z = lerp(ROTATE_START, ROTATE_END, animate);
  });
  return (
    <group ref={containerRef} rotation={[0, 0, ROTATE_START]}>
      <Ryoturia position={[0, 0, 4.2]} />
    </group>
  );
};

export default RotatingRyoturia;
