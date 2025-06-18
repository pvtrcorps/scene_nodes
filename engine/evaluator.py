import bpy
import types
import fnmatch
from mathutils import Vector
from .filters import filter_objects


def _prepare_scene():
    """Return a clean scene used to evaluate the node tree."""
    name = "Scene Nodes"
    scene = bpy.data.scenes.get(name)
    if scene is None:
        scene = bpy.data.scenes.new(name)
    else:
        # Remove existing objects and collections
        for obj in list(scene.objects):
            bpy.data.objects.remove(obj, do_unlink=True)
        for coll in list(scene.collection.children):
            scene.collection.children.unlink(coll)
            bpy.data.collections.remove(coll)

    bpy.context.window.scene = scene
    return scene


def _get_node_dependencies(node):
    """Return a list of nodes that feed into *node* through linked inputs."""
    deps = []
    for socket in node.inputs:
        if socket.is_linked:
            for link in socket.links:
                deps.append(link.from_node)
    return deps


def _topological_sort(nodes):
    """Return nodes sorted so dependencies appear before dependents."""
    order = []
    visited = set()
    visiting = set()

    def visit(n):
        if id(n) in visited:
            return
        if id(n) in visiting:
            raise RuntimeError("Cycle detected in scene node tree")
        visiting.add(id(n))
        for dep in _get_node_dependencies(n):
            visit(dep)
        visiting.remove(id(n))
        visited.add(id(n))
        order.append(n)

    for n in nodes:
        visit(n)
    return order


def _socket_value(node, name, default=None):
    sock = node.inputs.get(name)
    if sock is None:
        return default
    if sock.is_linked and sock.links:
        return getattr(sock.links[0].from_socket, "value", default)
    return getattr(sock, "value", default)


def _collect_input_scenes(node):
    """Gather evaluated scenes from linked inputs."""
    scenes = []
    for sock in node.inputs:
        if sock.bl_idname == "SceneSocketType" and sock.is_linked:
            for link in sock.links:
                from_node = link.from_node
                scenes.append(getattr(from_node, "scene_nodes_output", None))
    return scenes


def _evaluate_blend_input(node, _inputs, scene, context):
    filepath = (
        _socket_value(node, "File Path", getattr(node, "file_path", ""))
        if getattr(node, "use_file_path", False)
        else ""
    )
    collection_path = (
        _socket_value(node, "Collection Path", getattr(node, "collection_path", ""))
        if getattr(node, "use_collection_path", False)
        else ""
    )
    load_mode = (
        _socket_value(node, "Load Mode", getattr(node, "load_mode", "APPEND"))
        if getattr(node, "use_load_mode", False)
        else getattr(node, "load_mode", "APPEND")
    )
    filter_expr = (
        _socket_value(node, "Filter", getattr(node, "filter_expr", ""))
        if getattr(node, "use_filter_expr", False)
        else getattr(node, "filter_expr", "")
    )
    if not filepath:
        node.scene_nodes_output = None
        return None

    link = load_mode in {"LINK", "OVERRIDE"}
    with bpy.data.libraries.load(filepath, link=link) as (data_from, data_to):
        if collection_path:
            if collection_path in data_from.collections:
                data_to.collections = [collection_path]
        elif filter_expr:
            matches = [name for name in data_from.collections if fnmatch.fnmatchcase(name, filter_expr)]
            data_to.collections = matches

    collections = list(data_to.collections) if data_to.collections else []
    if not collections:
        node.scene_nodes_output = None
        return None

    processed = []
    for collection in collections:
        coll = collection
        if filter_expr and collection_path:
            objs = list(filter_objects(coll.objects, filter_expr))
            filtered = bpy.data.collections.new(name=f"{coll.name}_filtered")
            for obj in objs:
                filtered.objects.link(obj)
            coll = filtered
        processed.append(coll)

    if len(processed) > 1:
        # Create a wrapper collection combining all loaded collections
        wrapper = bpy.data.collections.new(name=f"{node.name}_group")
        for coll in processed:
            for obj in coll.objects:
                if obj.name not in wrapper.objects:
                    wrapper.objects.link(obj)
        collection = wrapper
    else:
        collection = processed[0]

    if load_mode == "OVERRIDE":
        # Link, create override and remove original link to avoid duplicates
        scene.collection.children.link(collection)
        overridden = collection.override_create(scene.collection)
        scene.collection.children.unlink(collection)
        if collection.users == 0:
            bpy.data.collections.remove(collection)
        collection = overridden
    elif load_mode == "INSTANCE":
        # Remove previous instance wrapper and object if they exist
        wrapper_name = f"{collection.name}_instance"
        obj_name = f"{collection.name}_inst"
        old_wrapper = bpy.data.collections.get(wrapper_name)
        if old_wrapper:
            for obj in list(old_wrapper.objects):
                bpy.data.objects.remove(obj, do_unlink=True)
            bpy.data.collections.remove(old_wrapper)
        if obj_name in bpy.data.objects:
            bpy.data.objects.remove(bpy.data.objects[obj_name], do_unlink=True)

        # Create a new wrapper collection with a collection instance object
        wrapper = bpy.data.collections.new(name=wrapper_name)
        scene.collection.children.link(wrapper)
        inst_obj = bpy.data.objects.new(name=obj_name, object_data=None)
        inst_obj.instance_type = 'COLLECTION'
        inst_obj.instance_collection = collection
        wrapper.objects.link(inst_obj)
        collection = wrapper
    else:
        scene.collection.children.link(collection)

    node.scene_nodes_output = collection
    return collection


