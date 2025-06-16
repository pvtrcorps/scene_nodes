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

- Render Properties node now adjusts its parameters depending on the selected render engine.
- Scene and Output nodes expose additional settings such as frame range, FPS and color mode.
- Added **Join String** and **Split String** nodes for basic text manipulation.
- New **Cycles Attributes** node lets you edit Cycles visibility flags with optional filtering.

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
out = tree.nodes.new("OutputPropertiesNodeType")

# Link instance to output
tree.links.new(inst.outputs[0], out.inputs[0])

# Evaluate the tree (applies changes to the scene)
evaluate_scene_tree(tree)
```

Nodes that modify objects, such as **Transform** and **Cycles Attributes**, support
an optional *Filter* property. The expression can include wildcards to match
object names or collection paths, allowing selective updates.

## Migration

Global Options and Render Outputs nodes have been replaced by **Scene Properties**, **Render Properties** and **Output Properties**. Update existing trees by inserting the new nodes in place of the old ones.
