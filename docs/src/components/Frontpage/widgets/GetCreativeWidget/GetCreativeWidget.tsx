import React from "react";
import "./GetCreativeWidget.css";
import ScrollFadeUpRepeat from "@site/src/components/animations/ScrollFadeUp";
import { motion } from "motion/react";

type Props = {};

const GetCreativeWidget = (props: Props) => {
  return (
    <div className="FrontpageContainer GetCreative">
      <div className="container">
        <div className="box">
          <div className="content">
            <h2>Get creative!</h2>
            <h3>Let your music flow</h3>
          </div>

          <a href="/docs/resources/showcase" className="oat-button ghost">
            Browse our showcase for inspiration
          </a>

          <img
            src="/img/frontpage/get-creative-curved-piano.png"
            aria-hidden="true"
            className="spacer"
          />
        </div>

        <motion.div
          className="piano"
          initial={{
            opacity: 0,
            y: 100,
          }}
          whileInView={{
            opacity: 1,
            y: 0,
          }}
        >
          <motion.img
            src="/img/frontpage/get-creative-curved-piano.png"
            alt="The settings UI panel for the plugin in Blender"
            initial={{
              y: -50,
            }}
            animate={{
              y: 50,
            }}
            transition={{
              delay: 1,
              duration: 4.2,
              repeat: Infinity,
              repeatType: "mirror",
            }}
          />
        </motion.div>
      </div>
    </div>
  );
};

export default GetCreativeWidget;
