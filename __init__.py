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
DEFAULT_TEMPO = 500000

# Global state
midi_file_loaded = ""
selected_tracks_raw = []

# ------------------------------------------------------------------------
#    Scene Properties
# ------------------------------------------------------------------------

def selected_track_enum_callback(scene, context):
    global midi_file_loaded, selected_tracks_raw

    midi_keyframe_props = context.scene.midi_keyframe_props
    midi_file_path = midi_keyframe_props.midi_file

    # Check input and ensure it's actually MIDI
    is_midi_file = ".mid" in midi_file_path
    # TODO: Return error to user somehow??
    if not is_midi_file:
        return []
        

    # Have we already scanned this file? Check the "cache"
    if midi_file_loaded == midi_file_path:
        return selected_tracks_raw

    # Import the MIDI file
    from .modules.mido.mido import MidiFile

    mid = MidiFile(midi_file_path)

    # Setup time for track
    selected_tracks_raw = []
    time = 0
    # current_frame = context.scene.frame_current
    scene_start_frame = context.scene.frame_start
    scene_end_frame = context.scene.frame_end
    total_frames = scene_end_frame - scene_start_frame
    

    # Determine active track
    for i, track in enumerate(mid.tracks):
        # Loop over each note in the track
        for msg in track:
            if not msg.is_meta:
                # add to list of tracks
                selected_tracks_raw.insert(len(selected_tracks_raw), ("{}".format(i), "Track {} {}".format(i, track.name), ""))
                break;

    # print(selected_tracks_raw)

    # Mark this MIDI file as "cached"
    midi_file_loaded = midi_file_path
    
    return selected_tracks_raw

# UI properties
class GI_SceneProperties(PropertyGroup):
        
    # User Settings
    
    # MIDI File data
    midi_file: StringProperty(
        name="MIDI File",
        description="Music file you want to import",
        subtype = 'FILE_PATH'
        )
    selected_track:EnumProperty(
        name="Selected Track",
        description="The track you want copied to animation frames",
        items=selected_track_enum_callback
        )
    midi_file_loaded = ""
    
    # Animation toggles
    travel_distance: FloatProperty(
        name = "Travel Distance",
        description = "How far key moves when 'pressed' or how high object 'jumps'",
        default = 1.0,
        min = 0.01,
        max = 100.0
        )
    animation_type: EnumProperty(
        name="Object Animation",
        description="Changes what animates about object (e.g. Move is up and down)",
        items=[ ('MOVE', "Move", ""),
                ('SCALE', "Scale", ""),
                ('ROTATE', "Rotate", ""),
              ]
        )
    axis: EnumProperty(
        name="Axis",
        description="Axis that gets animated, aka direction piano keys move",
        items=[ ('0', "X", ""),
                ('1', "Y", ""),
                ('2', "Z", ""),
              ]
        )


    # MIDI Keys
    obj_jump: PointerProperty(
        name="Jumping Object",
        description="Object that 'jumps' between key objects",
        type=bpy.types.Object,
        )
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
    
    # App State (not for user)
    initial_state = {}

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
        midi_keyframe_props = scene.midi_keyframe_props
        
        # Legacy: Install deps using pip - we keep deps as git submodules now
        # row = layout.row()
        # row.operator("wm.install_midi")

        layout.label(text="MIDI Settings", icon="OUTLINER_OB_SPEAKER")
        row = layout.row()
        row.prop(midi_keyframe_props, "midi_file")
        row = layout.row()
        row.prop(midi_keyframe_props, "selected_track")

        layout.separator(factor=1.5)
        layout.label(text="Animation Settings", icon="IPO_ELASTIC")

        if midi_keyframe_props.animation_type != "SCALE":
            row = layout.row()
            row.prop(midi_keyframe_props, "axis")
        
        row = layout.row()
        row.prop(midi_keyframe_props, "travel_distance")
        row = layout.row()
        row.prop(midi_keyframe_props, "animation_type")

        layout.separator(factor=1.5)
        layout.label(text="Generate Animation", icon="RENDER_ANIMATION")
        row = layout.row()
        row.operator("wm.generate_piano_animation")
        row = layout.row()
        row.operator("wm.generate_jumping_animation")

        layout.separator(factor=1.5)
        layout.label(text="Piano Keys", icon="OBJECT_DATAMODE")
        row = layout.row()
        row.operator("wm.assign_keys")
        row = layout.row()
        row.prop(midi_keyframe_props, "obj_c", icon="EVENT_C")
        row = layout.row()
        row.prop(midi_keyframe_props, "obj_d", icon="EVENT_D")
        row = layout.row()
        row.prop(midi_keyframe_props, "obj_e", icon="EVENT_E")
        row = layout.row()
        row.prop(midi_keyframe_props, "obj_f", icon="EVENT_F")
        row = layout.row()
        row.prop(midi_keyframe_props, "obj_g", icon="EVENT_G")
        row = layout.row()
        row.prop(midi_keyframe_props, "obj_a", icon="EVENT_A")
        row = layout.row()
        row.prop(midi_keyframe_props, "obj_b", icon="EVENT_B")
        row = layout.row()
        row.prop(midi_keyframe_props, "obj_csharp", icon="EVENT_C")
        row = layout.row()
        row.prop(midi_keyframe_props, "obj_dsharp", icon="EVENT_D")
        row = layout.row()
        row.prop(midi_keyframe_props, "obj_fsharp", icon="EVENT_F")
        row = layout.row()
        row.prop(midi_keyframe_props, "obj_gsharp", icon="EVENT_G")
        row = layout.row()
        row.prop(midi_keyframe_props, "obj_asharp", icon="EVENT_A")

        layout.separator(factor=1.5)
        layout.label(text="Other Objects", icon="OBJECT_HIDDEN")
        row = layout.row()
        row.prop(midi_keyframe_props, "obj_jump", icon="MATSPHERE")

        layout.separator(factor=4.2)
        layout.label(text="Danger Zone", icon="ERROR")
        row = layout.row()
        row.operator("wm.delete_all_keyframes", icon="TRASH")

