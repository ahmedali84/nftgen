import bpy
import os
from . import functions as func
from .render import RenderBatch

class Dummy(bpy.types.Operator):
    bl_idname = "nftgen.dummy"
    bl_label = ""
    bl_description = ""
    bl_options = {'UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        self.report({'INFO'}, "Dummy")
        return {'FINISHED'}

class AddTrait(bpy.types.Operator):
    bl_idname = "nftgen.add_trait"
    bl_label = "Add"
    bl_description = "Add new trait"
    bl_options = {'UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        traits = func.get_traits()
        traits.add()
        return {'FINISHED'}

class RemoveTrait(bpy.types.Operator):
    bl_idname = "nftgen.remove_trait"
    bl_label = "Remove"
    bl_description = "Remove active trait"
    bl_options = {'UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        props = func.get_props()
        traits = func.get_traits()

        active_trait_id = props.active_trait_id
        func.remove_trait_values(active_trait_id)
        traits.remove(active_trait_id)

        active_trait_id = max(0, active_trait_id - 1)
        return {'FINISHED'}

class AddTraitValue(bpy.types.Operator):
    bl_idname = "nftgen.add_trait_value"
    bl_label = "Add"
    bl_description = "Add new value for active trait"
    bl_options = {'UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        props = func.get_props()
        trait_values = func.get_traits_values()
        active_trait_id = props.active_trait_id

        new_trait_value = trait_values.add()
        new_trait_value.name = func.generate_random_id()
        new_trait_value.trait_id = active_trait_id
        return {'FINISHED'}

class RemoveTraitValue(bpy.types.Operator):
    bl_idname = "nftgen.remove_trait_value"
    bl_label = "Remove"
    bl_description = "Remove active trait value"
    bl_options = {'UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        props = func.get_props()
        trait_values = func.get_traits_values()
        active_trait_value_id = props.active_trait_value_id

        trait_values.remove(active_trait_value_id)

        active_trait_value_id = max(0, active_trait_value_id - 1)
        return {'FINISHED'}
    
class ClearTraitValues(bpy.types.Operator):
    bl_idname = "nftgen.clear_trait_value"
    bl_label = "Clear"
    bl_description = "Clear values for active trait"
    bl_options = {'UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        props = func.get_props()
        active_trait_id = props.active_trait_id
        # trait_values = func.get_traits_values()

        func.remove_trait_values(active_trait_id)

        # props.active_trait_value_id = 0


        return {'FINISHED'}

classes = (
    Dummy, 
    AddTrait, 
    RemoveTrait, 
    AddTraitValue, 
    RemoveTraitValue, 
    ClearTraitValues, 
    RenderBatch, 
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)