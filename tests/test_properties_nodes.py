import types
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

# Stub Blender modules
bpy = types.ModuleType("bpy")
bpy.__path__ = []
bpy.data = types.SimpleNamespace(objects={})
bpy.context = types.SimpleNamespace(window=types.SimpleNamespace())
bpy.utils = types.SimpleNamespace(register_class=lambda *a, **k: None,
                                  unregister_class=lambda *a, **k: None)
bpy.types = types.ModuleType("bpy.types")
bpy.props = types.SimpleNamespace(FloatProperty=lambda **k: None, IntProperty=lambda **k: None, BoolProperty=lambda **k: None, FloatVectorProperty=lambda **k: None, StringProperty=lambda **k: None, EnumProperty=lambda **k: None)
bpy.types.NodeTree = type("NodeTree", (), {})
bpy.types.Node = type("Node", (), {})
bpy.types.NodeSocket = type("NodeSocket", (), {})
bpy.types.Operator = type("Operator", (), {})
bpy.types.Panel = type("Panel", (), {})
sys.modules.setdefault("bpy", bpy)
sys.modules.setdefault("bpy.types", bpy.types)

nodeitems_utils = types.ModuleType("nodeitems_utils")
nodeitems_utils.register_node_categories = lambda *a, **k: None
nodeitems_utils.unregister_node_categories = lambda *a, **k: None
nodeitems_utils.NodeCategory = type("NodeCategory", (), {"__init__": lambda self,*a,**k: None})
nodeitems_utils.NodeItem = lambda *a, **k: None
nodeitems_utils.NodeItem = lambda *a, **k: None
sys.modules.setdefault("nodeitems_utils", nodeitems_utils)

mathutils = types.ModuleType("mathutils")
mathutils.Vector = tuple
sys.modules.setdefault("mathutils", mathutils)

from scene_nodes.engine import evaluator

class FakeScene:
    def __init__(self):
        self.render = types.SimpleNamespace(
            engine="",
            resolution_x=0,
            resolution_y=0,
            filepath="",
            fps=24,
            image_settings=types.SimpleNamespace(file_format="", color_mode=""),
        )
        self.frame_start = 1
        self.frame_end = 250
        self.cycles = types.SimpleNamespace(samples=0, max_bounces=0)
        self.eevee = types.SimpleNamespace(taa_render_samples=0, use_motion_blur=False)
        self.collection = object()
        self.camera = None


def test_cycles_properties():
    node = types.SimpleNamespace(
        inputs={},
        use_res_x=True, res_x=1280,
        use_res_y=True, res_y=720,
        use_frame_start=True, frame_start=10,
        use_frame_end=True, frame_end=20,
        use_fps=True, fps=30,
        use_camera_path=False,
        use_samples=True, samples=16,
        use_max_bounces=True, max_bounces=4,
        use_filepath=True, filepath="/tmp/a",
        use_file_format=True, file_format="PNG",
        use_color_mode=True, color_mode="RGBA",
    )
    scene = FakeScene()
    evaluator._evaluate_cycles_properties(node, [], scene)

    assert scene.render.engine == "CYCLES"
    assert scene.render.resolution_x == 1280
    assert scene.render.resolution_y == 720
    assert scene.frame_start == 10
    assert scene.frame_end == 20
    assert scene.render.fps == 30
    assert scene.cycles.samples == 16
    assert scene.cycles.max_bounces == 4
    assert scene.render.filepath == "/tmp/a"
    assert scene.render.image_settings.file_format == "PNG"
    assert scene.render.image_settings.color_mode == "RGBA"


def test_eevee_properties():
    node = types.SimpleNamespace(
        inputs={},
        use_res_x=True, res_x=1024,
        use_res_y=True, res_y=512,
        use_frame_start=True, frame_start=5,
        use_frame_end=True, frame_end=15,
        use_fps=True, fps=60,
        use_camera_path=False,
        use_samples=True, samples=8,
        use_motion_blur=True, motion_blur=True,
        use_filepath=True, filepath="/tmp/b",
        use_file_format=True, file_format="OPEN_EXR",
        use_color_mode=True, color_mode="RGB",
    )
    scene = FakeScene()
    evaluator._evaluate_eevee_properties(node, [], scene)

    assert scene.render.engine == "BLENDER_EEVEE"
    assert scene.render.resolution_x == 1024
    assert scene.render.resolution_y == 512
    assert scene.frame_start == 5
    assert scene.frame_end == 15
    assert scene.render.fps == 60
    assert scene.eevee.taa_render_samples == 8
    assert scene.eevee.use_motion_blur is True
    assert scene.render.filepath == "/tmp/b"
    assert scene.render.image_settings.file_format == "OPEN_EXR"
    assert scene.render.image_settings.color_mode == "RGB"
