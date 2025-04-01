  uniform float time;
  uniform float rotation;
  uniform vec3 color;
  varying vec2 vUv;
  varying float vPressed;
  #pragma glslify: random = require(glsl-random)

float map(float value, float min1, float max1, float min2, float max2) {
  return min2 + (value - min1) * (max2 - min2) / (max1 - min1);
}

  void main() {
    float pressedAmount = map(rotation, 0.0, 0.03, 0.0, 1.0);
    vec3 pressedColor = vec3(0.0,0.0,1.0);
    vec3 keyColor = mix(color, pressedColor, pressedAmount);
    gl_FragColor.rgba = vec4(keyColor, 1.0);
    // gl_FragColor.rgba = vec4(color * vPressed, 1.0);
    // gl_FragColor.rgba = vec4(vec3(0.), 1.);
  }
