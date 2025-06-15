bl_info = {
    "name": "Scene Nodes",
    "author": "Tu Nombre",
    "version": (0, 1),
    "blender": (4, 0, 0),
    "location": "Node Editor > Scene Graph",
    "description": "Un sistema nodal para ensamblaje de escenas en Blender",
    "category": "Node"
}

import bpy
from nodeitems_utils import register_node_categories, unregister_node_categories

# NodeTree y sockets
from .node_tree import SceneNodeTree
from .nodes.base import SceneSocket

# Nodos individuales
from .nodes.scene_instance import SceneInstanceNode
from .nodes.transform import TransformNode
from .nodes.group import GroupNode
from .nodes.light import LightNode
from .nodes.global_options import GlobalOptionsNode
from .nodes.outputs_stub import OutputsStubNode

# UI
from .ui.node_categories import node_categories
from .ui.node_editor import SCENE_GRAPH_MT_add
from .ui.operators import NODE_OT_sync_to_scene

# Engine
from .engine import evaluate_scene_tree

# Clases a registrar
classes = [
    SceneNodeTree,
    SceneSocket,
    SceneInstanceNode, TransformNode, GroupNode,
    LightNode, GlobalOptionsNode, OutputsStubNode,
    NODE_OT_sync_to_scene,
    SCENE_GRAPH_MT_add,
]

NODETREE_CATEGORY = 'SCENE_NODES'

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.scene_node_tree = bpy.props.PointerProperty(type=SceneNodeTree)
    register_node_categories(NODETREE_CATEGORY, node_categories)


def unregister():
    unregister_node_categories(NODETREE_CATEGORY)
    del bpy.types.Scene.scene_node_tree
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)