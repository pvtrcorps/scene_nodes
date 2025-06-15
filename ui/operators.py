import bpy

class NODE_OT_sync_to_scene(bpy.types.Operator):
    bl_idname = "scene_nodes.sync_to_scene"
    bl_label = "Sync to Scene"
    bl_description = "Sincroniza el node tree con la escena de Blender"

    def execute(self, context):
        from ..engine.evaluator import evaluate_scene_tree
        tree = context.scene.scene_node_tree
        evaluate_scene_tree(tree)
        return {'FINISHED'}