def _evaluate_alembic_import(node, _inputs, scene, context):
    filepath = (
        _socket_value(node, "File Path", getattr(node, "file_path", ""))
        if getattr(node, "use_file_path", False)
        else ""
    )
    if not filepath:
        node.scene_nodes_output = None
        return None

    scale = (
        _socket_value(node, "Scale", getattr(node, "scale", 1.0))
        if getattr(node, "use_scale", False)
        else getattr(node, "scale", 1.0)
    )
    set_frame_range = (
        _socket_value(node, "Set Frame Range", getattr(node, "set_frame_range", True))
        if getattr(node, "use_set_frame_range", False)
        else getattr(node, "set_frame_range", True)
    )
    validate_meshes = (
        _socket_value(node, "Validate Meshes", getattr(node, "validate_meshes", False))
        if getattr(node, "use_validate_meshes", False)
        else getattr(node, "validate_meshes", False)
    )
    add_cache_reader = (
        _socket_value(node, "Add Cache Reader", getattr(node, "always_add_cache_reader", False))
        if getattr(node, "use_always_add_cache_reader", False)
        else getattr(node, "always_add_cache_reader", False)
    )
    is_sequence = (
        _socket_value(node, "Is Sequence", getattr(node, "is_sequence", False))
        if getattr(node, "use_is_sequence", False)
        else getattr(node, "is_sequence", False)
    )
    background_job = (
        _socket_value(node, "Background Job", getattr(node, "as_background_job", False))
        if getattr(node, "use_as_background_job", False)
        else getattr(node, "as_background_job", False)
    )

    existing = set(scene.objects)
    bpy.ops.wm.alembic_import(
        filepath=filepath,
        as_background_job=background_job,
        set_frame_range=set_frame_range,
        validate_meshes=validate_meshes,
        is_sequence=is_sequence,
        scale=scale,
        always_add_cache_reader=add_cache_reader,
    )

    collection = bpy.data.collections.new(name=f"{node.name}_abc")
    scene.collection.children.link(collection)
    for obj in scene.objects:
        if obj not in existing:
            collection.objects.link(obj)
            scene.collection.objects.unlink(obj)

    node.scene_nodes_output = collection
    return collection


