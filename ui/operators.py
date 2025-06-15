import bpy

class NODE_OT_sync_to_scene(bpy.types.Operator):
    bl_idname = "scene_nodes.sync_to_scene"
    bl_label = "Sync to Scene"
    bl_description = "Sincroniza el node tree con la escena de Blender"

    def execute(self, context):
        from ..engine.evaluator import evaluate_scene_tree

        tree = None

        if context.area and context.area.type == 'NODE_EDITOR':
            space = context.space_data
            if space and space.tree_type == 'SceneNodeTreeType':
                tree = space.node_tree

        if tree is None:
            for nt in bpy.data.node_groups:
                if nt.bl_idname == 'SceneNodeTreeType':
                    tree = nt
                    break

        if tree is None:
            self.report({'ERROR'}, "No Scene Node Tree found")
            return {'CANCELLED'}

        evaluate_scene_tree(tree)
        return {'FINISHED'}
