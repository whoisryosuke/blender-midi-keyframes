import React, { type ReactNode } from "react";

import { useThemeConfig } from "@docusaurus/theme-common";
import FooterLinks from "./Links";
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
      <div className="content">
        <div className="logo">
          <img
            src="/blender-midi-motion/img/logo-stacked.svg"
            alt="MIDI Motion logo"
          />
          <p>MIDI animation made easy with one plugin.</p>
        </div>
        <FooterLinks title="Guides" links={LINKS.guides} />
        <FooterLinks title="Resources" links={LINKS.resources} />
        <FooterLinks title="Social" links={LINKS.social} />
      </div>
    </footer>
  );
}

export default React.memo(Footer);
