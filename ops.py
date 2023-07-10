import bpy
import os
import json
from . import functions as func
from .render import RenderBatch
from .metadata import ExportMetadata

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
        props = func.get_props()
        traits = func.get_traits()

        new_trait = traits.add()
        new_trait.name = func.generate_random_id()
        idx = traits.find(new_trait.name)
        print(idx)
        props.active_trait_id = idx

        props.traits_updated = func.traits_updated()
        return {'FINISHED'}

class RemoveTrait(bpy.types.Operator):
    bl_idname = "nftgen.remove_trait"
    bl_label = "Remove"
    bl_description = "Remove active trait"
    bl_options = {'UNDO'}

    @classmethod
    def poll(cls, context):
        traits = func.get_traits()
        return bool(traits)

    def execute(self, context):
        props = func.get_props()
        traits = func.get_traits()

        active_trait_index = props.active_trait_id
        active_trait = traits[active_trait_index]
        func.remove_trait_values(active_trait)
        traits.remove(active_trait_index)

        props.active_trait_id = max(0, active_trait_index - 1)
        # print(active_trait_index)
        props.traits_updated = func.traits_updated()
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
        traits = func.get_traits()
        trait_values = func.get_traits_values()
        active_trait_index = props.active_trait_id

        new_trait_value = trait_values.add()
        new_trait_value.name = func.generate_random_id()
        new_trait_value.trait_id = traits[active_trait_index].name

        trait_values = [tv for tv in trait_values]
        props.active_trait_value_id = trait_values.index(new_trait_value)
        return {'FINISHED'}

class RemoveTraitValue(bpy.types.Operator):
    bl_idname = "nftgen.remove_trait_value"
    bl_label = "Remove"
    bl_description = "Remove active trait value"
    bl_options = {'UNDO'}

    @classmethod
    def poll(cls, context):
        props = func.get_props()
        active_trait_index = props.active_trait_id
        traits = func.get_traits()
        
        try:
            active_trait = traits[active_trait_index]
            traits_values = func.get_traits_values()

        except IndexError:
            return False
        
        return bool([tv for tv in traits_values if tv.trait_id == active_trait.name])

    def execute(self, context):
        props = func.get_props()
        traits_values = func.get_traits_values()
        active_trait_value_id = props.active_trait_value_id
        active_trait_value = traits_values[active_trait_value_id]
        candidate_tv = func.get_candidate_tv(active_trait_value)
        # print(f"Next tv= {candidate_tv.metadata_name}")

        traits_values.remove(active_trait_value_id)
        
        if candidate_tv:
            traits_values = func.get_traits_values()
            props.active_trait_value_id = traits_values.find(candidate_tv)
        else:
            props.active_trait_value_id = 0
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
        active_trait_index = props.active_trait_id
        traits = func.get_traits()

        func.remove_trait_values(traits[active_trait_index].name)

        # props.active_trait_value_id = 0
        return {'FINISHED'}

class ClearTokens(bpy.types.Operator):
    bl_idname = "nftgen.clear_tokens"
    bl_label = "Clear Tokens"
    bl_description = "Clear all generated tokens"
    bl_options = {'UNDO'}

    @classmethod
    def poll(cls, context):
        tokens = func.get_tokens()
        return bool(tokens)

    def execute(self, context):
        tokens = func.get_tokens()
        tokens.clear()

        # clear active token collection props
        active_token_props = func.get_active_token_props()
        active_token_props.clear()

        # go back to the generate panel
        props = func.get_props()
        props.mode = '0'
        return {'FINISHED'}

class AddRule(bpy.types.Operator):
    bl_idname = "nftgen.add_rule"
    bl_label = "Add"
    bl_description = "Add new rule"
    bl_options = {'UNDO'}

    @classmethod
    def poll(cls, context):
        traits = func.get_traits()
        return bool(traits)

    def execute(self, context):
        props = func.get_props()
        rules = func.get_rules()

        new_rule = rules.add()
        new_rule.name = func.generate_random_id()
        idx = rules.find(new_rule.name)
        props.active_rule_id = idx
        return {'FINISHED'}

