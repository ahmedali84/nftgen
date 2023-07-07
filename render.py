import bpy
import os
from . import functions as func

class RenderBatch(bpy.types.Operator):
    bl_idname = "nftgen.render"
    bl_label = "Render"
    bl_description = "Render tokens in range -from- to -To-"
    bl_options = {'UNDO'}

    _timer = None
    shots = None
    stop = None
    rendering = None
    path = ""

    @classmethod
    def poll(cls, context):
        return True

    def pre(self, scene, context=None):
        self.rendering = True
        
    def post(self, scene, context=None):
        self.shots.pop(0)
        self.rendering = False

    def cancelled(self, scene, context=None):
        self.stop = True

    def execute(self, context):
        scene = context.scene
        props = func.get_props()
        tokens = func.get_tokens()

        start = props.export_from
        end = props.export_to

        self.stop = False
        self.rendering = False
        self.shots = [tk for tk in tokens if tk.index >= start and tk.index <= end]

        # to be able to reset filepath later
        self.original_path = scene.render.filepath
        self.path = func.get_export_folder("render")

        bpy.app.handlers.render_pre.append(self.pre)
        bpy.app.handlers.render_post.append(self.post)
        bpy.app.handlers.render_cancel.append(self.cancelled)
        
        # The timer gets created and the modal handler
        # is added to the window manager
        self._timer = context.window_manager.event_timer_add(0.5, window=context.window)
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}
    
    def modal(self, context, event):
        scene = context.scene
        props = func.get_props()

        if event.type == 'TIMER':
            if any([not self.shots, self.stop]):
                # remove handlers and modal timer to clean everything
                bpy.app.handlers.render_pre.remove(self.pre)
                bpy.app.handlers.render_post.remove(self.post)
                bpy.app.handlers.render_cancel.remove(self.cancelled)
                context.window_manager.event_timer_remove(self._timer)

                # reset render filepath
                scene.render.filepath = self.original_path
                return {'FINISHED'}
            
            elif not self.rendering:
                # assign shot and start rendering
                scene = context.scene
                shot = self.shots[0]
                # scene.render.filepath = f"{self.path}_{str(shot.index)}"
                scene.render.filepath = f"{self.path}{str(shot.index)}"
                print(self.path)
                props.active_token_id = shot.index

                # start rendering
                bpy.ops.render.render("INVOKE_DEFAULT", write_still=True)
        return {'PASS_THROUGH'}