class GI_install_midi(bpy.types.Operator):
    """Install mido"""
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
    
# Shared helper functions
def get_note_obj(midi_keyframe_props, noteLetter):
    if noteLetter == "C":
        return midi_keyframe_props.obj_c
    if noteLetter == "D":
        return midi_keyframe_props.obj_d
    if noteLetter == "E":
        return midi_keyframe_props.obj_e
    if noteLetter == "F":
        return midi_keyframe_props.obj_f
    if noteLetter == "G":
        return midi_keyframe_props.obj_g
    if noteLetter == "A":
        return midi_keyframe_props.obj_a
    if noteLetter == "B":
        return midi_keyframe_props.obj_b
    if noteLetter == "C#":
        return midi_keyframe_props.obj_csharp
    if noteLetter == "D#":
        return midi_keyframe_props.obj_dsharp
    if noteLetter == "F#":
        return midi_keyframe_props.obj_fsharp
    if noteLetter == "G#":
        return midi_keyframe_props.obj_gsharp
    if noteLetter == "A#":
        return midi_keyframe_props.obj_asharp
    
def replace_note_obj(midi_keyframe_props, noteLetter, new_obj):
    if noteLetter == "C":
        midi_keyframe_props.obj_c = new_obj
    if noteLetter == "D":
        midi_keyframe_props.obj_d = new_obj
    if noteLetter == "E":
        midi_keyframe_props.obj_e = new_obj
    if noteLetter == "F":
        midi_keyframe_props.obj_f = new_obj
    if noteLetter == "G":
        midi_keyframe_props.obj_g = new_obj
    if noteLetter == "A":
        midi_keyframe_props.obj_a = new_obj
    if noteLetter == "B":
        midi_keyframe_props.obj_b = new_obj
    if noteLetter == "C#":
        midi_keyframe_props.obj_csharp = new_obj
    if noteLetter == "D#":
        midi_keyframe_props.obj_dsharp = new_obj
    if noteLetter == "F#":
        midi_keyframe_props.obj_fsharp = new_obj
    if noteLetter == "G#":
        midi_keyframe_props.obj_gsharp = new_obj
    if noteLetter == "A#":
        midi_keyframe_props.obj_asharp = new_obj

def check_for_midi_file(context):
        midi_keyframe_props = context.scene.midi_keyframe_props
        midi_file_path = midi_keyframe_props.midi_file

        # Check input and ensure it's actually MIDI
        print("Checking if it's a MIDI file")
        is_midi_file = ".mid" in midi_file_path
        # TODO: Return error to user somehow??
        if not is_midi_file:
            return {"FINISHED"}

