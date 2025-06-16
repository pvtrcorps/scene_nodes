import types
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

# Stub Blender modules
bpy = types.ModuleType("bpy")
bpy.__path__ = []
bpy.utils = types.SimpleNamespace(register_class=lambda *a, **k: None, unregister_class=lambda *a, **k: None)
bpy.data = types.SimpleNamespace()
bpy.context = types.SimpleNamespace()
bpy.types = types.ModuleType("bpy.types")
bpy.props = types.SimpleNamespace(
    FloatProperty=lambda **k: None,
    IntProperty=lambda **k: None,
    BoolProperty=lambda **k: None,
    FloatVectorProperty=lambda **k: None,
    StringProperty=lambda **k: None,
    EnumProperty=lambda **k: None,
    CollectionProperty=lambda **k: None,
)
bpy.types.NodeTree = type("NodeTree", (), {})
bpy.types.Node = type("Node", (), {})
bpy.types.NodeSocket = type("NodeSocket", (), {})
bpy.types.Operator = type("Operator", (), {})
bpy.types.Panel = type("Panel", (), {})
bpy.types.PropertyGroup = type("PropertyGroup", (), {})
bpy.types.UIList = type("UIList", (), {})
sys.modules.setdefault("bpy", bpy)
sys.modules.setdefault("bpy.types", bpy.types)

from scene_nodes.engine import evaluator


def make_socket(name, from_node):
    return types.SimpleNamespace(
        bl_idname="SceneSocketType",
        name=name,
        is_linked=True,
        links=[types.SimpleNamespace(from_node=from_node)],
    )


def test_name_switch():
    node_a = types.SimpleNamespace(scene_nodes_output="A")
    node_b = types.SimpleNamespace(scene_nodes_output="B")
    socket_a = make_socket("PassA", node_a)
    socket_default = make_socket("Default", node_b)
    node = types.SimpleNamespace(inputs=[socket_a, socket_default])
    ctx = types.SimpleNamespace(render_pass="PassA")

    result = evaluator._evaluate_name_switch(node, [], None, ctx)
    assert result == "A"

    ctx.render_pass = "Other"
    result = evaluator._evaluate_name_switch(node, [], None, ctx)
    assert result == "B"

