import { useFrame } from "@react-three/fiber";
import { JSX, useMemo, useRef } from "react";
import { Color, Mesh, MeshPhysicalMaterial } from "three";

type Props = Partial<JSX.IntrinsicElements["mesh"]> & {};

// This is pulled from the `<Ryoturia />` component, each mesh has a hard-coded position
const START_DISTANCE = 1.453;
const BASE_COLOR = new Color("#FFFFFF");
const PRESSED_COLOR = new Color("#002EFF");
// Because floats are inprecise, we can't just say "less than" or "equals"
// since the object may fluctuate +- 0.001
// so we check if it's passed a threshold (this buffer)
const FLOAT_BUFFER = 0.05;

const DrumpadButton = ({ material, ...props }: Props) => {
  const meshRef = useRef<Mesh>(null);
  const materialUnique = useMemo(() => material.clone(), []);

  useFrame((state, delta) => {
    if (meshRef.current.material) {
      const material = meshRef.current.material as MeshPhysicalMaterial;
      //   meshRef.current.material.uniforms.rotation.value =
      //     meshRef.current.rotation.x;
      material.color =
        meshRef.current.position.y < START_DISTANCE - FLOAT_BUFFER
          ? PRESSED_COLOR
          : BASE_COLOR;
    }
  });

  return <mesh ref={meshRef} material={materialUnique} {...props} />;
};
export default DrumpadButton;
