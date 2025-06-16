# ui/__init__.py
from .operators import NODE_OT_sync_to_scene
from .node_panel import (
    SCENE_NODES_PT_node_props,
    SCENE_NODES_PT_node_props_properties,
    SCENE_NODES_PT_socket_visibility,
)

__all__ = [
    "NODE_OT_sync_to_scene",
    "SCENE_NODES_PT_node_props",
    "SCENE_NODES_PT_node_props_properties",
    "SCENE_NODES_PT_socket_visibility",
]
from . import node_panel


def register():
    node_panel.register()


def unregister():
    node_panel.unregister()

