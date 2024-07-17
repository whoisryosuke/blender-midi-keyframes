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

# ------------------------------------------------------------------------
#    Scene Properties
# ------------------------------------------------------------------------

# UI properties
class GI_SceneProperties(PropertyGroup):
        
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
    bl_category = "MIDI"
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

        layout.label(text="Controls")
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



# Load/unload addon into Blender
classes = (
    GI_SceneProperties,
    GI_GamepadInputPanel,
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
