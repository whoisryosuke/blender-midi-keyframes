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
};

const ControlAnimationBlock = ({ title, subtitle, icon }: Props) => {
  const Icon = ICONS[icon];
  return (
    <div className="block">
      <div className="content">
        <Icon size={96} />
        <h3>{title}</h3>
        <p>{subtitle}</p>
      </div>
    </div>
  );
};

export default ControlAnimationBlock;
