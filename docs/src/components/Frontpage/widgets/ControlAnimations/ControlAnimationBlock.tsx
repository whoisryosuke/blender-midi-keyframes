import ScrollFadeUpRepeat from "@site/src/components/animations/ScrollFadeUp";
import { motion } from "motion/react";
import React from "react";
import {
  BiListOl,
  BiMenuAltLeft,
  BiMove,
  BiCaretRightSquare,
  BiFile,
  BiGhost,
} from "react-icons/bi";

const ICONS = {
  select_track: BiListOl,
  select_octave: BiMenuAltLeft,
  animation_type: BiMove,
  animation_mode: BiCaretRightSquare,
  export: BiFile,
  object: BiGhost,
};

type Props = {
  title: string;
  subtitle: string;
  icon: keyof typeof ICONS;
  index: number;
};

[
  { scale: 1.3 },
  { scale: 1 },
  { rotate: 180 },
  { rotate: 0 },
  { y: -10 },
  { y: 0 },
];
const ControlAnimationBlock = ({ title, subtitle, icon, index }: Props) => {
  const Icon = ICONS[icon];
  return (
    <div className="block">
      <ScrollFadeUpRepeat className="content" delay={(index + 1) * 0.3}>
        <motion.div
          whileHover={
            icon == "animation_type"
              ? {
                  scale: [null, 1.3, 1, null, null, null, null],
                  rotate: [null, null, null, 180, 0, null, null],
                  y: [null, null, null, null, null, -10, 0],
                }
              : {
                  y: -10,
                }
          }
          transition={{
            duration: icon == "animation_type" ? 2 : 0.3,
          }}
        >
          <Icon size={96} />
        </motion.div>
        <h3>{title}</h3>
        <p>{subtitle}</p>
      </ScrollFadeUpRepeat>
    </div>
  );
};

export default ControlAnimationBlock;
