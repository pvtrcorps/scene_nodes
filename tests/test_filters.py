from types import SimpleNamespace
from scene_nodes.engine.filters import matches, object_path

obj = SimpleNamespace(name="Cube", users_collection=[SimpleNamespace(name="Coll", parent=None)])
assert object_path(obj) == "Coll/Cube"
assert matches(obj, "Coll/*")
assert matches(obj, "Cube")
