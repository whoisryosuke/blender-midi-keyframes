import * as THREE from "three";
import { extend } from "@react-three/fiber";
import { shaderMaterial } from "@react-three/drei";

import vertex from "./shaders/shader.vert";
import fragment from "./shaders/shader.frag";

const PianoKeyMaterial = shaderMaterial(
  {
    time: 0,
    rotation: 0,
    color: new THREE.Color(0.05, 0.2, 0.025),
  },
  vertex,
  fragment
);

// This is the 🔑 that HMR will renew if this file is edited
// It works for THREE.ShaderMaterial as well as for drei/shaderMaterial
// @ts-ignore
PianoKeyMaterial.key = THREE.MathUtils.generateUUID();

export default PianoKeyMaterial;

extend({ PianoKeyMaterial });