class RemoveRule(bpy.types.Operator):
    bl_idname = "nftgen.remove_rule"
    bl_label = "Remove"
    bl_description = "Remove selected rule"
    bl_options = {'UNDO'}

    @classmethod
    def poll(cls, context):
        rules = func.get_rules()
        return bool(rules)

    def execute(self, context):
        props = func.get_props()
        rules = func.get_rules()

        idx = props.active_rule_id
        rules.remove(idx)

        props.active_rule_id = max(0, idx - 1)
        return {'FINISHED'}

class UpRule(bpy.types.Operator):
    bl_idname = "nftgen.up_rule"
    bl_label = "Up"
    bl_description = "Move selected rule up"
    bl_options = {'UNDO'}

    @classmethod
    def poll(cls, context):
        rules = func.get_rules()
        props = func.get_props()
        
        return bool(rules) and props.active_rule_id > 0

    def execute(self, context):
        props = func.get_props()
        rules = func.get_rules()

        rules.move(props.active_rule_id, props.active_rule_id - 1)
        props.active_rule_id -= 1
        return {'FINISHED'}
    
class DownRule(bpy.types.Operator):
    bl_idname = "nftgen.down_rule"
    bl_label = "Down"
    bl_description = "Move selected rule down"
    bl_options = {'UNDO'}

    @classmethod
    def poll(cls, context):
        rules = func.get_rules()
        props = func.get_props()
        
        return bool(rules) and props.active_rule_id < len(rules) - 1

    def execute(self, context):
        props = func.get_props()
        rules = func.get_rules()

        rules.move(props.active_rule_id, props.active_rule_id + 1)
        props.active_rule_id += 1
        return {'FINISHED'}

class OpenOutputDir(bpy.types.Operator):
    bl_idname = "nftgen.open_output_dir"
    bl_label = "Open Output Folder"
    bl_description = "Open Output Folder in File Explorer"
    bl_options = {'UNDO'}

    @classmethod
    def poll(cls, context):
        # check if output folder exists
        props = func.get_props()
        output_dir = bpy.path.abspath(props.output_dir)
        
        return os.path.exists(output_dir)

    def execute(self, context):
        props = func.get_props()
        output_dir = bpy.path.abspath(props.output_dir)

        os.startfile(output_dir)
        return {'FINISHED'}

class UpTrait(bpy.types.Operator):
    bl_idname = "nftgen.up_trait"
    bl_label = "Up"
    bl_description = "Move selected trait up"
    bl_options = {'UNDO'}

    @classmethod
    def poll(cls, context):
        props = func.get_props()
        traits = func.get_traits()
        
        return bool(traits) and props.active_trait_id > 0

    def execute(self, context):
        props = func.get_props()
        traits = func.get_traits()

        traits.move(props.active_trait_id, props.active_trait_id - 1)
        props.active_trait_id -= 1

        # set prop.traits_order_updated
        # to add warning in export panel in case traits order has been changed
        # after tokens were generated
        props.traits_updated = func.traits_updated()
        return {'FINISHED'}
    
class DownTrait(bpy.types.Operator):
    bl_idname = "nftgen.down_trait"
    bl_label = "Down"
    bl_description = "Move selected trait down"
    bl_options = {'UNDO'}

    @classmethod
    def poll(cls, context):
        traits = func.get_traits()
        props = func.get_props()
        
        return bool(traits) and props.active_trait_id < len(traits) - 1

    def execute(self, context):
        props = func.get_props()
        traits = func.get_traits()

        traits.move(props.active_trait_id, props.active_trait_id + 1)
        props.active_trait_id += 1

        props.traits_updated = func.traits_updated()
        return {'FINISHED'}

classes = (
    Dummy, 
    AddTrait, 
    RemoveTrait, 
    AddTraitValue, 
    RemoveTraitValue, 
    ClearTraitValues, 
    RenderBatch, 
    ExportMetadata, 
    ClearTokens, 
    AddRule, 
    RemoveRule, 
    UpRule, 
    DownRule, 
    OpenOutputDir, 
    UpTrait, 
    DownTrait
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)