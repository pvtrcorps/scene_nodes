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
sys.modules.setdefault("bpy", bpy)
sys.modules.setdefault("bpy.types", bpy.types)

nodeitems_utils = types.ModuleType("nodeitems_utils")
nodeitems_utils.register_node_categories = lambda *a, **k: None
nodeitems_utils.unregister_node_categories = lambda *a, **k: None
nodeitems_utils.NodeCategory = type("NodeCategory", (), {"__init__": lambda self,*a,**k: None})
nodeitems_utils.NodeItem = lambda *a, **k: None
sys.modules.setdefault("nodeitems_utils", nodeitems_utils)

mathutils = types.ModuleType("mathutils")
mathutils.Vector = tuple
sys.modules.setdefault("mathutils", mathutils)

from scene_nodes.engine import evaluator

class FakeObjects(list):
    def link(self, obj):
        self.append(obj)
    def unlink(self, obj):
        if obj in self:
            self.remove(obj)

class FakeCollection:
    def __init__(self, name):
        self.name = name
        self.objects = FakeObjects()
        self.children = FakeObjects()
        self.users = 0
        self.parent = None
    def override_create(self, parent):
        # simple stub returning self
        return self

class FakeScene:
    def __init__(self):
        self.collection = FakeCollection("Root")

class FakeLibLoad:
    def __init__(self, collections):
        self.collections = collections
    def __enter__(self):
        self.data_from = types.SimpleNamespace(collections=list(self.collections.keys()))
        self.data_to = types.SimpleNamespace(collections=[])
        return (self.data_from, self.data_to)
    def __exit__(self, exc_type, exc, tb):
        self.data_to.collections = [self.collections[name] for name in self.data_to.collections]
        return False

def make_env(collections):
    bpy.data = types.SimpleNamespace(
        libraries=types.SimpleNamespace(load=lambda path, link=False: FakeLibLoad(collections)),
        collections=types.SimpleNamespace(new=lambda name: FakeCollection(name), get=lambda name: None, remove=lambda coll: None),
        objects=types.SimpleNamespace(remove=lambda obj, do_unlink=True: None, new=lambda name, object_data=None: types.SimpleNamespace(name=name)),
    )
    evaluator.bpy.data = bpy.data


def test_scene_instance_no_filter():
    src = FakeCollection("Coll")
    a = types.SimpleNamespace(name="A", users_collection=[src])
    b = types.SimpleNamespace(name="B", users_collection=[src])
    src.objects.link(a)
    src.objects.link(b)
    make_env({"Coll": src})

    node = types.SimpleNamespace(
        inputs={},
        use_file_path=True, file_path="dummy.blend",
        use_collection_path=True, collection_path="Coll",
        use_load_mode=True, load_mode="APPEND",
        use_filter_expr=False, filter_expr="",
    )
    scene = FakeScene()
    ctx = types.SimpleNamespace(render_pass="")

    result = evaluator._evaluate_blend_input(node, [], scene, ctx)

    assert result is src
    assert src in scene.collection.children


def test_scene_instance_with_filter():
    src = FakeCollection("Coll")
    a = types.SimpleNamespace(name="A", users_collection=[src])
    b = types.SimpleNamespace(name="B", users_collection=[src])
    src.objects.link(a)
    src.objects.link(b)
    make_env({"Coll": src})

    node = types.SimpleNamespace(
        inputs={},
        use_file_path=True, file_path="dummy.blend",
        use_collection_path=True, collection_path="Coll",
        use_load_mode=True, load_mode="APPEND",
        use_filter_expr=True, filter_expr="B*",
    )
    scene = FakeScene()
    ctx = types.SimpleNamespace(render_pass="")

    result = evaluator._evaluate_blend_input(node, [], scene, ctx)

    assert result is not src
    assert len(result.objects) == 1
    assert result.objects[0].name == "B"
    assert result in scene.collection.children


def test_scene_instance_collection_filtering():
    c1 = FakeCollection("CollA")
    c2 = FakeCollection("CollB")
    o1 = types.SimpleNamespace(name="A1", users_collection=[c1])
    o2 = types.SimpleNamespace(name="B1", users_collection=[c2])
    c1.objects.link(o1)
    c2.objects.link(o2)
    make_env({"CollA": c1, "CollB": c2})

    node = types.SimpleNamespace(
        name="Node",
        inputs={},
        use_file_path=True, file_path="dummy.blend",
        use_collection_path=False, collection_path="",
        use_load_mode=True, load_mode="APPEND",
        use_filter_expr=True, filter_expr="Coll*",
    )
    scene = FakeScene()
    ctx = types.SimpleNamespace(render_pass="")

    result = evaluator._evaluate_blend_input(node, [], scene, ctx)

    assert result in scene.collection.children
    assert len(result.objects) == 2

