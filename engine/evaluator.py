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
    filepath = _socket_value(node, "File Path", getattr(node, "file_path", ""))
    collection_path = _socket_value(node, "Collection Path", getattr(node, "collection_path", ""))
    load_mode = _socket_value(node, "Load Mode", getattr(node, "load_mode", "APPEND"))
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

    if load_mode != "INSTANCE":
        scene.collection.children.link(collection)

    if load_mode == "OVERRIDE":
        collection = collection.override_create(scene.collection)
    elif load_mode == "INSTANCE":
        # Create a new wrapper collection with a collection instance object
        wrapper = bpy.data.collections.new(name=f"{collection.name}_instance")
        scene.collection.children.link(wrapper)
        inst_obj = bpy.data.objects.new(name=f"{collection.name}_inst", object_data=None)
        inst_obj.instance_type = 'COLLECTION'
        inst_obj.instance_collection = collection
        wrapper.objects.link(inst_obj)
        collection = wrapper

    node.scene_nodes_output = collection
    return collection


def _evaluate_transform(node, inputs):
    t = Vector(_socket_value(node, "Translate", getattr(node, "translate", (0.0, 0.0, 0.0))))
    r = Vector(_socket_value(node, "Rotate", getattr(node, "rotate", (0.0, 0.0, 0.0))))
    s = Vector(_socket_value(node, "Scale", getattr(node, "scale", (1.0, 1.0, 1.0))))

    for coll in inputs:
        if coll is None:
            continue
        for obj in coll.objects:
            obj.location = Vector(obj.location) + t
            obj.rotation_euler = Vector(obj.rotation_euler) + r
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
    ltype = _socket_value(node, "Type", getattr(node, "light_type", "POINT"))
    energy = _socket_value(node, "Energy", getattr(node, "energy", 1.0))
    color = _socket_value(node, "Color", getattr(node, "color", (1.0, 1.0, 1.0)))

    light_data = bpy.data.lights.new(name=node.name, type=ltype)
    light_data.energy = energy
    light_data.color = color

    light_obj = bpy.data.objects.new(node.name, light_data)
    scene.collection.objects.link(light_obj)

    node.scene_nodes_output = scene.collection
    return node.scene_nodes_output


def _evaluate_global_options(node, _inputs, scene):
    res_x = _socket_value(node, "Resolution X", getattr(node, "res_x", 1920))
    res_y = _socket_value(node, "Resolution Y", getattr(node, "res_y", 1080))
    samples = _socket_value(node, "Samples", getattr(node, "samples", 128))
    camera_path = _socket_value(node, "Camera Path", getattr(node, "camera_path", ""))

    scene.render.resolution_x = res_x
    scene.render.resolution_y = res_y
    scene.cycles.samples = samples if hasattr(scene, "cycles") else samples

    if camera_path in bpy.data.objects:
        scene.camera = bpy.data.objects[camera_path]

    node.scene_nodes_output = scene.collection
    return node.scene_nodes_output


def _evaluate_outputs_stub(node, _inputs, scene):
    path = _socket_value(node, "File Path", getattr(node, "filepath", ""))
    fmt = _socket_value(node, "Format", getattr(node, "file_format", "OPEN_EXR"))

    scene.render.filepath = path
    scene.render.image_settings.file_format = fmt

    node.scene_nodes_output = scene.collection
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
    else:
        print(f"[scene_nodes] unknown node type {ntype}")


def evaluate_scene_tree(tree):
    """Traverse *tree* starting from its active node and evaluate."""
    if tree is None:
        raise ValueError("Scene node tree is None")

    scene = _prepare_scene()

    root = getattr(tree.nodes, "active", None)
    if root is not None:
        order = _topological_sort([root])
    else:
        order = _topological_sort(tree.nodes)
    for node in order:
        if getattr(node, "scene_nodes_dirty", True):
            node.scene_nodes_output = _evaluate_node(node, scene)
            node.scene_nodes_dirty = False
