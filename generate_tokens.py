import bpy
from . import functions as func
import json

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
    
classes = (
    GenerateTokens, 
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)