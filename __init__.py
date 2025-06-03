bl_info = {
    "name": "MIDI Motion",
    "description": "Import MIDI files and generate animations",
    "author": "whoisryosuke",
    "version": (0, 0, 9),
    "blender": (2, 80, 0), # not sure if this is right
    "location": "Properties > Output",
    "warning": "Make sure to press 'Install dependencies' button in the plugin panel before using", # used for warning icon and text in addons panel
    "wiki_url": "https://github.com/whoisryosuke/blender-midi-keyframes",
    "tracker_url": "",
    "category": "Development"
}


import bpy
from bpy.props import (StringProperty,
                       FloatProperty,
                       EnumProperty,
                       BoolProperty,
                       PointerProperty,
                       )
from bpy.types import (
                       PropertyGroup,
                       )
import math
import subprocess
import sys
import os

# Constants
midi_note_map = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
octaves = [0,1,2,3,4,5,6,7,8]
def generate_full_midi_keys():
    full_notes = []
    
    # Generate notes with numbers (e.g. C#4, C#5, etc)
    for note in midi_note_map:
        for octave in octaves:
            full_notes.append(note + str(octave))
        
        full_notes.append("C8")
    return full_notes
full_midi_note_map = generate_full_midi_keys()

DEFAULT_TEMPO = 500000

# Global state
midi_file_loaded = ""
selected_tracks_raw = []

