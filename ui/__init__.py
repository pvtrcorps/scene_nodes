# ui/__init__.py
from .node_editor import SCENE_GRAPH_MT_add
from .operators import NODE_OT_sync_to_scene
from .node_panel import SCENE_NODES_PT_node_props

__all__ = [
    "SCENE_GRAPH_MT_add",
    "NODE_OT_sync_to_scene",
    "SCENE_NODES_PT_node_props",
]
from . import node_editor
from . import node_panel


def register():
    node_editor.register()
    node_panel.register()


def unregister():
    node_editor.unregister()
    node_panel.unregister()