def _evaluate_transform(node, inputs, context):
    t = (
        Vector(
            _socket_value(node, "Translate", getattr(node, "translate", (0.0, 0.0, 0.0)))
        )
        if getattr(node, "use_translate", False)
        else Vector((0.0, 0.0, 0.0))
    )
    r = (
        Vector(
            _socket_value(node, "Rotate", getattr(node, "rotate", (0.0, 0.0, 0.0)))
        )
        if getattr(node, "use_rotate", False)
        else Vector((0.0, 0.0, 0.0))
    )
    s = (
        Vector(
            _socket_value(node, "Scale", getattr(node, "scale", (1.0, 1.0, 1.0)))
        )
        if getattr(node, "use_scale", False)
        else Vector((1.0, 1.0, 1.0))
    )

    filter_expr = (
        _socket_value(node, "Filter", getattr(node, "filter_expr", ""))
        if getattr(node, "use_filter_expr", False)
        else ""
    )

    for coll in inputs:
        if coll is None:
            continue
        objs = coll.objects
        if filter_expr:
            objs = list(filter_objects(objs, filter_expr))
        for obj in objs:
            obj.location = Vector(obj.location) + t
            obj.rotation_euler = Vector(obj.rotation_euler) + r
            obj.scale = Vector(obj.scale) * s

    node.scene_nodes_output = inputs[0] if inputs else None
    return node.scene_nodes_output


def _evaluate_group(node, inputs, scene, context):
    collection = bpy.data.collections.new(name=f"{node.name}_group")
    scene.collection.children.link(collection)
    for coll in inputs:
        if coll is None:
            continue
        for obj in coll.objects:
            if obj.name not in collection.objects:
                collection.objects.link(obj)

    node.scene_nodes_output = collection
    return collection


def _evaluate_light(node, _inputs, scene, context):
    ltype = (
        _socket_value(node, "Type", getattr(node, "light_type", "POINT"))
        if getattr(node, "use_light_type", False)
        else getattr(node, "light_type", "POINT")
    )
    energy = (
        _socket_value(node, "Energy", getattr(node, "energy", 1.0))
        if getattr(node, "use_energy", False)
        else None
    )
    color = (
        _socket_value(node, "Color", getattr(node, "color", (1.0, 1.0, 1.0)))
        if getattr(node, "use_color", False)
        else None
    )

    light_data = bpy.data.lights.new(name=node.name, type=ltype)
    if energy is not None:
        light_data.energy = energy
    if color is not None:
        light_data.color = color

    light_obj = bpy.data.objects.new(node.name, light_data)
    scene.collection.objects.link(light_obj)

    node.scene_nodes_output = scene.collection
    return node.scene_nodes_output


def _evaluate_global_options(node, _inputs, scene, context):
    if getattr(node, "use_res_x", False):
        res_x = _socket_value(node, "Resolution X", getattr(node, "res_x", 1920))
        scene.render.resolution_x = res_x

    if getattr(node, "use_res_y", False):
        res_y = _socket_value(node, "Resolution Y", getattr(node, "res_y", 1080))
        scene.render.resolution_y = res_y

    if getattr(node, "use_samples", False):
        samples = _socket_value(node, "Samples", getattr(node, "samples", 128))
        scene.cycles.samples = samples if hasattr(scene, "cycles") else samples

    if getattr(node, "use_camera_path", False):
        camera_path = _socket_value(node, "Camera Path", getattr(node, "camera_path", ""))
        if camera_path in bpy.data.objects:
            scene.camera = bpy.data.objects[camera_path]

    node.scene_nodes_output = scene.collection
    return node.scene_nodes_output


