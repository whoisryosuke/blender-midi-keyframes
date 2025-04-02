import type { ReactNode } from "react";
import clsx from "clsx";
import Link from "@docusaurus/Link";
import useDocusaurusContext from "@docusaurus/useDocusaurusContext";
import Layout from "@theme/Layout";
import HomepageFeatures from "@site/src/components/HomepageFeatures";
import Heading from "@theme/Heading";

import styles from "./index.module.css";
import PianoScene from "../components/PianoScene/PianoScene";
import MastheadText from "../components/Masthead/MastheadText";
import Wrapper from "../components/Wrapper/Wrapper";
import ControlAnimations from "../components/Frontpage/ControlAnimations/ControlAnimations";
import AnimatedNotes from "../components/PianoScene/AnimatedNotes/AnimatedNotes";

export default function Home(): ReactNode {
  const { siteConfig } = useDocusaurusContext();
  return (
    <Layout
      title={`Hello from ${siteConfig.title}`}
      description="Description will go into a meta tag in <head />"
    >
      <Wrapper>
        <main style={{ display: "flex", flex: 1, flexDirection: "column" }}>
          <MastheadText />
          <div
            style={{
              width: "100%",
              height: 600,
              marginTop: -50,
              position: "relative",
            }}
          >
            <AnimatedNotes />
            <PianoScene />
          </div>
          <ControlAnimations />
        </main>
      </Wrapper>
    </Layout>
  );
}
