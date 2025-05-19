export type FooterLink = {
  title: string;
  href: string;
};

const DOCS_URL = "/blender-midi-motion/docs";

const GUIDES: FooterLink[] = [
  {
    href: `${DOCS_URL}/getting-started`,
    title: "Installation",
  },
  {
    href: `${DOCS_URL}/getting-started`,
    title: "Getting Started",
  },
  {
    href: `${DOCS_URL}/exporting/export`,
    title: "Exporting to GLTF",
  },
  // {
  //   href: "#",
  //   title: "Ableton Live Workflow",
  // },
];

const RESOURCES: FooterLink[] = [
  {
    href: `${DOCS_URL}/resources/example-files`,
    title: "Free Blender Templates",
  },
  {
    href: "https://www.youtube.com/watch?v=E4wfblQWhtY",
    title: "Video Tutorial Walkthrough",
  },
  {
    href: `${DOCS_URL}/resources/showcase`,
    title: "Showcase",
  },
];

const SOCIAL: FooterLink[] = [
  {
    href: "https://www.instagram.com/whoisryosuke/",
    title: "Instagram",
  },
  {
    href: "https://bsky.app/profile/whoisryosuke.bsky.social",
    title: "Bluesky",
  },
  {
    href: "https://www.threads.com/@whoisryosuke",
    title: "Threads",
  },
  {
    href: "https://www.youtube.com/@whoisryosuke",
    title: "YouTube",
  },
];

const LINKS = {
  guides: GUIDES,
  resources: RESOURCES,
  social: SOCIAL,
};

export default LINKS;