def get_note_letter(note):
    # Figure out the actual note "letter" (e.g. C, C#, etc)
    # Get the octave
    octave = round(note / 12)
    # MIDI note number = current octave * 12 + the note index (0-11)
    octave_offset = octave * 12
    note_index = note - octave_offset
    note_letter = midi_note_map[note_index]
    # print("Note: {}{}".format(note_letter, octave))

    return note_letter

class ParsedMidiFile:
    total_time = 0
    midi = None
    has_release = False
    tempo = DEFAULT_TEMPO
    selected_track = 0

    def __init__(self, midi_file_path, selected_track) -> None:
        print("Loading MIDI file...") 
        self.selected_track = selected_track
        from .modules.mido.mido import MidiFile

        self.midi = MidiFile(midi_file_path)
        
        # Get tempo from the first track
        for msg in self.midi.tracks[0]:
            if msg.is_meta and msg.type == 'set_tempo':
                self.tempo = msg.tempo

        # Total time
        for msg in self.midi.tracks[int(selected_track)]:
            
            # Figure out total time
            # We basically loop over every note in the selected track
            # and add up the time!
            self.total_time += msg.time

            # We also see if there's any stopping points using `note_off`
            # If missing - we assume notes are held for 1 second (like 1 block in FLStudio)
            if msg.type == 'note_off':
                self.has_release = True

    def for_each_key(self, context, key_callback):
        from mido import tick2second

        scene_start_frame = context.scene.frame_start
        scene_end_frame = context.scene.frame_end
        total_frames = scene_end_frame - scene_start_frame
        fps = context.scene.render.fps
        time = 0

        last_keyframe = 0
        last_note = None


        # Loop over each MIDI track
        for msg in self.midi.tracks[int(self.selected_track)]:
            # mido returns "metadata" embedded alongside music
            # we don't need so we filter out
            # print(msg.type)
            is_note = True if msg.type == "note_on" or msg.type == "note_off" else False
            if not msg.is_meta and is_note:
                pressed = True if msg.type == "note_on" else False
                released = True if msg.type == "note_off" else False

                # Figure out the actual note "letter" (e.g. C, C#, etc)
                note_letter = get_note_letter(msg.note)
                
                # Increment time
                time += msg.time
                # Figure out what frame we're on
                time_percent = time / self.total_time
                current_frame = total_frames * time_percent
                # print("time: {}, current frame: {}".format(time, current_frame))
                real_time = tick2second(time, self.midi.ticks_per_beat, self.tempo)

                # print("real time in seconds", real_time)

                real_keyframe = (real_time * fps) + 1

                key_callback(context, note_letter, real_keyframe, pressed, self.has_release, last_keyframe, last_note)

                last_keyframe = real_keyframe
                last_note = note_letter

class GI_generate_piano_animation(bpy.types.Operator):
    """Generate animation"""
    bl_idname = "wm.generate_piano_animation"
    bl_label = "Piano Key Animation"
    bl_description = "Creates keyframes on piano key objects to simulate playback"

    def execute(self, context: bpy.types.Context):
        midi_keyframe_props = context.scene.midi_keyframe_props
        midi_file_path = midi_keyframe_props.midi_file
        selected_track = midi_keyframe_props.selected_track
        animation_type = midi_keyframe_props.animation_type
        axis = int(midi_keyframe_props.axis)

        # Is it a MIDI file? If not, bail early
        check_for_midi_file(context)


        # Import the MIDI file
        print("Parsing MIDI file...") 
        midi_file = ParsedMidiFile(midi_file_path, selected_track)

        # Debug - check for meta messages    
        # for msg in mid.tracks[int(selected_track)]:
        #     is_note = True if msg.type == "note_on" or msg.type == "note_off" else False
        #     if not is_note:
        #         print(msg)

        # Get initial positions for each key
        for note_letter in midi_note_map:
            # Get the right object corresponding to the note
            move_obj = get_note_obj(midi_keyframe_props, note_letter)
            if move_obj == None:
                return
            
            match animation_type:
                case "MOVE":
                    midi_keyframe_props.initial_state[note_letter] = move_obj.location[axis]

                case "SCALE":
                    midi_keyframe_props.initial_state[note_letter] = move_obj.scale.x
                    
                case "ROTATE":
                    midi_keyframe_props.initial_state[note_letter] = move_obj.rotation_euler[axis]

        # Loop over each music note and animate corresponding keys
        midi_file.for_each_key(context, animate_keys)

        return {"FINISHED"}

