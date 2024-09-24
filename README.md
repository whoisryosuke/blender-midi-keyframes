[Example of plugin generating keyframes with 3D piano keys](https://github.com/user-attachments/assets/dc90301c-569a-493f-a6f9-35798aeb086b)

# MIDI to Keyframes Blender addon

This is a free Blender addon to import MIDI files and generate animation keyframes. It assigns the keyframes to objects you assign as piano keys.

> On some devices like Mac you may need to give elevated permissions to Blender to allow for plugin to work. This is because we need to install a library to read MIDI files inside Blender.

## ⬇️ Installation

1. [Download as a zip](https://github.com/whoisryosuke/blender-midi-keyframes/archive/refs/heads/main.zip)
1. Open Blender
1. Go to Edit > Preferences and go to the Addons tab on left.
1. Click install button.
1. Select the zip you downloaded.
1. You can confirm it's installed by searching for **"MIDI to Keyframes"** and seeing if it's checked off

## 🔰 How to use

![The plugin panel inside Blender](/docs/screenshots/plugin-panel.jpg)

1. Open up the side panel labeled **"MIDI Import"**, it's available in the 3D viewport in the n-panel (the right side panel that's usually collapsed).
1. Select a MIDI file you'd like to import.
1. Assign 3D objects to piano keys.
1. Click the button labeled **"Generate Keyframes"**

> Not happy with the animation? You can undo the keyframes (`CTRL/CMD + Z`). Can't undo? Try the **"Delete All Keyframes"** button, it will delete **_all_** keyframes on any selected note object.

### Tips

#### Auto Assigning Keys

The plugin can automatically assign piano keys if you create a collection with objects with the note letter appended to the end.

For example, you'd name your objects something like:

- `ObjectName.C` maps to the `C` piano key
- `yourobject.F#` maps to the `F#` piano key

Then you can select the collection and press the **"Auto-Assign Keys" button**.

#### Visualizing the MIDI Track

I'd recommend downloading [Audacity](https://www.audacityteam.org/) to visualize the MIDI tracks and see what the note charts look like before you import them into Blender.

## 🐛 Known Bugs

### MIDI file won't load!

Currently the plugin only works with a full file path. The plugin will not work if you provide a relative file path (which Blender sometimes does automatically if the MIDI file is located in the same folder as the Blender file...).

Correct way:

- Windows: `C:\some-folder\midi-file.mid`
- Mac: `Macintosh HD/Users/Your Name/some-folder/midi-file.mid`

This will probably get fixed in the future 👍

## ⚙️ How it works

I did [a full breakdown on my blog here](https://whoisryosuke.com/blog/2024/midi-powered-animations-in-blender) that covers the creation of the plugin and tips and tricks for working with MIDI in Python.

## 💪 Credits

- [mido](https://github.com/mido/mido)
- [Gamepad Input Blender addon](https://github.com/whoisryosuke/blender-gamepad)
