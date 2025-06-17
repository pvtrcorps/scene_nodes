import types
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

# Stub Blender modules
bpy = types.ModuleType("bpy")
bpy.__path__ = []
bpy.data = types.SimpleNamespace(node_groups=[], scenes=types.SimpleNamespace())
bpy.context = types.SimpleNamespace(window=types.SimpleNamespace())
bpy.utils = types.SimpleNamespace(register_class=lambda *a, **k: None,
                                  unregister_class=lambda *a, **k: None)
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
render_calls = []
bpy.ops = types.SimpleNamespace(render=types.SimpleNamespace(render=lambda **k: render_calls.append(k)))

sys.modules["bpy"] = bpy
sys.modules["bpy.types"] = bpy.types

nodeitems_utils = types.ModuleType("nodeitems_utils")
nodeitems_utils.register_node_categories = lambda *a, **k: None
nodeitems_utils.unregister_node_categories = lambda *a, **k: None
nodeitems_utils.NodeCategory = type("NodeCategory", (), {"__init__": lambda self,*a,**k: None})
nodeitems_utils.NodeItem = lambda *a, **k: None
sys.modules.setdefault("nodeitems_utils", nodeitems_utils)

mathutils = types.ModuleType("mathutils")
mathutils.Vector = tuple
sys.modules.setdefault("mathutils", mathutils)

from importlib import reload
from scene_nodes.ui import operators as operators_module
from scene_nodes.engine import evaluator
operators = reload(operators_module)


class FakeViewLayers(dict):
    def new(self, name):
        layer = types.SimpleNamespace(name=name)
        self[name] = layer
        return layer


class FakeScene:
    def __init__(self):
        self.view_layers = FakeViewLayers()


evaluated_scenes = []

def fake_evaluate_scene_tree(tree):
    scene = FakeScene()
    evaluated_scenes.append(scene)
    bpy.context.window.scene = scene

evaluator.evaluate_scene_tree = fake_evaluate_scene_tree


passes_node = types.SimpleNamespace(
    bl_idname="RenderPassesNodeType",
    passes=[types.SimpleNamespace(name="Pass1"), types.SimpleNamespace(name="Pass2")],
)
tree = types.SimpleNamespace(bl_idname="SceneNodeTreeType", nodes=[passes_node])
bpy.data.node_groups = [tree]

original_scene = FakeScene()
original_layer = original_scene.view_layers.new("Original")
bpy.context.window.scene = original_scene
bpy.context.window.view_layer = original_layer

context = types.SimpleNamespace(area=None, window=bpy.context.window)


def test_render_pass_wedge_creates_layers_and_restores():
    op = operators.RENDER_OT_render_pass_wedge()
    op.execute(context)

    assert bpy.context.window.scene is original_scene
    assert bpy.context.window.view_layer is original_layer
    assert len(evaluated_scenes) == 2
    assert len(render_calls) == 2
    assert "Pass1" in evaluated_scenes[0].view_layers
    assert "Pass2" in evaluated_scenes[1].view_layers
    assert "Pass1" not in original_scene.view_layers

