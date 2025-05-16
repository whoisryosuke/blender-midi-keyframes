# MIDI Motion Documentation

The documentation website for the MIDI Motion plugin, built using [Docusaurus](https://docusaurus.io/).

## How it works

The [frontpage is located here](docs\src\pages\index.tsx). It's the only page that's built fully in React. It contains a few fun components that handle the 3D rendering and MIDI animations.

All documentation content is written in MDX files (basically Markdown with React components added). Content is located in `docs/docs/`.

### Tips

- Keep images located alongside documentation (unless it's used globally). Add an `assets/` folder to the MDX content folder and place any images inside.
- There's a few "preset" React components you can use anywhere in MDX files, like embeds for social media. [Find a full list here](docs\src\theme\MDXComponents\index.tsx).

## Development

### Installation

```
$ yarn
```

### Local Development

```
$ yarn start
```

This command starts a local development server and opens up a browser window. Most changes are reflected live without having to restart the server.

### Build

```
$ yarn build
```

This command generates static content into the `build` directory and can be served using any static contents hosting service.

### Deployment

Push changes to `main` branch and documentation website should automatically build to GitHub Pages using GitHub Actions. See `.github/workflows/` for more info.

## References

- [Docusaurus](https://docusaurus.io/)