class GI_delete_all_keyframes(bpy.types.Operator):
    """Deletes all keyframes with confirm dialog"""
    bl_idname = "wm.delete_all_keyframes"
    bl_label = "Delete All Keyframes"
    bl_description = "Clears all animation data from assigned key objects"
    bl_options = {'REGISTER', 'INTERNAL'}

    @classmethod
    def poll(cls, context):
        return True
    def execute(self, context: bpy.types.Context):
        midi_keyframe_props = context.scene.midi_keyframe_props

        for note_letter in midi_note_map:
            note_obj = get_note_obj(midi_keyframe_props, note_letter)
            if note_obj == None:
                return
            note_obj.animation_data_clear()

        return {"FINISHED"}
    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

class GI_assign_keys(bpy.types.Operator):
    """Test function for gamepads"""
    bl_idname = "wm.assign_keys"
    bl_label = "Auto-Assign Keys"
    bl_description = "Finds piano keys in currently selected collection"

    def execute(self, context: bpy.types.Context):
        midi_keyframe_props = context.scene.midi_keyframe_props

        for check_obj in context.collection.all_objects:
            obj_name_split = check_obj.name.split(".")
            obj_name_key = obj_name_split[-1]
            for note in midi_note_map:
                if note == obj_name_key:
                    print("Found a note obj!")
                    print(note)
                    replace_note_obj(midi_keyframe_props, note, check_obj)

        return {"FINISHED"}

class GI_generate_jumping_animation(bpy.types.Operator):
    """Jump animation"""
    bl_idname = "wm.generate_jumping_animation"
    bl_label = "Jumping Animation"
    bl_description = "Creates keyframes on Jump object animating between keys"

    def execute(self, context: bpy.types.Context):
        midi_keyframe_props = context.scene.midi_keyframe_props
        midi_file_path = midi_keyframe_props.midi_file
        selected_track = midi_keyframe_props.selected_track

        # Is it a MIDI file? If not, bail early
        check_for_midi_file(context)

        # Do we have an object to move?
        if midi_keyframe_props.obj_jump == None:
            return;

        # Import the MIDI file
        print("Parsing MIDI file...") 
        midi_file = ParsedMidiFile(midi_file_path, selected_track)

        # Debug - check for meta messages    
        # for msg in mid.tracks[int(selected_track)]:
        #     is_note = True if msg.type == "note_on" or msg.type == "note_off" else False
        #     if not is_note:
        #         print(msg)

        # Save initial keyframe
        midi_keyframe_props.obj_jump.keyframe_insert(data_path="location", frame=0)

        # Loop over each music note and animate corresponding keys
        midi_file.for_each_key(context, animate_jump)

        return {"FINISHED"}

