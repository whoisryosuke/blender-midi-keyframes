import React, { type ReactNode } from "react";

import { useThemeConfig } from "@docusaurus/theme-common";
import FooterLinks from "./Links";
import FooterLogo from "@theme/Footer/Logo";
import FooterCopyright from "@theme/Footer/Copyright";
import FooterLayout from "@theme/Footer/Layout";
import "./Footer.css";
import LINKS from "./footer-links";

function Footer(): ReactNode {
  const { footer } = useThemeConfig();
  if (!footer) {
    return null;
  }
  const { copyright, links, logo, style } = footer;

  return (
    <footer className="Footer">
      <div className="logo">
        <img src="/img/logo-stacked.svg" alt="MIDI Motion logo" />
        <p>MIDI animation made easy with one plugin.</p>
      </div>
      <FooterLinks title="Guides" links={LINKS.guides} />
      <FooterLinks title="Resources" links={LINKS.resources} />
      <FooterLinks title="Social" links={LINKS.social} />
    </footer>
  );
}

export default React.memo(Footer);
