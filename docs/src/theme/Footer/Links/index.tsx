import React, { type ReactNode } from "react";

import { isMultiColumnFooterLinks } from "@docusaurus/theme-common";
import FooterLinksMultiColumn from "@theme/Footer/Links/MultiColumn";
import FooterLinksSimple from "@theme/Footer/Links/Simple";
import { FooterLink } from "../footer-links";

type Props = {
  links: FooterLink[];
  title: string;
};

export default function FooterLinks({ title, links }: Props): ReactNode {
  return (
    <ul>
      <li>
        <h3>{title}</h3>
      </li>
      {links.map((link) => (
        <li>
          <a href={link.href}>{link.title}</a>
        </li>
      ))}
    </ul>
  );
}