# Animates objects up and down like piano keys
def animate_keys(context, note_letter, real_keyframe, pressed, has_release, prev_keyframe, prev_note):
    midi_keyframe_props = context.scene.midi_keyframe_props
    initial_state = midi_keyframe_props.initial_state
    animation_type = midi_keyframe_props.animation_type
    axis = int(midi_keyframe_props.axis)

    # Keyframe generation
    # Get the right object corresponding to the note
    move_obj = get_note_obj(midi_keyframe_props, note_letter)
    if move_obj == None:
        return

    # Save initial position as previous frame
    match animation_type:
        case "MOVE":
            move_obj.location[axis] = initial_state[note_letter]
            move_obj.keyframe_insert(data_path="location", frame=real_keyframe - 1)

        case "SCALE":
            move_obj.scale = (initial_state[note_letter],initial_state[note_letter],initial_state[note_letter])
            move_obj.keyframe_insert(data_path="scale", frame=real_keyframe - 1)
            
        case "ROTATE":
            move_obj.rotation_euler[axis] = initial_state[note_letter]
            move_obj.keyframe_insert(data_path="rotation_euler", frame=real_keyframe - 1)

    # Move the object
    match animation_type:
        case "MOVE":
            # Position distance is negative for pressing (since we're in Z-axis going "down")
            reverse_direction = midi_keyframe_props.travel_distance * -1
            move_distance = reverse_direction + initial_state[note_letter] if pressed else initial_state[note_letter]
            move_obj.location[axis] = move_distance
            move_obj.keyframe_insert(data_path="location", frame=real_keyframe)
        case "SCALE":
            # Scale "distance" is positive for pressing
            move_distance = midi_keyframe_props.travel_distance + initial_state[note_letter] if pressed else initial_state[note_letter]
            move_obj.scale = (move_distance,move_distance,move_distance)
            move_obj.keyframe_insert(data_path="scale", frame=real_keyframe)
        case "ROTATE":
            # Rotation distance is positive for pressing
            move_distance = midi_keyframe_props.travel_distance + initial_state[note_letter] if pressed else initial_state[note_letter]
            move_obj.rotation_euler[axis] = math.radians(move_distance)
            move_obj.keyframe_insert(data_path="rotation_euler", frame=real_keyframe)

    # Does the file not have "released" notes? Create one if not
    # TODO: Figure out proper "hold" time based on time scale
    match animation_type:
        case "MOVE":
            move_obj.location[axis] = initial_state[note_letter]
            move_obj.keyframe_insert(data_path="location", frame=real_keyframe + 10)
        case "SCALE":
            move_obj.scale = (initial_state[note_letter],initial_state[note_letter],initial_state[note_letter])
            move_obj.keyframe_insert(data_path="scale", frame=real_keyframe + 10)
        case "ROTATE":
            move_obj.rotation_euler[axis] = initial_state[note_letter]
            move_obj.keyframe_insert(data_path="rotation_euler", frame=real_keyframe + 10)

# Animates an object to "jump" between keys
def animate_jump(context, note_letter, real_keyframe, pressed, has_release, prev_keyframe, prev_note):
    midi_keyframe_props = context.scene.midi_keyframe_props
    # Keyframe generation
    # Get the right object corresponding to the note
    piano_key = get_note_obj(midi_keyframe_props, note_letter)
    if piano_key == None:
        return
    
    move_obj = midi_keyframe_props.obj_jump

    if pressed:
        piano_key_world_pos = piano_key.matrix_world.to_translation()

        # Create jumping keyframes in between
        if prev_note != None:
            frame_between = int((real_keyframe - prev_keyframe) / 2) + prev_keyframe
            # print("Jumping!!: {} {} {}".format(real_keyframe, prev_keyframe, frame_between))
            prev_piano_key = get_note_obj(midi_keyframe_props, prev_note)
            prev_piano_key_world_pos = prev_piano_key.matrix_world.to_translation()
            middle_distance_x = (piano_key_world_pos.x - prev_piano_key_world_pos.x)
            move_obj.location.x = prev_piano_key_world_pos.x + middle_distance_x
            print("middle point x", prev_piano_key_world_pos.x + middle_distance_x)
            move_obj.location.z += midi_keyframe_props.travel_distance
            move_obj.keyframe_insert(data_path="location", frame=frame_between)
            print("Moving back down", note_letter, prev_note, prev_piano_key.name, prev_piano_key.location, prev_piano_key_world_pos.x, piano_key_world_pos.x)
            # Place it back down
            move_obj.location.z -= midi_keyframe_props.travel_distance


        # Move object to current key (the "down" moment)
        # print("pressed keyframe: {}".format(real_keyframe))
        # print("Setting jump keyframe: {} {}".format(piano_key.location.x, str(mathutils.Matrix.decompose(piano_key.matrix_world)[0])))
        # print("Setting jump keyframe: {} {}".format(note_letter, piano_key_world_pos.x))
        move_obj.location.x = piano_key_world_pos.x
        move_obj.keyframe_insert(data_path="location", frame=real_keyframe)



# Load/unload addon into Blender
classes = (
    GI_SceneProperties,
    GI_GamepadInputPanel,
    GI_install_midi,
    GI_generate_piano_animation,
    GI_generate_jumping_animation,
    GI_assign_keys,
    GI_delete_all_keyframes
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    bpy.types.Scene.midi_keyframe_props = PointerProperty(type=GI_SceneProperties)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)


if __name__ == "__main__":
    register()
