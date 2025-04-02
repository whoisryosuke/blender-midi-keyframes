import React, { useRef } from "react";
import { Group } from "three";
import Ryoturia from "../Ryoturia/Ryoturia";
import { useFrame } from "@react-three/fiber";
import { lerp } from "three/src/math/MathUtils.js";
import PianoKeys from "../PianoKeys/PianoKeys";

type Props = {};

const ROTATE_START = -Math.PI / 14;
const ROTATE_END = ROTATE_START + 0.001;
const ROTATE_SIDE = -Math.PI / 12;

const RotatedPianoKeys = (props: Props) => {
  const containerRef = useRef<Group>(null);

  useFrame(({ clock }) => {
    const animate = Math.sin(clock.elapsedTime) * 100;
    const animateY = Math.cos(clock.elapsedTime) * 200;

    // containerRef.current.rotation.x =
    //   lerp(ROTATE_START, ROTATE_END, animateY) + 0.5;
    containerRef.current.rotation.z = lerp(ROTATE_START, ROTATE_END, animate);
  });
  return (
    <group ref={containerRef} rotation={[ROTATE_SIDE, 0, ROTATE_START]}>
      <PianoKeys position={[-4, 0, 2.2]} scale={1.5} />
    </group>
  );
};

export default RotatedPianoKeys;
