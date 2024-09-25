[Example of plugin generating keyframes with 3D piano keys](https://github.com/user-attachments/assets/dc90301c-569a-493f-a6f9-35798aeb086b)

# MIDI to Keyframes Blender addon

This is a free Blender addon to import MIDI files and generate animation keyframes. It assigns the keyframes to objects you assign as piano keys.

## ⬇️ Installation

1. [Download the plugin zip](https://github.com/whoisryosuke/blender-midi-keyframes/releases/download/v0.0.1/midi-to-keyframes-v0.0.1.zip) from the releases page
1. Open Blender
1. Go to Edit > Preferences and go to the Addons tab on left.
1. Click install button.
1. Select the zip you downloaded.
1. You can confirm it's installed by searching for **"MIDI to Keyframes"** and seeing if it's checked off

## 🔰 How to use

![The plugin panel inside Blender](/docs/screenshots/plugin-panel.jpg)

1. Open up the side panel labeled **"MIDI Importer"**, it's available in the 3D viewport in the n-panel (the right side panel that's usually collapsed).
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

## ⚙️ How it works

I did [a full breakdown on my blog here](https://whoisryosuke.com/blog/2024/midi-powered-animations-in-blender) that covers the creation of the plugin and tips and tricks for working with MIDI in Python.

## Development

1. Clone the repo: `git clone`
1. Download any submodules: `git submodule update --init --recursive`
1. Install in Blender
1. Open the plugin code inside your Blender plugin folder
1. Edit, Save, Repeat.

## 💪 Credits

- [mido](https://github.com/mido/mido)
- [Gamepad Input Blender addon](https://github.com/whoisryosuke/blender-gamepad)
