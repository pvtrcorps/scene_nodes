# Scene Nodes

Experimental node-based system for assembling Blender scenes.

## Installation

1. Clone or download this repository.
2. Zip the `scene_nodes` folder or use GitHub's *Download ZIP*.
3. In Blender open **Edit > Preferences > Add-ons** and click **Install...**.
4. Select the ZIP file and install.
5. Enable the add-on by checking **Scene Nodes** in the add-on list.

After enabling, you'll have a new **Scene Graph** tree type in the Node Editor.

## New in this version

- New **Cycles Properties** and **Eevee Properties** nodes combine scene, render
  and output settings for each engine.
- Added **Join String** and **Split String** nodes for basic text manipulation.
- New **Cycles Attributes** node lets you edit Cycles visibility flags with optional filtering.
- Added **Alembic Import** node to load `.abc` files directly.
- The **Render Pass Wedge** operator now creates view layers on the evaluated
  scene and restores the original scene and view layer after rendering.

## Usage

1. Open the Node Editor and change the tree type to **Scene Graph**.
2. Add nodes using the **Add** menu under **Scene Node**.
3. Connect them with the provided `Scene` sockets.

The tree can be evaluated via the **Sync to Scene** operator (accessible with **F3**) or from a Python script.
You can also find shortcuts to this and other operators in the **Scene Nodes**
tab of the side panel (**N**).
The operator uses the Scene Graph tree currently open in the Node Editor (or the
first one it finds in the file) so scenes don't need their own tree pointer.
When present, **Render** nodes in the tree produce output images during evaluation.

## Quick Example

```python
import bpy
from scene_nodes.engine import evaluate_scene_tree

# Create a Scene Node Tree
tree = bpy.data.node_groups.new("Example", "SceneNodeTreeType")


# Add nodes
inst = tree.nodes.new("BlendInputNodeType")
props = tree.nodes.new("EeveePropertiesNodeType")
render = tree.nodes.new("RenderNodeType")

# Link instance to properties and then to render
tree.links.new(inst.outputs[0], props.inputs[0])
tree.links.new(props.outputs[0], render.inputs[0])

# Evaluate the tree (applies changes to the scene)
evaluate_scene_tree(tree)

# You can also specify a render pass name when evaluating without
# a Render node
# evaluate_scene_tree(tree, render_pass="MyPass")
```

Nodes that modify or load objects, such as **Transform**, **Cycles Attributes**
and **Blend Input**, support an optional *Filter* property. The expression can
include wildcards to match object names or collection paths, allowing selective
updates.

## Migration

Global Options and Render Outputs nodes have been replaced by **Cycles Properties** and **Eevee Properties**.

## License

This project is licensed under the GNU General Public License v3.0. See [LICENSE](LICENSE) for more information.
