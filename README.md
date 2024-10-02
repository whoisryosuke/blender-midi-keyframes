[Example of plugin generating keyframes with 3D piano keys](https://github.com/user-attachments/assets/dc90301c-569a-493f-a6f9-35798aeb086b)

# MIDI to Keyframes Blender addon

This is a free Blender addon to import MIDI files and generate animation keyframes. It assigns the keyframes to objects you assign as piano keys.

## ⬇️ Installation

1. [Download the plugin zip](https://github.com/whoisryosuke/blender-midi-keyframes/releases/download/v0.0.2/midi-to-keyframes-v0.0.2.zip) from the releases page
1. Open Blender
1. Go to Edit > Preferences and go to the Addons tab on left.
1. Click install button.
1. Select the zip you downloaded.
1. You can confirm it's installed by searching for **"MIDI to Keyframes"** and seeing if it's checked off

### Optional: Install Dependencies

> This isn't necessary anymore, I'll remove this instructions soon.

One last thing, you'll need to press 1 more button:

1. Open up the side panel labeled **"MIDI Importer"**, it's available in the 3D viewport in the n-panel (the right side panel that's usually collapsed).
1. Click the button labeled **"Install Dependencies"**.
1. Done!

> Having issues installing the dependencies? Try running `pip install mido` in the [Python console](https://docs.blender.org/manual/en/latest/editors/python_console.html).

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

#### FPS and Music Timing

When creating the animation keyframes, we use the current scene's frame rate to calculate the music time. If you **change the frame rate** after generating keyframes, you should **re-generate keyframes** to ensure the timing is correct.

## ⚙️ How it works

I did [a full breakdown on my blog here](https://whoisryosuke.com/blog/2024/midi-powered-animations-in-blender) that covers the creation of the plugin and tips and tricks for working with MIDI in Python.

## Development

1. Clone the repo: `git clone`
1. Zip up the folder.
1. Install in Blender.
1. Open the plugin code inside your Blender plugin folder.
1. Edit, Save, Repeat.

## Publish

1. Bump version in `__init__.py`
1. Bump version in `blender_manifest.toml`
1. `blender --command extension build --output-dir dist`
1. Upload the new `.zip` file generated inside `/dist` folder to Blender addon marketplace and [GitHub Releases page](https://github.com/whoisryosuke/blender-midi-keyframes/releases/new).

> Read more about [the extension setup here](https://docs.blender.org/manual/en/dev/advanced/extensions/getting_started.html) and [build process here](https://docs.blender.org/manual/en/dev/advanced/command_line/extension_arguments.html#command-line-args-extension-build). We basically have Python PIP "wheel" files that contain dependencies we need for this addon. The manifest installs them for us. Running the build command just zips up the folder with the version name attached - nothing fancy.

> On Windows? You can add `blender` to your command line by going to Start annd searching for "Edit Environment Variables for your account". Find the Variable "PATH" and edit it. Add the full path to where your `blender.exe` is located (e.g. `C:/Program Files/Blender/4.2/`).

## 💪 Credits

- [mido](https://github.com/mido/mido)
- [Gamepad Input Blender addon](https://github.com/whoisryosuke/blender-gamepad)
