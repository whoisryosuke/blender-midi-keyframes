import { useFrame } from "@react-three/fiber";
import { JSX, useMemo, useRef } from "react";
import PianoKeyMaterial from "./PianoKeyMaterial";
import { Color, Mesh, MeshPhysicalMaterial } from "three";

type Props = Partial<JSX.IntrinsicElements["mesh"]> & {
  black?: boolean;
};

const PRESSED_COLOR = new Color("#002EFF");

const PianoKey = ({ black = false, ...props }: Props) => {
  const meshRef = useRef<Mesh>(null);
  const keyBaseColor = useMemo(
    () => (black ? new Color("#000000") : new Color("#FFFFFF")),
    [black]
  );

  useFrame((state, delta) => {
    if (meshRef.current.material) {
      const material = meshRef.current.material as MeshPhysicalMaterial;
      //   meshRef.current.material.uniforms.rotation.value =
      //     meshRef.current.rotation.x;
      material.color =
        meshRef.current.rotation.x > 0 ? PRESSED_COLOR : keyBaseColor;
    }
  });

  return (
    <mesh ref={meshRef} {...props}>
      {/* @ts-ignore */}
      <meshPhysicalMaterial color={keyBaseColor} />
    </mesh>
  );
};
export default PianoKey;