def _evaluate_cycles_properties(node, _inputs, scene, context):
    scene.render.engine = "CYCLES"

    if getattr(node, "use_res_x", False):
        scene.render.resolution_x = _socket_value(node, "Resolution X", getattr(node, "res_x", 1920))

    if getattr(node, "use_res_y", False):
        scene.render.resolution_y = _socket_value(node, "Resolution Y", getattr(node, "res_y", 1080))

    if getattr(node, "use_frame_start", False):
        scene.frame_start = _socket_value(node, "Frame Start", getattr(node, "frame_start", scene.frame_start))

    if getattr(node, "use_frame_end", False):
        scene.frame_end = _socket_value(node, "Frame End", getattr(node, "frame_end", scene.frame_end))

    if getattr(node, "use_fps", False):
        scene.render.fps = _socket_value(node, "FPS", getattr(node, "fps", scene.render.fps))

    if getattr(node, "use_camera_path", False):
        camera_path = _socket_value(node, "Camera Path", getattr(node, "camera_path", ""))
        if camera_path in bpy.data.objects:
            scene.camera = bpy.data.objects[camera_path]

    if getattr(node, "use_samples", False):
        scene.cycles.samples = _socket_value(node, "Samples", getattr(node, "samples", 64))

    if getattr(node, "use_max_bounces", False):
        scene.cycles.max_bounces = _socket_value(node, "Max Bounces", getattr(node, "max_bounces", 8))

    if getattr(node, "use_diffuse_bounces", False):
        scene.cycles.diffuse_bounces = _socket_value(node, "Diffuse Bounces", getattr(node, "diffuse_bounces", 4))

    if getattr(node, "use_adaptive_sampling", False):
        scene.cycles.use_adaptive_sampling = _socket_value(node, "Adaptive Sampling", getattr(node, "use_adaptive_sampling", False))

    if getattr(node, "use_volume_step_rate", False):
        scene.cycles.volume_step_rate = _socket_value(node, "Volume Step Rate", getattr(node, "volume_step_rate", 1.0))

    if getattr(node, "use_hair_shape_radius", False):
        scene.cycles.hair_shape_radius = _socket_value(node, "Hair Shape Radius", getattr(node, "hair_shape_radius", 1.0))

    if getattr(node, "use_simplify", False):
        scene.render.use_simplify = _socket_value(node, "Use Simplify", getattr(node, "use_simplify", False))

    if getattr(node, "use_motion_blur_shutter", False):
        scene.render.motion_blur_shutter = _socket_value(node, "Shutter", getattr(node, "motion_blur_shutter", 0.5))

    if getattr(node, "use_film_exposure", False):
        scene.cycles.film_exposure = _socket_value(node, "Exposure", getattr(node, "film_exposure", 1.0))

    if getattr(node, "use_tile_x", False):
        scene.cycles.tile_x = _socket_value(node, "Tile X", getattr(node, "tile_x", 64))

    if getattr(node, "use_gpencil_antialias_threshold", False):
        gp = getattr(scene, "grease_pencil", types.SimpleNamespace(antialias_threshold=1.0))
        gp.antialias_threshold = _socket_value(node, "Grease Pencil AA", getattr(node, "gpencil_antialias_threshold", 1.0))
        scene.grease_pencil = gp

    if getattr(node, "use_use_freestyle", False):
        scene.render.use_freestyle = _socket_value(node, "Use Freestyle", getattr(node, "use_freestyle", False))

    if getattr(node, "use_filepath", False):
        scene.render.filepath = _socket_value(node, "File Path", getattr(node, "filepath", ""))

    if getattr(node, "use_file_format", False):
        scene.render.image_settings.file_format = _socket_value(node, "Format", getattr(node, "file_format", "OPEN_EXR"))

    if getattr(node, "use_color_mode", False):
        scene.render.image_settings.color_mode = _socket_value(node, "Color", getattr(node, "color_mode", "RGB"))

    node.scene_nodes_output = scene.collection
    return node.scene_nodes_output


