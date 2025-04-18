import type { ReactNode } from "react";
import useDocusaurusContext from "@docusaurus/useDocusaurusContext";
import Layout from "@theme/Layout";
import Wrapper from "../components/Wrapper/Wrapper";
import Frontpage from "../components/Frontpage/Frontpage";

export default function Home(): ReactNode {
  const { siteConfig } = useDocusaurusContext();
  return (
    <Layout
      title={`MIDI animation in Blender made easy`}
      description="Description will go into a meta tag in <head />"
    >
      <Wrapper>
        <Frontpage />
      </Wrapper>
    </Layout>
  );
}
