import { motion } from "motion/react";
import React, { PropsWithChildren } from "react";

type Props = {
  delay?: number;
};

const ScrollFadeUpRepeat = ({
  children,
  delay = 0,
  ...props
}: PropsWithChildren<Props>) => {
  return (
    <motion.div
      initial={{
        opacity: 0,
        y: 42,
      }}
      whileInView={{
        opacity: 1,
        y: 0,
      }}
      transition={{
        duration: 1,
        delay,
      }}
      viewport={{ once: true }}
      {...props}
    >
      {children}
    </motion.div>
  );
};

export default ScrollFadeUpRepeat;
