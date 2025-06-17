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
    EnumSocket,
)

# Nodos individuales
from .nodes.blend_input import BlendInputNode
from .nodes.alembic_import import AlembicImportNode
from .nodes.transform import TransformNode
from .nodes.group import GroupNode
from .nodes.light import LightNode
from .nodes.global_options import GlobalOptionsNode
from .nodes.outputs_stub import OutputsStubNode
from .nodes.render_node import RenderNode
from .nodes.input import InputNode
from .nodes.join_string import JoinStringNode
from .nodes.split_string import SplitStringNode
from .nodes.name_switch import (
    NameSwitchNode,
    NameSwitchItem,
    SCENE_NODES_UL_name_switch,
    SCENE_NODES_OT_name_switch_add,
    SCENE_NODES_OT_name_switch_remove,
)
from .nodes.cycles_properties import CyclesPropertiesNode
from .nodes.eevee_properties import EeveePropertiesNode
from .nodes.cycles_attributes import CyclesAttributesNode
from .nodes.eevee_attributes import EeveeAttributesNode
from .nodes.render_engine import RenderEngineNode
from .nodes.render_passes import (
    RenderPassesNode,
    RenderPassItem,
    SCENE_NODES_UL_render_passes,
    SCENE_NODES_OT_render_pass_add,
    SCENE_NODES_OT_render_pass_remove,
)

# UI
from .ui.node_categories import node_categories
from .ui.operators import NODE_OT_sync_to_scene, RENDER_OT_render_pass_wedge
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
    EnumSocket,
    BlendInputNode, AlembicImportNode, TransformNode, GroupNode,
    LightNode, GlobalOptionsNode, OutputsStubNode, RenderNode, InputNode,
    JoinStringNode, SplitStringNode,
    NameSwitchItem, NameSwitchNode,
    SCENE_NODES_UL_name_switch, SCENE_NODES_OT_name_switch_add,
    SCENE_NODES_OT_name_switch_remove,
    CyclesPropertiesNode, EeveePropertiesNode,
    CyclesAttributesNode, EeveeAttributesNode, RenderEngineNode,
    RenderPassItem, RenderPassesNode,
    SCENE_NODES_UL_render_passes,
    SCENE_NODES_OT_render_pass_add, SCENE_NODES_OT_render_pass_remove,
    NODE_OT_sync_to_scene, RENDER_OT_render_pass_wedge,
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
