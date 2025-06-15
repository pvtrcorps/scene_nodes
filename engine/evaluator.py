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


def _evaluate_scene_instance(node):
    filepath = getattr(node, "file_path", "")
    collection_path = getattr(node, "collection_path", "")
    as_override = getattr(node, "as_override", False)
    print(f"[scene_nodes] load instance {filepath}::{collection_path}, override={as_override}")


def _evaluate_transform(node):
    t = getattr(node, "translate", (0.0, 0.0, 0.0))
    r = getattr(node, "rotate", (0.0, 0.0, 0.0))
    s = getattr(node, "scale", (1.0, 1.0, 1.0))
    print(f"[scene_nodes] transform T={t} R={r} S={s}")


def _evaluate_group(_node):
    print("[scene_nodes] group scenes")


def _evaluate_light(node):
    ltype = getattr(node, "light_type", "POINT")
    energy = getattr(node, "energy", 1.0)
    print(f"[scene_nodes] create light {ltype} energy={energy}")


def _evaluate_global_options(node):
    res_x = getattr(node, "res_x", 1920)
    res_y = getattr(node, "res_y", 1080)
    samples = getattr(node, "samples", 128)
    print(f"[scene_nodes] global options {res_x}x{res_y} samples={samples}")


def _evaluate_outputs_stub(node):
    path = getattr(node, "filepath", "")
    fmt = getattr(node, "file_format", "OPEN_EXR")
    print(f"[scene_nodes] outputs {path} format={fmt}")


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
    else:
        print(f"[scene_nodes] unknown node type {ntype}")


def evaluate_scene_tree(tree):
    """Traverse *tree*, resolve dependencies and evaluate each node."""
    order = _topological_sort(tree.nodes)
    for node in order:
        if getattr(node, "scene_nodes_dirty", True):
            _evaluate_node(node)
            node.scene_nodes_dirty = False
