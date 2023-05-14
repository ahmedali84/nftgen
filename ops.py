import bpy
import os
import json
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
        props = func.get_props()
        traits = func.get_traits()

        new_trait = traits.add()
        new_trait.name = func.generate_random_id()
        idx = traits.find(new_trait.name)
        print(idx)
        props.active_trait_id = idx
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

        props.active_trait_id = max(0, active_trait_id - 1)
        print(active_trait_id)
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
        active_trait_id = props.active_trait_id

        new_trait_value = trait_values.add()
        new_trait_value.name = func.generate_random_id()
        new_trait_value.trait_id = traits[active_trait_id].name
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
        traits = func.get_traits()

        func.remove_trait_values(traits[active_trait_id].name)

        # props.active_trait_value_id = 0
        return {'FINISHED'}
    
class GenerateTokens(bpy.types.Operator):
    bl_idname = "nftgen.generate_tokens"
    bl_label = "Generate Tokens"
    bl_description = """Randomly generate tokens according to rarities assigned to each trait"""
    bl_options = {'UNDO'}

    @classmethod
    def poll(cls, context):
        props = func.get_props()
        max_unique_tokens = func.max_unique_tokens()
        return props.tokens_count <= max_unique_tokens

    def execute(self, context):
        props = func.get_props()
        traits = func.get_traits()
        tokens = func.get_tokens()

        # clear existing tokens list
        tokens.clear()
        
        # randomly generate new unique tokens
        token_set = set()
        while len(token_set) < props.tokens_count:
            token_data = {}
            for tt in traits:
                choice = func.pick_random_choice(tt)
                token_data[tt.name] = choice

            # implement rules here
            token_data = func.apply_rules(token_data)
            if token_data:
                token_data = json.dumps(token_data)
                token_set.add(token_data)

        for element in token_set:
            new_token = tokens.add()
            new_token.attributes = element

        # navigate to the first token in the stack
        props.active_token_id = 0
        props.mode = '1'
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

classes = (
    Dummy, 
    AddTrait, 
    RemoveTrait, 
    AddTraitValue, 
    RemoveTraitValue, 
    ClearTraitValues, 
    RenderBatch, 
    GenerateTokens, 
    ClearTokens, 
    AddRule, 
    RemoveRule, 
    UpRule, 
    DownRule
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)