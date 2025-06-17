from importlib import reload
import types
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

# Stub Blender modules
bpy = types.ModuleType("bpy")
bpy.__path__ = []
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


class FakeViewLayers(dict):
    def new(self, name):
        layer = types.SimpleNamespace(name=name)
        self[name] = layer
        return layer


class FakeCollectionChildren(list):
    def unlink(self, coll):
        if coll in self:
            self.remove(coll)


class FakeCollection:
    def __init__(self):
        self.children = FakeCollectionChildren()


class FakeScene:
    def __init__(self, name):
        self.name = name
        self.objects = []
        self.collection = FakeCollection()
        self.view_layers = FakeViewLayers()
        self.render = types.SimpleNamespace(filepath="", image_settings=types.SimpleNamespace(file_format="OPEN_EXR"))


class FakeScenes(dict):
    def get(self, name):
        return dict.get(self, name)

    def new(self, name):
        scene = FakeScene(name)
        self[name] = scene
        return scene


bpy.data = types.SimpleNamespace(
    scenes=FakeScenes(),
    objects=types.SimpleNamespace(remove=lambda obj, do_unlink=True: None),
    collections=types.SimpleNamespace(remove=lambda coll: None),
)
bpy.context = types.SimpleNamespace(window=types.SimpleNamespace(scene=None, view_layer=None))
_render_calls = []

def _render_stub(write_still=False):
    _render_calls.append(write_still)

bpy.ops = types.SimpleNamespace(render=types.SimpleNamespace(render=_render_stub))

from scene_nodes.engine import evaluator

def test_evaluate_scene_tree_triggers_render():
    patched = evaluator.evaluate_scene_tree
    reload(evaluator)

    bpy_mod = evaluator.bpy
    bpy_mod.data.scenes = FakeScenes()
    bpy_mod.data.objects = types.SimpleNamespace(remove=lambda obj, do_unlink=True: None)
    bpy_mod.data.collections = types.SimpleNamespace(remove=lambda coll: None)
    prev_ops = bpy_mod.ops.render
    bpy_mod.ops.render = types.SimpleNamespace(render=_render_stub)

    _render_calls.clear()
    rnode = types.SimpleNamespace(bl_idname="RenderNodeType", inputs=[], use_scene_name=False)
    old_scene = bpy_mod.context.window.scene
    tree = types.SimpleNamespace(nodes=[rnode])

    evaluator.evaluate_scene_tree(tree)

    assert len(_render_calls) == 1
    assert bpy_mod.context.window.scene is not None

    bpy_mod.ops.render = prev_ops
    bpy_mod.context.window.scene = old_scene
    evaluator.evaluate_scene_tree = patched


def test_evaluate_scene_tree_without_render_node():
    patched = evaluator.evaluate_scene_tree
    reload(evaluator)

    bpy_mod = evaluator.bpy
    bpy_mod.data.scenes = FakeScenes()
    bpy_mod.data.objects = types.SimpleNamespace(remove=lambda obj, do_unlink=True: None)
    bpy_mod.data.collections = types.SimpleNamespace(remove=lambda coll: None)
    prev_ops = bpy_mod.ops.render
    bpy_mod.ops.render = types.SimpleNamespace(render=_render_stub)

    _render_calls.clear()
    inode = types.SimpleNamespace(bl_idname="InputNodeType", inputs=[])
    old_scene = bpy_mod.context.window.scene
    tree = types.SimpleNamespace(nodes=[inode])

    evaluator.evaluate_scene_tree(tree)

    assert len(_render_calls) == 0
    assert bpy_mod.context.window.scene is not None

    bpy_mod.ops.render = prev_ops
    bpy_mod.context.window.scene = old_scene
    evaluator.evaluate_scene_tree = patched
