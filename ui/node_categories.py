import nodeitems_utils
from nodeitems_utils import NodeCategory, NodeItem

class SceneNodeCategory(NodeCategory):
    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == 'SceneNodeTreeType'

node_categories = [
    SceneNodeCategory('SCENE_NODES', "Scene Nodes", items=[
        NodeItem("BlendInputNodeType"),
        NodeItem("AlembicImportNodeType"),
        NodeItem("TransformNodeType"),
        NodeItem("InputNodeType"),
        NodeItem("JoinStringNodeType"),
        NodeItem("SplitStringNodeType"),
        NodeItem("NameSwitchNodeType"),
        NodeItem("GroupNodeType"),
        NodeItem("LightNodeType"),
        NodeItem("GlobalOptionsNodeType"),
        NodeItem("RenderPassesNodeType"),
        NodeItem("CyclesPropertiesNodeType"),
        NodeItem("EeveePropertiesNodeType"),
        NodeItem("CyclesAttributesNodeType"),
        NodeItem("EeveeAttributesNodeType"),
        NodeItem("RenderEngineNodeType"),
        NodeItem("RenderNodeType"),
    ])
]