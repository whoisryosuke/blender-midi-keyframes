varying vec2 vUv;
varying float vPressed;
void main() {
  vUv = uv;
  float pressed = 0.0;
  // if(modelViewMatrix[1].z > 1.0) {
  //   pressed = 1.0;
  // }

  mat3 rotationMatrix = mat3(modelViewMatrix);
  vec3 rotatedPos = rotationMatrix * position;

  if (rotatedPos.z > 4.0) {
    pressed = 1.0;
  }

  vPressed = pressed;
  gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
}
