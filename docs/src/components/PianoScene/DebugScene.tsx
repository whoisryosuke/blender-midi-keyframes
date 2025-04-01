import { OrbitControls, OrbitControlsProps } from "@react-three/drei";
import { useFrame } from "@react-three/fiber";
import React, { useRef } from "react";
import { Euler, Vector3 } from "three";

type Props = {}; //_y: -1.0473527742131672e-8 //_z: -0.010473253689300936
//2.17, 10.79, -3
//​_x: -1.5707953268052943
//target = 3,0,-3.3
const CENTER = new Vector3(0, 0, 0);

const DebugScene = (props: Props) => {
  const orbitRef = useRef<OrbitControlsProps>(null);
  useFrame(({ camera }) => {
    // Manual
    camera.position.x = 0;
    camera.position.y = 12;
    camera.position.z = 0;
    // orbitRef.current.target.x = 0;
    // orbitRef.current.target.y = 0;
    // orbitRef.current.target.z = 0;

    // Copied from console
    // camera.position.x = 2.17;
    // camera.position.y = 10.79;
    // camera.position.z = -3;
    // const rotation = new Euler(3, 0, -3.3, "XYZ");
    // camera.rotation.x = rotation.x;
    // camera.rotation.y = rotation.y;
    // camera.rotation.z = rotation.z;
    // camera.rotation.x = 3;
    // camera.rotation.y = 0;
    // camera.rotation.z = -3.3;
    // camera.lookAt(CENTER);
    // camera.lookAt(new Vector3(3, 0, -3.3));
    // orbitRef.current.target.x = 3;
    // orbitRef.current.target.y = 0;
    // orbitRef.current.target.z = -3.3;
    // console.log("cam", camera.position, camera.rotation);
    // console.log("orbit", orbitRef.current.target);
  });
  return (
    <>
      <OrbitControls ref={orbitRef} />
    </>
  );
};

export default DebugScene;