def _evaluate_eevee_properties(node, _inputs, scene, context):
    scene.render.engine = "BLENDER_EEVEE"

    if getattr(node, "use_res_x", False):
        scene.render.resolution_x = _socket_value(node, "Resolution X", getattr(node, "res_x", 1920))

    if getattr(node, "use_res_y", False):
        scene.render.resolution_y = _socket_value(node, "Resolution Y", getattr(node, "res_y", 1080))

    if getattr(node, "use_frame_start", False):
        scene.frame_start = _socket_value(node, "Frame Start", getattr(node, "frame_start", scene.frame_start))

    if getattr(node, "use_frame_end", False):
        scene.frame_end = _socket_value(node, "Frame End", getattr(node, "frame_end", scene.frame_end))

    if getattr(node, "use_fps", False):
        scene.render.fps = _socket_value(node, "FPS", getattr(node, "fps", scene.render.fps))

    if getattr(node, "use_camera_path", False):
        camera_path = _socket_value(node, "Camera Path", getattr(node, "camera_path", ""))
        if camera_path in bpy.data.objects:
            scene.camera = bpy.data.objects[camera_path]

    if getattr(node, "use_samples", False):
        scene.eevee.taa_render_samples = _socket_value(node, "Samples", getattr(node, "samples", 64))

    if getattr(node, "use_use_taa_reprojection", False):
        scene.eevee.use_taa_reprojection = _socket_value(node, "TAA Reprojection", getattr(node, "use_taa_reprojection", False))

    if getattr(node, "use_clamp_direct", False):
        scene.eevee.clamp_direct = _socket_value(node, "Clamp Direct", getattr(node, "clamp_direct", 0.0))

    if getattr(node, "use_clamp_indirect", False):
        scene.eevee.clamp_indirect = _socket_value(node, "Clamp Indirect", getattr(node, "clamp_indirect", 0.0))

    if getattr(node, "use_raytrace_resolution", False):
        scene.eevee.raytrace_resolution = _socket_value(node, "Raytrace Resolution", getattr(node, "raytrace_resolution", 512))

    if getattr(node, "use_motion_blur", False):
        scene.eevee.use_motion_blur = _socket_value(node, "Motion Blur", getattr(node, "motion_blur", False))

    if getattr(node, "use_motion_blur_shutter", False):
        scene.eevee.motion_blur_shutter = _socket_value(node, "Shutter", getattr(node, "motion_blur_shutter", 0.5))

    if getattr(node, "use_film_exposure", False):
        scene.eevee.film_exposure = _socket_value(node, "Exposure", getattr(node, "film_exposure", 1.0))

    if getattr(node, "use_filepath", False):
        scene.render.filepath = _socket_value(node, "File Path", getattr(node, "filepath", ""))

    if getattr(node, "use_file_format", False):
        scene.render.image_settings.file_format = _socket_value(node, "Format", getattr(node, "file_format", "OPEN_EXR"))

    if getattr(node, "use_color_mode", False):
        scene.render.image_settings.color_mode = _socket_value(node, "Color", getattr(node, "color_mode", "RGB"))

    node.scene_nodes_output = scene.collection
    return node.scene_nodes_output



