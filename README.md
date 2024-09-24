[MIDI to Keyframe - Process - Creating Keyframes V2 Shorter Zoom.webm](https://github.com/user-attachments/assets/dc90301c-569a-493f-a6f9-35798aeb086b)

# MIDI to Keyframes Blender addon

This is a free Blender addon to import MIDI files and generate animation keyframes. It assigns the keyframes to objects you assign as piano keys.

> On some devices like Mac you may need to give elevated permissions to Blender to allow for plugin to work. This is because we need to install a library to read MIDI files inside Blender.

## Installation

1. Download as a zip
1. Open Blender
1. Go to Edit > Preferences and go to the Addons tab on left.
1. Click install button.
1. Select the zip you downloaded.
1. You can confirm it's installed by searching for "MIDI to Keyframes" and seeing if it's checked off

## How to use

1. Open up the side panel labeled **"MIDI Import"**, it's available in the 3D viewport in the n-panel (the right side panel that's usually collapsed).
1. Select a MIDI file you'd like to import.
1. Assign 3D objects to piano keys.
1. Click the button labeled **"Generate Keyframes"**

> Not happy with the animation? You can undo the keyframes (`CTRL/CMD + Z`). Can't undo? Try the **"Delete All Keyframes"** button, it will delete **_all_** keyframes on any selected note object.

### Tips

I'd recommend downloading [Audacity](https://www.audacityteam.org/) to visualize the MIDI tracks and see what the note charts look like before you import them into Blender.

## How it works

I did [a full breakdown on my blog here](https://whoisryosuke.com/blog/2024/midi-powered-animations-in-blender) that covers the creation of the plugin and tips and tricks for working with MIDI in Python.

## Credits

- [mido](https://github.com/mido/mido)
- [Gamepad Input Blender addon](https://github.com/whoisryosuke/blender-gamepad)