def handle_midi_file_path(midi_file_path):
    fixed_midi_file_path = midi_file_path

    # Relative file path? Lets fix that
    if "//" in midi_file_path:
        filepath = bpy.data.filepath
        directory = os.path.dirname(filepath)
        midi_path_base = midi_file_path.replace("//", "")
        fixed_midi_file_path = os.path.join( directory , midi_path_base)
        
    return fixed_midi_file_path
    

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
    from mido import MidiFile

    fixed_path = handle_midi_file_path(midi_file_path)
    mid = MidiFile(fixed_path)

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
ANIM_MODE_KEYFRAMES = "KEYFRAMES"
ANIM_MODE_ACTIONS = "ACTIONS"

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
    animation_mode: EnumProperty(
        name="Animation Mode",
        description="Changes animation mode",
        items=[ (ANIM_MODE_KEYFRAMES, "Keyframes", ""),
                (ANIM_MODE_ACTIONS, "Actions", ""),
              ]
        )

    ## MODE: Collection
    collection_mode: BoolProperty(
        name = "Collection Mode",
        description = "Animate objects inside a collection instead of individual objects",
        default = False,
        )

    ## MODE: Actions
    action_advanced_mode: BoolProperty(
        name = "Advanced Mode",
        description = "Lets you add an action per note (instead of 1 for all)",
        default = False,
        )
    action_default: PointerProperty(
        name="Action",
        description="Action that plays when any note is 'pressed'",
        type=bpy.types.Action,
        )
    
    ## MODE: Keyframes
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
    direction: EnumProperty(
        name = "Direction",
        description = "Do the objects move up or down?",
        items=[ ('down', "Down", ""),
                ('up', "Up", ""),
              ]
        )
    octave: EnumProperty(
        name = "Octave",
        description = "Which octave should we use? (e.g. 3 = C3, D3, etc)",
        items=[ ('0', "All", ""),
                ('1', "1", ""),
                ('2', "2", ""),
                ('3', "3", ""),
                ('4', "4", ""),
                ('5', "5", ""),
                ('6', "6", ""),
                ('7', "7", ""),
                ('8', "8", ""),
              ]
        )
    speed: FloatProperty(
            name = "Speed",
            description = "Controls the tempo by this rate (e.g. 2 = 2x slower, 0.5 = 2x faster)",
            default = 1.0,
            min = 0.01,
            max = 100.0
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

    obj_collection: PointerProperty(
        name="Collection",
        description="Collection with 88 or less key objects to be controlled",
        type=bpy.types.Collection,
        )

    # Actions for objects
    action_c: PointerProperty(
        name="C",
        description="Action that plays for corresponding note",
        type=bpy.types.Action,
        )
        
    action_d: PointerProperty(
        name="D",
        description="Action that plays for corresponding note",
        type=bpy.types.Action,
        )
        
    action_e: PointerProperty(
        name="E",
        description="Action that plays for corresponding note",
        type=bpy.types.Action,
        )
        
    action_f: PointerProperty(
        name="F",
        description="Action that plays for corresponding note",
        type=bpy.types.Action,
        )
        
    action_g: PointerProperty(
        name="G",
        description="Action that plays for corresponding note",
        type=bpy.types.Action,
        )
        
    action_a: PointerProperty(
        name="A",
        description="Action that plays for corresponding note",
        type=bpy.types.Action,
        )
        
    action_b: PointerProperty(
        name="B",
        description="Action that plays for corresponding note",
        type=bpy.types.Action,
        )
        
    action_csharp: PointerProperty(
        name="C#",
        description="Action that plays for corresponding note",
        type=bpy.types.Action,
        )
        
    action_dsharp: PointerProperty(
        name="D#",
        description="Action that plays for corresponding note",
        type=bpy.types.Action,
        )
    
    action_fsharp: PointerProperty(
        name="F#",
        description="Action that plays for corresponding note",
        type=bpy.types.Action,
        )
    
    action_gsharp: PointerProperty(
        name="G#",
        description="Action that plays for corresponding note",
        type=bpy.types.Action,
        )

    action_asharp: PointerProperty(
        name="A#",
        description="Action that plays for corresponding note",
        type=bpy.types.Action,
        )
    
    
    # App State (not for user)
    initial_state = {}

# UI Panel
class GI_MIDIInputPanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_category = "MIDI Import"
    bl_label = "MIDI Importer"
    bl_idname = "SCENE_PT_midi_panel"
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
        row = layout.row()
        row.prop(midi_keyframe_props, "octave")

        layout.separator(factor=1.5)
        layout.label(text="Animation Settings", icon="IPO_ELASTIC")

        row = layout.row()
        row.prop(midi_keyframe_props, "animation_mode")
        
        if midi_keyframe_props.animation_mode == ANIM_MODE_ACTIONS:
            if not midi_keyframe_props.action_advanced_mode:
                row = layout.row()
                row.prop(midi_keyframe_props, "action_default")
            row = layout.row()
            row.prop(midi_keyframe_props, "action_advanced_mode")
            
        if midi_keyframe_props.action_advanced_mode:
            row = layout.row()
            row.prop(midi_keyframe_props, "action_c", icon="EVENT_C")
            row = layout.row()
            row.prop(midi_keyframe_props, "action_d", icon="EVENT_D")
            row = layout.row()
            row.prop(midi_keyframe_props, "action_e", icon="EVENT_E")
            row = layout.row()
            row.prop(midi_keyframe_props, "action_f", icon="EVENT_F")
            row = layout.row()
            row.prop(midi_keyframe_props, "action_g", icon="EVENT_G")
            row = layout.row()
            row.prop(midi_keyframe_props, "action_a", icon="EVENT_A")
            row = layout.row()
            row.prop(midi_keyframe_props, "action_b", icon="EVENT_B")
            row = layout.row()
            row.prop(midi_keyframe_props, "action_csharp", icon="EVENT_C")
            row = layout.row()
            row.prop(midi_keyframe_props, "action_dsharp", icon="EVENT_D")
            row = layout.row()
            row.prop(midi_keyframe_props, "action_fsharp", icon="EVENT_F")
            row = layout.row()
            row.prop(midi_keyframe_props, "action_gsharp", icon="EVENT_G")
            row = layout.row()
            row.prop(midi_keyframe_props, "action_asharp", icon="EVENT_A")
            
        if midi_keyframe_props.animation_mode == ANIM_MODE_KEYFRAMES:
            row = layout.row()
            row.prop(midi_keyframe_props, "animation_type")
            if midi_keyframe_props.animation_type != "SCALE":
                row = layout.row()
                row.prop(midi_keyframe_props, "axis")
            row = layout.row()
            row.prop(midi_keyframe_props, "travel_distance")
            row = layout.row()
            row.prop(midi_keyframe_props, "direction")
            row = layout.row()
            row.prop(midi_keyframe_props, "speed")

        layout.separator(factor=1.5)
        layout.label(text="Generate Animation", icon="RENDER_ANIMATION")
        if midi_keyframe_props.animation_mode == ANIM_MODE_ACTIONS:
            row = layout.row()
            row.operator("wm.generate_action_animation")
        if midi_keyframe_props.animation_mode == ANIM_MODE_KEYFRAMES:
            row = layout.row()
            row.operator("wm.generate_piano_animation")
            row = layout.row()
            row.operator("wm.generate_jumping_animation")




        layout.separator(factor=1.5)
        layout.label(text="Piano Keys", icon="OBJECT_DATAMODE")
        row = layout.row()

        row.prop(midi_keyframe_props, "collection_mode")
        row = layout.row()

        if midi_keyframe_props.collection_mode:
            row.prop(midi_keyframe_props, "obj_collection")
        else:
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

# Legacy: We use PIP `.wheels` files to install deps via Blender manifest `.toml`
# But this remains as a reference, in case that doesn't work for some reason (e.g. older versions of Blender)
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

# Global Debug Vars   
print_once = False

# Shared helper functions

def get_note_obj_from_collection(collection, noteLetter, octave):

    note = noteLetter + str(octave)

    # print("Getting obj from collection", note, noteLetter, octave)
    found_obj = None
    for (key, obj) in collection:
        if note in key:
            found_obj = obj

    return found_obj

def get_note_obj(midi_keyframe_props, noteLetter, octave):

    if midi_keyframe_props.collection_mode:
        return get_note_obj_from_collection(midi_keyframe_props.obj_collection.all_objects.items(), noteLetter, octave)
        
    else:
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
    return None
    
def get_note_action(midi_keyframe_props, noteLetter):
    if noteLetter == "C":
        return midi_keyframe_props.action_c
    if noteLetter == "D":
        return midi_keyframe_props.action_d
    if noteLetter == "E":
        return midi_keyframe_props.action_e
    if noteLetter == "F":
        return midi_keyframe_props.action_f
    if noteLetter == "G":
        return midi_keyframe_props.action_g
    if noteLetter == "A":
        return midi_keyframe_props.action_a
    if noteLetter == "B":
        return midi_keyframe_props.action_b
    if noteLetter == "C#":
        return midi_keyframe_props.action_csharp
    if noteLetter == "D#":
        return midi_keyframe_props.action_dsharp
    if noteLetter == "F#":
        return midi_keyframe_props.action_fsharp
    if noteLetter == "G#":
        return midi_keyframe_props.action_gsharp
    if noteLetter == "A#":
        return midi_keyframe_props.action_asharp
    return None
    
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
        is_midi_file = ".mid" in midi_file_path
        # TODO: Return error to user somehow??
        if not is_midi_file:
            return {"FINISHED"}

def get_note_letter(note):
    # Figure out the actual note "letter" (e.g. C, C#, etc)
    # Get the octave
    octave_base = math.floor(note / 12)
    # MIDI note number = current octave * 12 + the note index (0-11)
    octave_offset = octave_base * 12
    note_index = note - octave_offset
    note_letter = midi_note_map[note_index]
    octave = octave_base - 1
    # print("Note: {}{}".format(note_letter, octave))

    return note_letter, octave

class ParsedMidiFile:
    total_time = 0
    midi = None
    has_release = False
    tempo = DEFAULT_TEMPO
    selected_track = 0

    def __init__(self, midi_file_path, selected_track) -> None:
        print("Loading MIDI file...") 
        self.selected_track = selected_track
        from mido import MidiFile

        fixed_midi_file_path = handle_midi_file_path(midi_file_path)

        self.midi = MidiFile(fixed_midi_file_path)
        
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
            if msg.type == 'note_off' or msg.type == 'note_on' and msg.velocity == 0:
                print("MIDI has release notes")
                self.has_release = True

    def for_each_key(self, context, key_callback):
        from mido import tick2second

        scene_start_frame = context.scene.frame_start
        scene_end_frame = context.scene.frame_end
        total_frames = scene_end_frame - scene_start_frame
        fps = context.scene.render.fps
        time = 0
        midi_keyframe_props = context.scene.midi_keyframe_props
        speed = midi_keyframe_props.speed

        last_keyframe = 0
        last_note = None


        # Loop over each MIDI track
        for msg in self.midi.tracks[int(self.selected_track)]:
            # mido returns "metadata" embedded alongside music
            # we don't need so we filter out
            # print(msg.type)
            is_note = True if msg.type == "note_on" or msg.type == "note_off" else False
            if not msg.is_meta and is_note:
                pressed = True if msg.type == "note_on" and msg.velocity > 0 else False
                released = True if msg.type == "note_off" or msg.type == "note_on" and msg.velocity == 0 else False

                # Figure out the actual note "letter" (e.g. C, C#, etc)
                note_letter, octave = get_note_letter(msg.note)
                
                # Increment time
                time += msg.time
                # Figure out what frame we're on
                time_percent = time / self.total_time
                current_frame = total_frames * time_percent
                # print("time: {}, current frame: {}".format(time, current_frame))
                real_time = tick2second(time, self.midi.ticks_per_beat, self.tempo) * speed

                # print("real time in seconds", real_time)

                real_keyframe = (real_time * fps) + 1

                key_callback(context, note_letter, octave, real_keyframe, pressed, released, self.has_release, last_keyframe, last_note)

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
        collection_mode = midi_keyframe_props.collection_mode
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
        note_map = full_midi_note_map if collection_mode else midi_note_map
        octave = 0

        print("Saving initial positions...") 
        for note in note_map:

            # For collections note_letter is C#1 - so we need to strip out octave
            note_letter = note
            if collection_mode:
                octave = int(note[-1])
                note_letter = note_letter[0:-1]

            # Get the right object corresponding to the note
            move_obj = get_note_obj(midi_keyframe_props, note_letter, octave)
            if move_obj == None:
                continue
            
            match animation_type:
                case "MOVE":
                    midi_keyframe_props.initial_state[note] = move_obj.location[axis]

                case "SCALE":
                    midi_keyframe_props.initial_state[note] = move_obj.scale.x
                    
                case "ROTATE":
                    midi_keyframe_props.initial_state[note] = move_obj.rotation_euler[axis]

        # Loop over each music note and animate corresponding keys
        midi_file.for_each_key(context, animate_keys)

        print("Done animating. Check objects for keyframes.")

        return {"FINISHED"}

class GI_generate_action_animation(bpy.types.Operator):
    """Generate animation"""
    bl_idname = "wm.generate_action_animation"
    bl_label = "Action Animation"
    bl_description = "Creates actions on piano key objects when notes are pressed"

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

        # Loop over each music note and animate corresponding keys
        midi_file.for_each_key(context, animate_actions)

        print("Done animating. Check objects for actions.")

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
        collection_mode = midi_keyframe_props.collection_mode

        note_map = full_midi_note_map if collection_mode else midi_note_map
        octave = 0

        for note in note_map:
            # For collections note_letter is C#1 - so we need to strip out octave
            note_letter = note
            if collection_mode:
                octave = int(note[-1])
                note_letter = note_letter[0:-1]

            note_obj = get_note_obj(midi_keyframe_props, note_letter, octave)
            if note_obj == None:
                continue
            note_obj.animation_data_clear()

        return {"FINISHED"}
    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

class GI_assign_keys(bpy.types.Operator):
    """Automatically assign piano keys"""
    bl_idname = "wm.assign_keys"
    bl_label = "Auto-Assign Keys"
    bl_description = "Finds piano keys in currently selected collection with names ending in the note letter like .C or .D#"

    def execute(self, context: bpy.types.Context):
        midi_keyframe_props = context.scene.midi_keyframe_props

        for check_obj in context.collection.all_objects:
            obj_name_split = check_obj.name.split(".")
            obj_name_key = obj_name_split[-1]
            for note in midi_note_map:
                if note == obj_name_key:
                    replace_note_obj(midi_keyframe_props, note, check_obj)

        return {"FINISHED"}

class GI_generate_jumping_animation(bpy.types.Operator):
    """Jump animation"""
    bl_idname = "wm.generate_jumping_animation"
    bl_label = "Jumping Animation"
    bl_description = "(BETA) Creates keyframes on Jump object animating between keys"

    def execute(self, context: bpy.types.Context):
        midi_keyframe_props = context.scene.midi_keyframe_props
        midi_file_path = midi_keyframe_props.midi_file
        selected_track = midi_keyframe_props.selected_track

        # Is it a MIDI file? If not, bail early
        check_for_midi_file(context)

        # Do we have an object to move?
        if midi_keyframe_props.obj_jump == None:
            return {"CANCELLED"}

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
def animate_actions(context, note_letter, octave: int, real_keyframe, pressed, released, has_release, prev_keyframe, prev_note):
    midi_keyframe_props = context.scene.midi_keyframe_props
    advanced_mode = midi_keyframe_props.action_advanced_mode
    action = midi_keyframe_props.action_default

    # We only care about presses for now
    # TODO: Separate actions for each interaction type (pressed, released)
    if not pressed:
        return

    # Keyframe generation
    # Get the right object corresponding to the note
    move_obj = get_note_obj(midi_keyframe_props, note_letter, octave)
    if move_obj == None:
        return
    
    # Make sure we create a "slot" for animation data - if it doesn't exist we get errors
    if move_obj.animation_data is None:
        move_obj.animation_data_create()

    # Create new animation track ("NLA Track")
    new_track = move_obj.animation_data.nla_tracks.new()
    strip_name = "note_c.001"

    # If we're in advanced mode we select a note-specific action
    if advanced_mode:
        action = get_note_action(midi_keyframe_props, note_letter)

    # Create new strip on that track and add action to it
    new_strip = new_track.strips.new(strip_name, int(real_keyframe), action)
    # We set extrapolation mode to NOTHING so it keeps playing (default is "HOLD" - freezing anim)
    new_strip.extrapolation = 'NOTHING'

# Animates objects up and down like piano keys
def animate_keys(context, note_letter, octave: int, real_keyframe, pressed, released, has_release, prev_keyframe, prev_note):
    midi_keyframe_props = context.scene.midi_keyframe_props
    collection_mode = midi_keyframe_props.collection_mode
    initial_state = midi_keyframe_props.initial_state
    animation_type = midi_keyframe_props.animation_type
    direction = midi_keyframe_props.direction
    direction_factor = -1 if direction == "down" else 1
    axis = int(midi_keyframe_props.axis)
    user_octave: str = midi_keyframe_props.octave

    # Skip this note if we don't care about the octave
    # 0 = All, so if it's not all, we need to check for octave
    if user_octave != "0":
        # The user_octave is string, while MIDI returns int for octave 
        if user_octave != str(octave):
            return;

    # For collections note includes octave - so we need full note to check initial state cache
    note = note_letter
    if collection_mode:
        note = note_letter + str(octave)

    print("animating key", note, octave)

    # Keyframe generation
    # Get the right object corresponding to the note
    move_obj = get_note_obj(midi_keyframe_props, note_letter, octave)
    if move_obj == None:
        return
    
    
    # Save initial position as previous frame
    match animation_type:
        case "MOVE":
            move_obj.location[axis] = initial_state[note]
            move_obj.keyframe_insert(data_path="location", frame=real_keyframe - 1)

        case "SCALE":
            move_obj.scale = (initial_state[note],initial_state[note],initial_state[note])
            move_obj.keyframe_insert(data_path="scale", frame=real_keyframe - 1)
            
        case "ROTATE":
            move_obj.rotation_euler[axis] = initial_state[note]
            move_obj.keyframe_insert(data_path="rotation_euler", frame=real_keyframe - 1)

    # Move the object
    if pressed:
        match animation_type:
            case "MOVE":
                # Position distance is negative for pressing (since we're in Z-axis going "down")
                # But it can be flipped by user preference
                reverse_direction = midi_keyframe_props.travel_distance * direction_factor
                move_distance = reverse_direction + initial_state[note]
                move_obj.location[axis] = move_distance
                move_obj.keyframe_insert(data_path="location", frame=real_keyframe)
            case "SCALE":
                # Scale "distance" is positive for pressing
                move_distance = midi_keyframe_props.travel_distance + initial_state[note]
                move_obj.scale = (move_distance,move_distance,move_distance)
                move_obj.keyframe_insert(data_path="scale", frame=real_keyframe)
            case "ROTATE":
                # Rotation distance is positive for pressing
                reverse_direction = midi_keyframe_props.travel_distance * direction_factor
                move_distance = reverse_direction + initial_state[note]
                move_obj.rotation_euler[axis] = math.radians(move_distance)
                move_obj.keyframe_insert(data_path="rotation_euler", frame=real_keyframe)
    if released:
        match animation_type:
            case "MOVE":
                # Position distance is negative for pressing (since we're in Z-axis going "down")
                # But it can be flipped by user preference
                reverse_direction = midi_keyframe_props.travel_distance * direction_factor
                move_distance = initial_state[note]
                move_obj.location[axis] = move_distance
                move_obj.keyframe_insert(data_path="location", frame=real_keyframe)
            case "SCALE":
                # Scale "distance" is positive for pressing
                move_distance = initial_state[note]
                move_obj.scale = (move_distance,move_distance,move_distance)
                move_obj.keyframe_insert(data_path="scale", frame=real_keyframe)
            case "ROTATE":
                # Rotation distance is positive for pressing
                reverse_direction = midi_keyframe_props.travel_distance * direction_factor
                move_distance = initial_state[note]
                move_obj.rotation_euler[axis] = math.radians(move_distance)
                move_obj.keyframe_insert(data_path="rotation_euler", frame=real_keyframe)

    # Does the file not have "released" notes? Create one if not
    # TODO: Figure out proper "hold" time based on time scale
    if not has_release:
        match animation_type:
            case "MOVE":
                move_obj.location[axis] = initial_state[note]
                move_obj.keyframe_insert(data_path="location", frame=real_keyframe + 10)
            case "SCALE":
                move_obj.scale = (initial_state[note],initial_state[note],initial_state[note])
                move_obj.keyframe_insert(data_path="scale", frame=real_keyframe + 10)
            case "ROTATE":
                move_obj.rotation_euler[axis] = initial_state[note]
                move_obj.keyframe_insert(data_path="rotation_euler", frame=real_keyframe + 10)

# Animates an object to "jump" between keys
def animate_jump(context, note_letter, octave, real_keyframe, pressed, released, has_release, prev_keyframe, prev_note):
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
            # print("middle point x", prev_piano_key_world_pos.x + middle_distance_x)
            move_obj.location.z += midi_keyframe_props.travel_distance
            move_obj.keyframe_insert(data_path="location", frame=frame_between)
            # print("Moving back down", note_letter, prev_note, prev_piano_key.name, prev_piano_key.location, prev_piano_key_world_pos.x, piano_key_world_pos.x)
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
    GI_MIDIInputPanel,
    GI_install_midi,
    GI_generate_piano_animation,
    GI_generate_jumping_animation,
    GI_generate_action_animation,
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
