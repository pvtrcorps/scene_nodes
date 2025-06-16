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


class RENDER_OT_render_pass_wedge(bpy.types.Operator):
    bl_idname = "scene_nodes.render_pass_wedge"
    bl_label = "Render Pass Wedge"
    bl_description = "Render all passes defined in the Render Passes node"

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

        passes_node = None
        for node in tree.nodes:
            if node.bl_idname == 'RenderPassesNodeType':
                passes_node = node
                break

        if passes_node is None or not passes_node.passes:
            self.report({'ERROR'}, "No Render Passes node found")
            return {'CANCELLED'}

        for item in passes_node.passes:
            # Ensure a view layer exists for this pass
            layer = context.scene.view_layers.get(item.name)
            if layer is None:
                layer = context.scene.view_layers.new(name=item.name)
            context.window.view_layer = layer

            setattr(context, "render_pass", item.name)
            evaluate_scene_tree(tree)
            bpy.ops.render.render(write_still=True)

        return {'FINISHED'}
