bl_info = {
    "name": "MIDI to Keyframes",
    "description": "",
    "author": "whoisryosuke",
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
    "location": "Properties > Output",
    "warning": "", # used for warning icon and text in addons panel
    "wiki_url": "",
    "tracker_url": "",
    "category": "Development"
}

# from .inputs import devices

import bpy
from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       EnumProperty,
                       PointerProperty,
                       )
from bpy.types import (Panel,
                       Menu,
                       Operator,
                       PropertyGroup,
                       )
import threading
import numpy
import math
import mathutils
import subprocess
import sys
import os

# Constants

midi_note_map = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

# ------------------------------------------------------------------------
#    Scene Properties
# ------------------------------------------------------------------------

# UI properties
class GI_SceneProperties(PropertyGroup):
        
    # User Settings
    midi_file: StringProperty(
        name="MIDI File",
        description="Music file you want to import",
        subtype = 'FILE_PATH'
        )

    # MIDI Keys
    obj_c: PointerProperty(
        name="C",
        description="Object to be controlled",
        type=bpy.types.Object,
        )
        
    obj_d: PointerProperty(
        name="D",
        description="Object to be controlled",
        type=bpy.types.Object,
        )
        
    obj_e: PointerProperty(
        name="E",
        description="Object to be controlled",
        type=bpy.types.Object,
        )
        
    obj_f: PointerProperty(
        name="F",
        description="Object to be controlled",
        type=bpy.types.Object,
        )
        
    obj_g: PointerProperty(
        name="G",
        description="Object to be controlled",
        type=bpy.types.Object,
        )
        
    obj_a: PointerProperty(
        name="A",
        description="Object to be controlled",
        type=bpy.types.Object,
        )
        
    obj_b: PointerProperty(
        name="B",
        description="Object to be controlled",
        type=bpy.types.Object,
        )
        
    obj_csharp: PointerProperty(
        name="C#",
        description="Object to be controlled",
        type=bpy.types.Object,
        )
        
    obj_dsharp: PointerProperty(
        name="D#",
        description="Object to be controlled",
        type=bpy.types.Object,
        )
    
    obj_fsharp: PointerProperty(
        name="F#",
        description="Object to be controlled",
        type=bpy.types.Object,
        )
    
    obj_gsharp: PointerProperty(
        name="G#",
        description="Object to be controlled",
        type=bpy.types.Object,
        )
    
    obj_asharp: PointerProperty(
        name="A#",
        description="Object to be controlled",
        type=bpy.types.Object,
        )

# UI Panel
class GI_GamepadInputPanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_category = "MIDI Import"
    bl_label = "MIDI Importer"
    bl_idname = "SCENE_PT_gamepad"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    # bl_context = "output"
    
    def draw(self, context):
        layout = self.layout

        scene = context.scene
        gamepad_props = scene.gamepad_props
        
        row = layout.row()
        row.operator("wm.install_midi")

        layout.label(text="Settings")
        row = layout.row()
        row.prop(gamepad_props, "midi_file")
        row = layout.row()
        row.operator("wm.generate_keyframes")


        layout.label(text="Piano Keys")
        row = layout.row()
        row.prop(gamepad_props, "obj_c")
        row = layout.row()
        row.prop(gamepad_props, "obj_d")
        row = layout.row()
        row.prop(gamepad_props, "obj_e")
        row = layout.row()
        row.prop(gamepad_props, "obj_f")
        row = layout.row()
        row.prop(gamepad_props, "obj_g")
        row = layout.row()
        row.prop(gamepad_props, "obj_a")
        row = layout.row()
        row.prop(gamepad_props, "obj_csharp")
        row = layout.row()
        row.prop(gamepad_props, "obj_dsharp")
        row = layout.row()
        row.prop(gamepad_props, "obj_fsharp")
        row = layout.row()
        row.prop(gamepad_props, "obj_gsharp")
        row = layout.row()
        row.prop(gamepad_props, "obj_asharp")

class GI_install_midi(bpy.types.Operator):
    """Test function for gamepads"""
    bl_idname = "wm.install_midi"
    bl_label = "Install dependencies"
    bl_description = "Installs necessary Python modules for handling MIDI files"

    def execute(self, context: bpy.types.Context):

        print("Installing MIDI library...") 
        python_exe = os.path.join(sys.prefix, 'bin', 'python.exe')
        target = os.path.join(sys.prefix, 'lib', 'site-packages')

        subprocess.call([python_exe, '-m', 'ensurepip'])
        subprocess.call([python_exe, '-m', 'pip', 'install', '--upgrade', 'pip'])

        subprocess.call([python_exe, '-m', 'pip', 'install', '--upgrade', 'mido', '-t', target])

        return {"FINISHED"}
    
    
class GI_generate_keyframes(bpy.types.Operator):
    """Test function for gamepads"""
    bl_idname = "wm.generate_keyframes"
    bl_label = "Generate keyframes"
    bl_description = "Creates keyframes using MIDI file and assigned objects"

    def execute(self, context: bpy.types.Context):


        midi_file_path = context.scene.gamepad_props.midi_file

        # Check input and ensure it's actually MIDI
        print("Checking if it's a MIDI file")
        is_midi_file = ".mid" in midi_file_path
        # TODO: Return error to user somehow??
        if not is_midi_file:
            return {"FINISHED"}
            
        # Import the MIDI file
        print("Loading MIDI file...") 
        from mido import MidiFile

        mid = MidiFile(midi_file_path)
        

        # Loop over each MIDI track
        for i, track in enumerate(mid.tracks):
            print('Track {}: {}'.format(i, track.name))
            # Loop over each note in the track
            for msg in track:
                # mido returns "metadata" embedded alongside music
                # we don't need so we filter out
                if not msg.is_meta:
                    print(msg)
                    # Get the octave
                    octave = round(msg.note / 12)

                    # Figure out the actual note "letter" (e.g. C, C#, etc)
                    # MIDI note number = current octave * 12 + the note index (0-11)
                    octave_offset = octave * 12
                    note_index = msg.note - octave_offset
                    note_letter = midi_note_map[note_index]
                    print("Note: {}{}".format(note_letter, octave))

        return {"FINISHED"}


# Load/unload addon into Blender
classes = (
    GI_SceneProperties,
    GI_GamepadInputPanel,
    GI_install_midi,
    GI_generate_keyframes
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    bpy.types.Scene.gamepad_props = PointerProperty(type=GI_SceneProperties)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)


if __name__ == "__main__":
    register()