def _evaluate_cycles_attributes(node, inputs, scene, context):
    filter_expr = (
        _socket_value(node, "Filter", getattr(node, "filter_expr", ""))
        if getattr(node, "use_filter_expr", False)
        else ""
    )

    for coll in inputs:
        if coll is None:
            continue
        objs = coll.objects
        if filter_expr:
            objs = list(filter_objects(objs, filter_expr))
        for obj in objs:
            if getattr(node, "use_hide_render", False):
                obj.hide_render = bool(
                    _socket_value(node, "Hide Render", getattr(node, "hide_render", False))
                )
            if getattr(node, "use_is_shadow_catcher", False):
                obj.is_shadow_catcher = bool(
                    _socket_value(node, "Shadow Catcher", getattr(node, "is_shadow_catcher", False))
                )
            if getattr(node, "use_is_holdout", False):
                obj.is_holdout = bool(
                    _socket_value(node, "Holdout", getattr(node, "is_holdout", False))
                )
            if getattr(node, "use_visible_camera", False):
                obj.visible_camera = bool(
                    _socket_value(node, "Visible Camera", getattr(node, "visible_camera", True))
                )
            if getattr(node, "use_visible_diffuse", False):
                obj.visible_diffuse = bool(
                    _socket_value(node, "Visible Diffuse", getattr(node, "visible_diffuse", True))
                )
            if getattr(node, "use_visible_glossy", False):
                obj.visible_glossy = bool(
                    _socket_value(node, "Visible Glossy", getattr(node, "visible_glossy", True))
                )
            if getattr(node, "use_visible_transmission", False):
                obj.visible_transmission = bool(
                    _socket_value(node, "Visible Transmission", getattr(node, "visible_transmission", True))
                )
            if getattr(node, "use_visible_volume_scatter", False):
                obj.visible_volume_scatter = bool(
                    _socket_value(node, "Visible Volume", getattr(node, "visible_volume_scatter", True))
                )
            if getattr(node, "use_visible_shadow", False):
                obj.visible_shadow = bool(
                    _socket_value(node, "Visible Shadow", getattr(node, "visible_shadow", True))
                )

    node.scene_nodes_output = inputs[0] if inputs else None
    return node.scene_nodes_output


def _evaluate_eevee_attributes(node, inputs, scene, context):
    return _evaluate_cycles_attributes(node, inputs, scene, context)


def _evaluate_render_engine(node, _inputs, scene, context):
    scene.render.engine = node.engine
    if node.engine == 'CYCLES':
        if getattr(node, "use_feature_set", False):
            scene.cycles.feature_set = _socket_value(node, "Feature Set", getattr(node, "feature_set", "SUPPORTED"))
        if getattr(node, "use_device", False):
            scene.cycles.device = _socket_value(node, "Device", getattr(node, "device", "CPU"))
        if getattr(node, "use_open_shading_language", False):
            scene.cycles.use_osl = bool(_socket_value(node, "Open Shading Language", getattr(node, "open_shading_language", False)))

    node.scene_nodes_output = scene.collection
    return node.scene_nodes_output


def _evaluate_join_string(node, _inputs, _scene, context):
    s1 = (
        _socket_value(node, "String 1", getattr(node, "string1", ""))
        if getattr(node, "use_string1", False)
        else getattr(node, "string1", "")
    )
    s2 = (
        _socket_value(node, "String 2", getattr(node, "string2", ""))
        if getattr(node, "use_string2", False)
        else getattr(node, "string2", "")
    )
    delim = (
        _socket_value(node, "Delimiter", getattr(node, "delimiter", ""))
        if getattr(node, "use_delimiter", False)
        else getattr(node, "delimiter", "")
    )
    result = delim.join([s1, s2]) if delim else s1 + s2
    out = node.outputs.get("String")
    if out is not None:
        out.value = result
    node.scene_nodes_output = None
    return None


def _evaluate_split_string(node, _inputs, _scene, context):
    text = (
        _socket_value(node, "String", getattr(node, "string", ""))
        if getattr(node, "use_string", False)
        else getattr(node, "string", "")
    )
    sep = (
        _socket_value(node, "Separator", getattr(node, "separator", ""))
        if getattr(node, "use_separator", False)
        else getattr(node, "separator", "")
    )
    parts = text.split(sep, 1) if sep else [text]
    first = parts[0] if parts else ""
    second = parts[1] if len(parts) > 1 else ""
    if node.outputs:
        out1 = node.outputs.get("Part 1")
        if out1 is not None:
            out1.value = first
        out2 = node.outputs.get("Part 2")
        if out2 is not None:
            out2.value = second
    node.scene_nodes_output = None
    return None


