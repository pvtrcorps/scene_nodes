# Scene Nodes

Experimental node-based system for assembling Blender scenes.

## Installation

1. Clone or download this repository.
2. Zip the `scene_nodes` folder or use GitHub's *Download ZIP*.
3. In Blender open **Edit > Preferences > Add-ons** and click **Install...**.
4. Select the ZIP file and install.
5. Enable the add-on by checking **Scene Nodes** in the add-on list.

After enabling, you'll have a new **Scene Graph** tree type in the Node Editor.

## Usage

1. Open the Node Editor and change the tree type to **Scene Graph**.
2. Add nodes using the **Add** menu under **Scene Node**.
3. Connect them with the provided `Scene` sockets.

The tree can be evaluated via the **Sync to Scene** operator (accessible with **F3**) or from a Python script.
The operator uses the Scene Graph tree currently open in the Node Editor (or the
first one it finds in the file) so scenes don't need their own tree pointer.

## Quick Example

```python
import bpy
from scene_nodes.engine import evaluate_scene_tree

# Create a Scene Node Tree
tree = bpy.data.node_groups.new("Example", "SceneNodeTreeType")

# Add nodes
inst = tree.nodes.new("SceneInstanceNodeType")
out = tree.nodes.new("OutputsStubNodeType")

# Link instance to output
tree.links.new(inst.outputs[0], out.inputs[0])

# Evaluate the tree (applies changes to the scene)
evaluate_scene_tree(tree)
```
