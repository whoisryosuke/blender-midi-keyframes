export type FooterLink = {
  title: string;
  href: string;
};

const GUIDES: FooterLink[] = [
  {
    href: "#",
    title: "Installation",
  },
  {
    href: "#",
    title: "Getting Started",
  },
  {
    href: "#",
    title: "Exporting to GLTF",
  },
  {
    href: "#",
    title: "Ableton Live Workflow",
  },
];

const RESOURCES: FooterLink[] = [
  {
    href: "#",
    title: "Free Blender Templates",
  },
  {
    href: "#",
    title: "Video Tutorial Walkthrough",
  },
  {
    href: "#",
    title: "Examples",
  },
];

const SOCIAL: FooterLink[] = [
  {
    href: "#",
    title: "Instagram",
  },
  {
    href: "#",
    title: "Bluesky",
  },
  {
    href: "#",
    title: "Threads",
  },
  {
    href: "#",
    title: "YouTube",
  },
];

const LINKS = {
  guides: GUIDES,
  resources: RESOURCES,
  social: SOCIAL,
};

export default LINKS;
