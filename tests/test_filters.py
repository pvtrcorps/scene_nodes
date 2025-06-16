import types
from types import SimpleNamespace
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
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
mathutils = types.ModuleType("mathutils")
mathutils.Vector = tuple
sys.modules.setdefault("mathutils", mathutils)
nodeitems_utils = types.ModuleType("nodeitems_utils")
nodeitems_utils.register_node_categories = lambda *a, **k: None
nodeitems_utils.unregister_node_categories = lambda *a, **k: None
nodeitems_utils.NodeCategory = type("NodeCategory", (), {"__init__": lambda self,*a,**k: None})
nodeitems_utils.NodeItem = lambda *a, **k: None
nodeitems_utils.NodeItem = lambda *a, **k: None
sys.modules.setdefault("nodeitems_utils", nodeitems_utils)

from scene_nodes.engine.filters import matches, object_path

obj = SimpleNamespace(name="Cube", users_collection=[SimpleNamespace(name="Coll", parent=None)])
assert object_path(obj) == "Coll/Cube"
assert matches(obj, "Coll/*")
assert matches(obj, "Cube")
