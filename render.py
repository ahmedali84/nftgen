import bpy
import os
from . import functions as func

class RenderBatch(bpy.types.Operator):
    bl_idname = "hbb.render_batch"
    bl_label = "Render Batch"
    bl_description = "Render a batch of HBBs in the collection starting with -from- to -To-"
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
        ob = func.get_object()
        hbbs = func.get_hbbs(ob)
        props = func.get_props()

        start = props.render_from
        end = min(props.render_to, len(hbbs))

        self.stop = False
        self.rendering = False
        self.shots = [(hbb.day, hbb.edition) for hbb in hbbs]
        # print(self.shots)

        # reset render path
        self.path = scene.render.filepath
        
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
        ob = func.get_object()
        hbbs = func.get_hbbs(ob)
        props = func.get_props()

        if event.type == 'TIMER':
            if any([not self.shots, self.stop]):
                # remove handlers and modal timer to clean everything
                bpy.app.handlers.render_pre.remove(self.pre)
                bpy.app.handlers.render_post.remove(self.post)
                bpy.app.handlers.render_cancel.remove(self.cancelled)
                context.window_manager.event_timer_remove(self._timer)

                # reset render filepath
                scene.render.filepath = self.path
                return {'FINISHED'}
            
            elif not self.rendering:
                # assign shot and start rendering
                scene = context.scene
                shot = self.shots[0]
                print(shot)
                # scene.render.filepath = f"{self.path}_{str(shot[1]).zfill(2)}_{str(shot[0]).zfill(5)}"
                # scene.render.filepath = f"{self.path}_{func.generate_hbb_name(shot[0], shot[1])}"
                scene.render.filepath = os.path.join(self.path, func.generate_hbb_name(shot[0], shot[1]))
                props.current_hbb_index = func.get_hbb_index(shot[0], shot[1])
                # props.current_day = shot[1]

                # start rendering
                bpy.ops.render.render("INVOKE_DEFAULT", write_still=True)

                

        return {'PASS_THROUGH'}