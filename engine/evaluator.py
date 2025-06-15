import bpy
from mathutils import Vector


def _prepare_scene(name="Scene Nodes"):
    """Return a clean scene to evaluate the node tree."""
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


def _is_exposed(node, attr):
    expose_map = getattr(node.__class__, '_expose_prop_map', {})
    expose_prop = expose_map.get(attr)
    if expose_prop is None:
        return True
    return getattr(node, expose_prop)


def _get_exposed_value(node, label, attr, default=None):
    if not _is_exposed(node, attr):
        return None
    return _socket_value(node, label, getattr(node, attr, default))


def _collect_input_scenes(node):
    """Gather evaluated scenes from linked inputs."""
    scenes = []
    for sock in node.inputs:
        if sock.bl_idname == "SceneSocketType" and sock.is_linked:
            for link in sock.links:
                from_node = link.from_node
                scenes.append(getattr(from_node, "scene_nodes_output", None))
    return scenes


def _evaluate_scene_instance(node, _inputs, scene):
    if not _is_exposed(node, "file_path") or not _is_exposed(node, "collection_path"):
        node.scene_nodes_output = None
        return None

    filepath = _get_exposed_value(node, "File Path", "file_path", "")
    collection_path = _get_exposed_value(node, "Collection Path", "collection_path", "")
    load_mode = _get_exposed_value(node, "Load Mode", "load_mode", "APPEND") or "APPEND"
    if not filepath or not collection_path:
        node.scene_nodes_output = None
        return None

    link = load_mode in {"LINK", "OVERRIDE"}
    with bpy.data.libraries.load(filepath, link=link) as (data_from, data_to):
        if collection_path in data_from.collections:
            data_to.collections = [collection_path]

    collection = data_to.collections[0] if data_to.collections else None
    if collection is None:
        node.scene_nodes_output = None
        return None

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


def _evaluate_transform(node, inputs):
    t_val = _get_exposed_value(node, "Translate", "translate", (0.0, 0.0, 0.0))
    r_val = _get_exposed_value(node, "Rotate", "rotate", (0.0, 0.0, 0.0))
    s_val = _get_exposed_value(node, "Scale", "scale", (1.0, 1.0, 1.0))

    t = Vector(t_val) if t_val is not None else None
    r = Vector(r_val) if r_val is not None else None
    s = Vector(s_val) if s_val is not None else None

    for coll in inputs:
        if coll is None:
            continue
        for obj in coll.objects:
            if t is not None:
                obj.location = Vector(obj.location) + t
            if r is not None:
                obj.rotation_euler = Vector(obj.rotation_euler) + r
            if s is not None:
                obj.scale = Vector(obj.scale) * s

    node.scene_nodes_output = inputs[0] if inputs else None
    return node.scene_nodes_output


def _evaluate_group(node, inputs, scene):
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


def _evaluate_light(node, _inputs, scene):
    ltype = _get_exposed_value(node, "Type", "light_type", "POINT") or "POINT"
    energy = _get_exposed_value(node, "Energy", "energy", 1.0)
    color = _get_exposed_value(node, "Color", "color", (1.0, 1.0, 1.0))

    if ltype is None:
        node.scene_nodes_output = scene.collection
        return scene.collection

    light_data = bpy.data.lights.new(name=node.name, type=ltype)
    light_data.energy = energy
    light_data.color = color

    light_obj = bpy.data.objects.new(node.name, light_data)
    scene.collection.objects.link(light_obj)

    node.scene_nodes_output = scene.collection
    return node.scene_nodes_output


def _evaluate_global_options(node, _inputs, scene):
    res_x = _get_exposed_value(node, "Resolution X", "res_x", 1920)
    res_y = _get_exposed_value(node, "Resolution Y", "res_y", 1080)
    samples = _get_exposed_value(node, "Samples", "samples", 128)
    camera_path = _get_exposed_value(node, "Camera Path", "camera_path", "")

    if res_x is not None:
        scene.render.resolution_x = res_x
    if res_y is not None:
        scene.render.resolution_y = res_y
    if samples is not None:
        scene.cycles.samples = samples if hasattr(scene, "cycles") else samples

    if camera_path and camera_path in bpy.data.objects:
        scene.camera = bpy.data.objects[camera_path]

    node.scene_nodes_output = scene.collection
    return node.scene_nodes_output


def _evaluate_outputs_stub(node, _inputs, scene):
    path = _get_exposed_value(node, "File Path", "filepath", "")
    fmt = _get_exposed_value(node, "Format", "file_format", "OPEN_EXR")

    if path is not None:
        scene.render.filepath = path
    if fmt is not None:
        scene.render.image_settings.file_format = fmt

    node.scene_nodes_output = scene.collection
    return node.scene_nodes_output


