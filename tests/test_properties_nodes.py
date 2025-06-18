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
            use_simplify=False,
            motion_blur_shutter=0.0,
            use_freestyle=False,
        )
        self.frame_start = 1
        self.frame_end = 250
        self.cycles = types.SimpleNamespace(
            samples=0,
            max_bounces=0,
            diffuse_bounces=0,
            use_adaptive_sampling=False,
            volume_step_rate=1.0,
            hair_shape_radius=0.0,
            film_exposure=1.0,
            tile_x=0,
        )
        self.eevee = types.SimpleNamespace(
            taa_render_samples=0,
            use_motion_blur=False,
            use_taa_reprojection=False,
            clamp_direct=0.0,
            clamp_indirect=0.0,
            raytrace_resolution=0,
            motion_blur_shutter=0.0,
            film_exposure=1.0,
        )
        self.grease_pencil = types.SimpleNamespace(antialias_threshold=1.0)
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
        use_use_adaptive_sampling=True, use_adaptive_sampling=True,
        use_diffuse_bounces=True, diffuse_bounces=2,
        use_volume_step_rate=True, volume_step_rate=0.5,
        use_hair_shape_radius=True, hair_shape_radius=1.5,
        use_use_simplify=True, use_simplify=True,
        use_motion_blur_shutter=True, motion_blur_shutter=0.4,
        use_film_exposure=True, film_exposure=1.2,
        use_tile_x=True, tile_x=32,
        use_gpencil_antialias_threshold=True, gpencil_antialias_threshold=0.2,
        use_use_freestyle=True, use_freestyle=True,
        use_filepath=True, filepath="/tmp/a",
        use_file_format=True, file_format="PNG",
        use_color_mode=True, color_mode="RGBA",
    )
    scene = FakeScene()
    ctx = types.SimpleNamespace(render_pass="")
    evaluator._evaluate_cycles_properties(node, [], scene, ctx)

    assert scene.render.engine == "CYCLES"
    assert scene.render.resolution_x == 1280
    assert scene.render.resolution_y == 720
    assert scene.frame_start == 10
    assert scene.frame_end == 20
    assert scene.render.fps == 30
    assert scene.cycles.samples == 16
    assert scene.cycles.max_bounces == 4
    assert scene.cycles.diffuse_bounces == 2
    assert scene.cycles.use_adaptive_sampling is True
    assert scene.cycles.volume_step_rate == 0.5
    assert scene.cycles.hair_shape_radius == 1.5
    assert scene.render.use_simplify is True
    assert scene.render.motion_blur_shutter == 0.4
    assert scene.cycles.film_exposure == 1.2
    assert scene.cycles.tile_x == 32
    assert scene.grease_pencil.antialias_threshold == 0.2
    assert scene.render.use_freestyle is True
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
        use_use_taa_reprojection=True, use_taa_reprojection=True,
        use_clamp_direct=True, clamp_direct=0.1,
        use_clamp_indirect=True, clamp_indirect=0.2,
        use_raytrace_resolution=True, raytrace_resolution=256,
        use_motion_blur=True, motion_blur=True,
        use_motion_blur_shutter=True, motion_blur_shutter=0.3,
        use_film_exposure=True, film_exposure=1.1,
        use_filepath=True, filepath="/tmp/b",
        use_file_format=True, file_format="OPEN_EXR",
        use_color_mode=True, color_mode="RGB",
    )
    scene = FakeScene()
    ctx = types.SimpleNamespace(render_pass="")
    evaluator._evaluate_eevee_properties(node, [], scene, ctx)

    assert scene.render.engine == "BLENDER_EEVEE"
    assert scene.render.resolution_x == 1024
    assert scene.render.resolution_y == 512
    assert scene.frame_start == 5
    assert scene.frame_end == 15
    assert scene.render.fps == 60
    assert scene.eevee.taa_render_samples == 8
    assert scene.eevee.use_taa_reprojection is True
    assert scene.eevee.clamp_direct == 0.1
    assert scene.eevee.clamp_indirect == 0.2
    assert scene.eevee.raytrace_resolution == 256
    assert scene.eevee.use_motion_blur is True
    assert scene.eevee.motion_blur_shutter == 0.3
    assert scene.eevee.film_exposure == 1.1
    assert scene.render.filepath == "/tmp/b"
    assert scene.render.image_settings.file_format == "OPEN_EXR"
    assert scene.render.image_settings.color_mode == "RGB"

