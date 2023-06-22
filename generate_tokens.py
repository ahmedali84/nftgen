import bpy
from . import functions as func
import json
from time import sleep

class GenerateTokens(bpy.types.Operator):
    bl_idname = "nftgen.generate_tokens"
    bl_label = "Generate Tokens"
    bl_description = """Randomly generate tokens according to rarities assigned to each trait"""
    bl_options = {'UNDO'}

    timer = None
    tokens = []
    tokens_count = 0
    progress = 0
    

    @classmethod
    def poll(cls, context):
        props = func.get_props()
        max_unique_tokens = func.max_unique_tokens()
        return props.tokens_count <= max_unique_tokens

    def execute(self, context):
        print("execute")
        props = func.get_props()
        tokens = func.get_tokens()

        tokens.clear()

        self.tokens_count = props.tokens_count
        self.progress = 0
        props.generate_progress = 0

        self.report({'INFO'}, message=f"Generating Tokens")

        # prepare the modal stuff
        self.timer = context.window_manager.event_timer_add(0.01, window=context.window)
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}
    
    def modal(self, context, event):
        if len(self.tokens) == self.tokens_count:
            tokens = func.get_tokens()
            props = func.get_props()

            # update the tokens global prop
            for element in self.tokens:
                new_token = tokens.add()
                new_token.attributes = element

            # navigate to the first token in the stack
            # and switch to edit tab
            props.active_token_id = 0
            props.mode = '1'

            self.report({'INFO'}, message=f"Tokens Generated")

            return {'FINISHED'} 

        # if event.type == 'TIMER':
        #     self.report({'INFO'}, message=f"Generated {self.progress}%")

        if event.type == 'ESC':
            print("Cancel")
            self.report({'WARNING'}, message=f"Canecelled")
            context.window_manager.event_timer_remove(self.timer)
            return {'CANCELLED'}
        

        # generate the tokens here
        print(f"{len(self.tokens)}")
        traits = func.get_traits()
        token_set = set(self.tokens)

        token_data = {}
        token_data = func.generate_token_data(traits)
        token_data = func.apply_rules(token_data)

        if token_data:
            token_data = json.dumps(token_data)
            token_set.add(token_data)
            self.tokens = list(token_set)
            progress = int(
                len(self.tokens) / self.tokens_count * 100
            )

            if progress > self.progress:
                self.report({'INFO'}, message=f"Generated {progress}%")
                self.progress = progress

        return {'PASS_THROUGH'}



    # def execute(self, context):
    #     props = func.get_props()
    #     traits = func.get_traits()
    #     tokens = func.get_tokens()

    #     # clear existing tokens list
    #     tokens.clear()
        
    #     # randomly generate new unique tokens
    #     token_set = set()

    #     token_data = {}
    #     token_data = func.generate_token_data(traits)
    #     token_data = func.apply_rules(token_data)

    #     if token_data:
    #         token_data = json.dumps(token_data)
    #         token_set.add(token_data)

    #     for element in token_set:
    #         new_token = tokens.add()
    #         new_token.attributes = element

    #     # navigate to the first token in the stack
    #     props.active_token_id = 0
    #     props.mode = '1'
    #     return {'FINISHED'}
    
classes = (
    GenerateTokens, 
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)