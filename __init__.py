import bpy



locations = {}
rotations = {}

class SAVE_TRANSFORM(bpy.types.Operator):
    bl_idname = "object.save_transform"
    bl_label = "Save Objects Transforms"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        for ob in context.selected_objects:
            locations[ob.name] = ob.location.copy()
            rotations[ob.name] = ob.rotation_euler.copy()
            
            
        return {'FINISHED'}
    
class LOAD_TRANSFORM(bpy.types.Operator):
    bl_idname = "object.load_transform"
    bl_label = "Load Objects Transforms"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        for ob in context.selected_objects:
            if ob.name in locations:
                ob.location = locations[ob.name]
            if ob.name in rotations:
                ob.rotation_euler = rotations[ob.name]
                
                
        return {'FINISHED'}


class CLEAR_TRANSFORM(bpy.types.Operator):
    bl_idname = "object.clear_transform"
    bl_label = "Clear Saved Transforms"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        locations.clear() 
        rotations.clear()
        return {'FINISHED'}

class VIEW3D_OT_PANEL_TRANSFORM_SAVER(bpy.types.Panel):
    bl_label = "Transform Saver"
    bl_idname = "OBJECT_Transform_SAVER"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "TransfromSaver"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.label(text="Status: {} transforms saved".format(len(locations)))
        row = layout.row()
        row.operator(SAVE_TRANSFORM.bl_idname)
        row = layout.row()
        row.operator(LOAD_TRANSFORM.bl_idname)
        row = layout.row()
        row.operator(CLEAR_TRANSFORM.bl_idname)


classes = (
    SAVE_TRANSFORM,
    LOAD_TRANSFORM,
    CLEAR_TRANSFORM,
    VIEW3D_OT_PANEL_TRANSFORM_SAVER

)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
