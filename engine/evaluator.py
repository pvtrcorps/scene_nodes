import bpy


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


def _evaluate_scene_instance(node):
    filepath = _socket_value(node, "File Path", getattr(node, "file_path", ""))
    collection_path = _socket_value(node, "Collection Path", getattr(node, "collection_path", ""))
    as_override = _socket_value(node, "As Override", getattr(node, "as_override", False))
    print(f"[scene_nodes] load instance {filepath}::{collection_path}, override={as_override}")


def _evaluate_transform(node):
    t = _socket_value(node, "Translate", getattr(node, "translate", (0.0, 0.0, 0.0)))
    r = _socket_value(node, "Rotate", getattr(node, "rotate", (0.0, 0.0, 0.0)))
    s = _socket_value(node, "Scale", getattr(node, "scale", (1.0, 1.0, 1.0)))
    print(f"[scene_nodes] transform T={t} R={r} S={s}")


def _evaluate_group(_node):
    print("[scene_nodes] group scenes")


def _evaluate_light(node):
    ltype = _socket_value(node, "Type", getattr(node, "light_type", "POINT"))
    energy = _socket_value(node, "Energy", getattr(node, "energy", 1.0))
    print(f"[scene_nodes] create light {ltype} energy={energy}")


def _evaluate_global_options(node):
    res_x = _socket_value(node, "Resolution X", getattr(node, "res_x", 1920))
    res_y = _socket_value(node, "Resolution Y", getattr(node, "res_y", 1080))
    samples = _socket_value(node, "Samples", getattr(node, "samples", 128))
    print(f"[scene_nodes] global options {res_x}x{res_y} samples={samples}")


def _evaluate_outputs_stub(node):
    path = _socket_value(node, "File Path", getattr(node, "filepath", ""))
    fmt = _socket_value(node, "Format", getattr(node, "file_format", "OPEN_EXR"))
    print(f"[scene_nodes] outputs {path} format={fmt}")


def _evaluate_input(node):
    val = _socket_value(node, "Value", None)
    print(f"[scene_nodes] input value={val}")


def _evaluate_node(node):
    ntype = node.bl_idname
    if ntype == "SceneInstanceNodeType":
        _evaluate_scene_instance(node)
    elif ntype == "TransformNodeType":
        _evaluate_transform(node)
    elif ntype == "GroupNodeType":
        _evaluate_group(node)
    elif ntype == "LightNodeType":
        _evaluate_light(node)
    elif ntype == "GlobalOptionsNodeType":
        _evaluate_global_options(node)
    elif ntype == "OutputsStubNodeType":
        _evaluate_outputs_stub(node)
    elif ntype == "InputNodeType":
        _evaluate_input(node)
    else:
        print(f"[scene_nodes] unknown node type {ntype}")


def evaluate_scene_tree(tree):
    """Traverse *tree* starting from its active node and evaluate."""
    if tree is None:
        raise ValueError("Scene node tree is None")

    root = getattr(tree.nodes, "active", None)
    if root is not None:
        order = _topological_sort([root])
    else:
        order = _topological_sort(tree.nodes)
    for node in order:
        if getattr(node, "scene_nodes_dirty", True):
            _evaluate_node(node)
            node.scene_nodes_dirty = False