def _camel_to_snake(name):
    out = ""
    for c in name:
        if c.isupper():
            if out:
                out += "_"
            out += c.lower()
        else:
            out += c
    return out


def _evaluate_cycles_render(node, _inputs, scene):
    if not hasattr(scene, "cycles"):
        node.scene_nodes_output = scene.collection
        return scene.collection

    for attr, label, _socket, _cat in node.__class__._prop_defs:
        if not _is_exposed(node, attr):
            continue
        value = _get_exposed_value(node, label, attr)
        blender_attr = _camel_to_snake(attr)
        if hasattr(scene.cycles, blender_attr) and value is not None:
            try:
                setattr(scene.cycles, blender_attr, value)
            except Exception:
                pass

    node.scene_nodes_output = scene.collection
    return node.scene_nodes_output


def _evaluate_eevee_render(node, _inputs, scene):
    samples = _get_exposed_value(node, "Samples", "samples", 64)
    use_bloom = _get_exposed_value(node, "Bloom", "use_bloom", False)

    if hasattr(scene, "eevee"):
        if samples is not None:
            scene.eevee.taa_render_samples = samples
        if use_bloom is not None:
            scene.eevee.use_bloom = use_bloom

    node.scene_nodes_output = scene.collection
    return node.scene_nodes_output


def _evaluate_output_properties(node, _inputs, scene):
    path = _get_exposed_value(node, "File Path", "filepath", "")
    fmt = _get_exposed_value(node, "Format", "file_format", "OPEN_EXR")
    res_x = _get_exposed_value(node, "Resolution X", "res_x", 1920)
    res_y = _get_exposed_value(node, "Resolution Y", "res_y", 1080)

    if path is not None:
        scene.render.filepath = path
    if fmt is not None:
        scene.render.image_settings.file_format = fmt
    if res_x is not None:
        scene.render.resolution_x = res_x
    if res_y is not None:
        scene.render.resolution_y = res_y

    node.scene_nodes_output = scene.collection
    return node.scene_nodes_output


def _evaluate_input(node, _inputs, _scene):
    node.scene_nodes_output = None
    return None


def _evaluate_scene_output(node, inputs, scene):
    node.scene_nodes_output = inputs[0] if inputs else None
    return node.scene_nodes_output


def _evaluate_node(node, scene):
    inputs = _collect_input_scenes(node)
    ntype = node.bl_idname
    if ntype == "SceneInstanceNodeType":
        return _evaluate_scene_instance(node, inputs, scene)
    elif ntype == "TransformNodeType":
        return _evaluate_transform(node, inputs)
    elif ntype == "GroupNodeType":
        return _evaluate_group(node, inputs, scene)
    elif ntype == "LightNodeType":
        return _evaluate_light(node, inputs, scene)
    elif ntype == "GlobalOptionsNodeType":
        return _evaluate_global_options(node, inputs, scene)
    elif ntype == "OutputsStubNodeType":
        return _evaluate_outputs_stub(node, inputs, scene)
    elif ntype == "CyclesRenderNodeType":
        return _evaluate_cycles_render(node, inputs, scene)
    elif ntype == "EeveeRenderNodeType":
        return _evaluate_eevee_render(node, inputs, scene)
    elif ntype == "OutputPropertiesNodeType":
        return _evaluate_output_properties(node, inputs, scene)
    elif ntype == "SceneOutputNodeType":
        return _evaluate_scene_output(node, inputs, scene)
    elif ntype == "InputNodeType":
        return _evaluate_input(node, inputs, scene)
    else:
        print(f"[scene_nodes] unknown node type {ntype}")


def evaluate_scene_tree(tree):
    """Evaluate *tree* for every Scene Output node found."""
    if tree is None:
        raise ValueError("Scene node tree is None")

    outputs = [n for n in tree.nodes if n.bl_idname == "SceneOutputNodeType"]
    if not outputs:
        raise RuntimeError("No Scene Output node in the tree")

    names = []
    for out in outputs:
        name = _socket_value(out, "Name", getattr(out, "scene_name", "")) or "Scene"
        if name in names:
            raise RuntimeError(f"Duplicate scene name '{name}'")
        names.append(name)

    for out, name in zip(outputs, names):
        scene = _prepare_scene(name)
        order = _topological_sort([out])
        for node in order:
            node.scene_nodes_output = _evaluate_node(node, scene)

