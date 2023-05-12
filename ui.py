import bpy
import json
from . import functions as func

class ModePanel(bpy.types.Panel):
    bl_label = "NFT Generator"
    bl_idname = "OBJECT_PT_mode"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category= 'NFT Generator'

    
    def draw(self, context):
        props = func.get_props()
        layout = self.layout

        row = layout.row(align= True)
        row.prop_enum(props, "mode", "0")
        row.prop_enum(props, "mode", "1")
        row.prop_enum(props, "mode", "2")

class NavigatePanel(bpy.types.Panel):
    bl_label = "Navigate"
    bl_idname = "OBJECT_PT_navigate"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category= 'NFT Generator'

    @classmethod
    def poll(cls, context):
        props = func.get_props()
        tokens = func.get_tokens()
        return props.mode == '1'  and tokens

    def draw(self, context):
        props = func.get_props()
        layout = self.layout 
        mode = props.mode
        tokens = func.get_tokens()
        
        col = layout.column(align=False)
        if tokens:
            col.prop(props, "active_token_id")
            col.scale_y = 2

        col = layout.column(align=False)
        row = col.row(align=False)
        if tokens:
            row.label(text=f"{len(tokens)} Tokens")
            row.operator("nftgen.clear_tokens", text="", icon='TRASH')

        col = layout.column(align=True)
        row = col.row(align=True)
        # row.operator("nftgen.dummy", text="First", icon="REW")
        # row.operator("nftgen.dummy", text="Last", icon= "FF")

class TokenDetailsPanel(bpy.types.Panel):
    bl_label = "Active Token Details"
    bl_idname = "OBJECT_PT_tkndetails"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category= 'NFT Generator'
    bl_parent_id= 'OBJECT_PT_navigate'

    @classmethod
    def poll(cls, context):
        props = func.get_props()
        tokens = func.get_tokens()
        return props.mode == '1'  and tokens

    def draw(self, context):
        props = func.get_props()
        layout = self.layout
        col = layout.column(align= True)
        mode = props.mode
        tokens = func.get_tokens()

        # show the active token data
        if tokens:
            active_token = tokens[props.active_token_id]
            active_token_attr = json.loads(active_token.attributes).items()

            traits = func.get_traits()
            traits_values = func.get_traits_values()

            for attr in active_token_attr:
                row = col.row(align=False)
                row.label(text=f"{traits[attr[0]].metadata_name} :")
                row.label(text=f"{traits_values[attr[1]].metadata_name}")


class TRAITS_UL_items(bpy.types.UIList):
    """The Slots UI list"""
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        row = layout.row()
        row.prop(item, "enable", text= "")
        row.prop(item, "metadata_name", text= "", emboss=False)
        row.prop(item, "value_type", text= "")
        

class TRAITVALUES_UL_items(bpy.types.UIList):
    """The Slots UI list"""
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        row = layout.row()
        row.prop(item, "enable", text= "")
        row.prop(item, "metadata_name", text= "", emboss=False)
        row.prop(item, "rarity", text="")
        
        traits = func.get_traits()
        trait = traits[item.trait_id]

        # change the displayed propery depending on
        # the trait this value is instanciated from
        VALUE_TYPES = {
            '0': "object_", 
            '1': "collection_"
        }
        row.prop(item, VALUE_TYPES[trait.value_type], text="")

    def filter_items(self, context, data, propname):
        """Filter and order items in the list."""

        # We initialize filtered and ordered as empty lists. Notice that 
        # if all sorting and filtering is disabled, we will return
        # these empty. 

        filtered = []
        ordered = []
        items = getattr(data, propname)

        # Filter

        # Initialize with all items visible
        filtered = [self.bitflag_filter_item] * len(items)

        props = func.get_props()
        active_trait_id = props.active_trait_id
        traits = func.get_traits()


        for i, item in enumerate(items):
            if item.trait_id != traits[active_trait_id].name:
                filtered[i] &= ~self.bitflag_filter_item

        
        return filtered, ordered
        

