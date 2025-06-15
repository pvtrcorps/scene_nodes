# ui/__init__.py
import bpy
from .node_editor import SCENE_GRAPH_MT_add
from .operators import NODE_OT_sync_to_scene
from .property_panel import SCENE_GRAPH_PT_property_sockets

__all__ = [
    "SCENE_GRAPH_MT_add",
    "NODE_OT_sync_to_scene",
    "SCENE_GRAPH_PT_property_sockets",
]
from . import node_editor, property_panel


def register():
    node_editor.register()
    bpy.utils.register_class(SCENE_GRAPH_PT_property_sockets)


def unregister():
    bpy.utils.unregister_class(SCENE_GRAPH_PT_property_sockets)
    node_editor.unregister()

