import React, { useRef } from "react";
import { Group } from "three";
import Ryoturia from "../Ryoturia/Ryoturia";
import { useFrame } from "@react-three/fiber";
import { lerp } from "three/src/math/MathUtils.js";
import PianoKeys from "../PianoKeys/PianoKeys";
import { spring } from "motion";

type Props = {};

const ROTATE_START = -Math.PI / 14;
const ROTATE_END = ROTATE_START + 0.001;
const ROTATE_SIDE = -Math.PI / 12;

const RotatedPianoKeys = (props: Props) => {
  const containerRef = useRef<Group>(null);
  const springRef = useRef(spring({ keyframes: [0.5, 1], stiffness: 400 }));

  useFrame(({ clock }) => {
    const animate = Math.sin(clock.elapsedTime) * 100;
    const animateY = Math.cos(clock.elapsedTime) * 200;

    // containerRef.current.rotation.x =
    //   lerp(ROTATE_START, ROTATE_END, animateY) + 0.5;
    containerRef.current.rotation.z = lerp(ROTATE_START, ROTATE_END, animate);

    const scaleDuration = 1; // in seconds

    const { value, done } = springRef.current.next(clock.elapsedTime * 1000);

    const animatedScale = value;
    // const animatedScale = lerp(
    //   0.5,
    //   1,
    //   Math.min(clock.elapsedTime / scaleDuration, 1)
    // );
    containerRef.current.scale.x = animatedScale;
    containerRef.current.scale.y = animatedScale;
    containerRef.current.scale.z = animatedScale;
  });
  return (
    <group
      ref={containerRef}
      scale={[0, 0, 0]}
      rotation={[ROTATE_SIDE, 0, ROTATE_START]}
    >
      <PianoKeys position={[-4, 0, 2.2]} scale={1.5} />
    </group>
  );
};

export default RotatedPianoKeys;