def _evaluate_name_switch(node, _inputs, _scene, context):
    target = getattr(context, "render_pass", "")
    chosen = None
    default = None
    for sock in node.inputs:
        if sock.bl_idname != "SceneSocketType" or not sock.is_linked:
            continue
        if not sock.links:
            continue
        scene_in = getattr(sock.links[0].from_node, "scene_nodes_output", None)
        if sock.name == target:
            chosen = scene_in
            break
        if sock.name == "Default" and default is None:
            default = scene_in
    if chosen is None:
        chosen = default
    node.scene_nodes_output = chosen
    return chosen


def _evaluate_input(node, _inputs, _scene, context):
    node.scene_nodes_output = None
    return None


def _evaluate_render(node, inputs, scene, context):
    if getattr(node, "use_filepath", False):
        scene.render.filepath = _socket_value(node, "File Path", getattr(node, "filepath", ""))

    if getattr(node, "use_file_format", False):
        scene.render.image_settings.file_format = _socket_value(node, "Format", getattr(node, "file_format", "OPEN_EXR"))

    node.scene_nodes_output = inputs[0] if inputs else None
    return node.scene_nodes_output


def _evaluate_node(node, scene, context):
    inputs = _collect_input_scenes(node)
    ntype = node.bl_idname
    if ntype == "BlendInputNodeType":
        return _evaluate_blend_input(node, inputs, scene, context)
    elif ntype == "AlembicImportNodeType":
        return _evaluate_alembic_import(node, inputs, scene, context)
    elif ntype == "TransformNodeType":
        return _evaluate_transform(node, inputs, context)
    elif ntype == "GroupNodeType":
        return _evaluate_group(node, inputs, scene, context)
    elif ntype == "CyclesAttributesNodeType":
        return _evaluate_cycles_attributes(node, inputs, scene, context)
    elif ntype == "EeveeAttributesNodeType":
        return _evaluate_eevee_attributes(node, inputs, scene, context)
    elif ntype == "RenderEngineNodeType":
        return _evaluate_render_engine(node, inputs, scene, context)
    elif ntype == "LightNodeType":
        return _evaluate_light(node, inputs, scene, context)
    elif ntype == "GlobalOptionsNodeType":
        return _evaluate_global_options(node, inputs, scene, context)
    elif ntype == "CyclesPropertiesNodeType":
        return _evaluate_cycles_properties(node, inputs, scene, context)
    elif ntype == "EeveePropertiesNodeType":
        return _evaluate_eevee_properties(node, inputs, scene, context)
    elif ntype == "RenderNodeType":
        return _evaluate_render(node, inputs, scene, context)
    elif ntype == "InputNodeType":
        return _evaluate_input(node, inputs, scene, context)
    elif ntype == "JoinStringNodeType":
        return _evaluate_join_string(node, inputs, scene, context)
    elif ntype == "SplitStringNodeType":
        return _evaluate_split_string(node, inputs, scene, context)
    elif ntype == "NameSwitchNodeType":
        return _evaluate_name_switch(node, inputs, scene, context)
    else:
        print(f"[scene_nodes] unknown node type {ntype}")


def evaluate_scene_tree(tree):
    """Evaluate *tree* and execute Render nodes when present."""
    if tree is None:
        raise ValueError("Scene node tree is None")

    renders = [n for n in tree.nodes if n.bl_idname == "RenderNodeType"]

    if renders:
        context = types.SimpleNamespace()
        for rnode in renders:
            if getattr(rnode, "use_scene_name", False):
                context.render_pass = _socket_value(
                    rnode,
                    "Name",
                    getattr(rnode, "scene_name", ""),
                ) or "Scene"
            else:
                context.render_pass = "Scene"
            scene = _prepare_scene()
            order = _topological_sort([rnode])
            for node in order:
                node.scene_nodes_output = _evaluate_node(node, scene, context)
            bpy.ops.render.render(write_still=True)
    else:
        context = types.SimpleNamespace(render_pass="Scene")
        scene = _prepare_scene()
        order = _topological_sort(list(tree.nodes))
        for node in order:
            node.scene_nodes_output = _evaluate_node(node, scene, context)