class TraitsPanel(bpy.types.Panel):
    bl_label = "Traits"
    bl_idname = "OBJECT_PT_traits"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category= 'NFT Generator'

    @classmethod
    def poll(cls, context):
        props = func.get_props()
        return props.mode == "0"

    def draw(self, context):
        scene = context.scene
        props = func.get_props()
        layout = self.layout

        col = layout.column()
        col.label(text= "Traits:")
        row = col.row()
        row.template_list(
            "TRAITS_UL_items", "", scene, "traits", props, "active_trait_id"
        )
        sub = row.column(align= True)
        sub.operator("nftgen.add_trait", icon='ADD', text="")
        sub.operator("nftgen.remove_trait", icon='REMOVE', text="")

        col.label(text= "Trait Values:")
        row = col.row()
        row.template_list(
            "TRAITVALUES_UL_items", "", scene, "traits_values", props, "active_trait_value_id"
        )
        sub = row.column(align= True)
        sub.operator("nftgen.add_trait_value", icon='ADD', text="")
        sub.operator("nftgen.remove_trait_value", icon='REMOVE', text="")
        sub.separator()
        sub.operator("nftgen.clear_trait_value", icon="TRASH", text="")

        col.label(text=f"Max unique tokens= {func.max_unique_tokens()}")

class GeneratePanel(bpy.types.Panel):
    bl_label = "Generate"
    bl_idname = "OBJECT_PT_generate"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category= 'NFT Generator'

    @classmethod
    def poll(cls, context):
        props = func.get_props()
        return props.mode == "0"

    def draw(self, context):
        scene = context.scene
        props = func.get_props()
        layout = self.layout
        col = layout.column()
        col.prop(props, "tokens_count")
        col.operator("nftgen.generate_tokens", text="Generate", icon="FILE_REFRESH")

class RulesPanel(bpy.types.Panel):
    bl_label = "Rules"
    bl_idname = "OBJECT_PT_rules"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'NFT Generator'
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        props = func.get_props()
        return props.mode == "0"

    def draw(self, context):
        scene = context.scene
        props = func.get_props()
        layout = self.layout
        col = layout.column()

class RenderPanel(bpy.types.Panel):
    bl_label = "Render"
    bl_idname = "OBJECT_PT_render"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'NFT Generator'

    @classmethod
    def poll(cls, context):
        props = func.get_props()
        tokens = func.get_tokens()
        return props.mode == "2" and tokens

    def draw(self, context):
        scene = context.scene
        props = func.get_props()
        layout = self.layout
        col = layout.column(align=True)

        col.prop(props, "render_from")
        col.prop(props, "render_to")
        col = layout.column()
        col.operator("nftgen.dummy", text="Render", icon="RENDERLAYERS")

class StatsPanel(bpy.types.Panel):
    bl_label = "Tokens Stats"
    bl_idname = "OBJECT_PT_stats"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'NFT Generator'
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        props = func.get_props()
        return props.mode == "1"

    def draw(self, context):
        traits = func.get_traits()
        traits_values = func.get_traits_values()

        layout = self.layout
        col = layout.column(align=True)
        # for tt in traits:
        #     col.label(text=f"{tt.metadata_name}:")
        #     trait_counter_dict = func.trait_stats(tt)
            
        #     for entry in trait_counter_dict.items():
        #         col = layout.column()
        #         row = col.row()
        #         row.label(text=f"{traits_values[entry[0]].metadata_name}: ")
        #         row.label(text=f"{entry[1]}")

        for tt in traits:
            col.prop(
                tt, 
                "expanded", 
                text=f"{tt.metadata_name}", 
                emboss=False, 
                icon="TRIA_DOWN" if tt.expanded else "TRIA_RIGHT"
            )

            trait_counter_dict = func.trait_stats(tt)
            for entry in trait_counter_dict.items():
                if tt.expanded:
                    col = layout.column()
                    row = col.row()
                    row.label(text=f"{traits_values[entry[0]].metadata_name}: ")
                    row.label(text=f"{entry[1]}")



classes = (
    ModePanel, 
    NavigatePanel, 
    TokenDetailsPanel, 
    GeneratePanel, 
    TRAITS_UL_items, 
    TRAITVALUES_UL_items, 
    TraitsPanel, 
    RulesPanel, 
    RenderPanel, 
    StatsPanel
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)