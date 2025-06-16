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
from .nodes.base import (
    SceneSocket,
    FloatSocket,
    IntSocket,
    BoolSocket,
    VectorSocket,
    StringSocket,
)

# Nodos individuales
from .nodes.scene_instance import SceneInstanceNode
from .nodes.transform import TransformNode
from .nodes.group import GroupNode
from .nodes.light import LightNode
from .nodes.global_options import GlobalOptionsNode
from .nodes.outputs_stub import OutputsStubNode
from .nodes.scene_output import SceneOutputNode
from .nodes.input import InputNode
from .nodes.scene_properties import ScenePropertiesNode
from .nodes.render_properties import RenderPropertiesNode
from .nodes.output_properties import OutputPropertiesNode

# UI
from .ui.node_categories import node_categories
from .ui.operators import NODE_OT_sync_to_scene
from . import ui

# Engine
from .engine import evaluate_scene_tree

# Clases a registrar
classes = [
    SceneNodeTree,
    SceneSocket,
    FloatSocket,
    IntSocket,
    BoolSocket,
    VectorSocket,
    StringSocket,
    SceneInstanceNode, TransformNode, GroupNode,
    LightNode, GlobalOptionsNode, OutputsStubNode, SceneOutputNode, InputNode,
    ScenePropertiesNode, RenderPropertiesNode, OutputPropertiesNode,
    NODE_OT_sync_to_scene,
]

NODETREE_CATEGORY = 'SCENE_NODES'


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    register_node_categories(NODETREE_CATEGORY, node_categories)
    ui.register()


def unregister():
    ui.unregister()
    unregister_node_categories(NODETREE_CATEGORY)
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
