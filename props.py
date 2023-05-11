import bpy
from . import functions as func

def active_trait_id_update(self, context):
    all_trait_values = func.get_traits_values()

    # get the relevant trait values
    for tv in all_trait_values:
        if tv.trait_id == self.active_trait_id:
            idx = all_trait_values.find(tv.name)
            self.active_trait_value_id = idx
            return
        
def collection_object_update(self, context):
    if self.object_ and not self.metadata_name:
        self.metadata_name = self.object_.name

    if self.collection_ and not self.metadata_name:
        self.metadata_name = self.collection_.name

def active_token_update(self, context):
    func.update_token(self.active_token_id)

def active_token_set(self, value):
    tokens = func.get_tokens()
    new_value = min(max(0, value), len(tokens) - 1)
    self['active_token_id'] = new_value
 
def active_token_get(self):
    return self.get('active_token_id', 0)

class NFTGenProps(bpy.types.PropertyGroup):
    active_token_id: bpy.props.IntProperty(
        name="Active Token", 
        default=0, 
        min=0, 
        update=active_token_update, 
        get=active_token_get, 
        set=active_token_set
    )

    active_trait_id: bpy.props.IntProperty(
        default=0, 
        min=0, 
        update=active_trait_id_update
    )

    active_trait_value_id: bpy.props.IntProperty(default=0, min=0)

    mode: bpy.props.EnumProperty(
        items= [
            ("0", "Generate", "Generate", '', 0),
            ("1", "Edit", "Edit", '', 1), 
            ("2", "Render", "Render", '', 2)
        ],
        default= '0'
    )

    tokens_count: bpy.props.IntProperty(
        name="Tokens Count", 
        min=1, 
        default=1
    )

    # render props
    render_from: bpy.props.IntProperty(
        name="Render From", 
        min=0, 
        default=0
    )
    render_to: bpy.props.IntProperty(
        name="Render To", 
        min=0, 
        default=0
    )

class Token(bpy.types.PropertyGroup):
    index: bpy.props.IntProperty(
        name="Index", 
        default=0
    )
    attributes: bpy.props.StringProperty(
        default=""
    )
    
class Trait(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(
        name="Name", 
        default=""
    )

    metadata_name: bpy.props.StringProperty(
        name="Metadata Name", 
        default=""
    )

    enable: bpy.props.BoolProperty(
        description="Enable this trait", 
        default=True
    )

    value_type: bpy.props.EnumProperty(
        items= [
            ("0", "Objects", "Objects", '', 0),
            ("1", "Collections", "Collections", '', 1)
        ],
        default= '0'
    )

class TraitValue(bpy.types.PropertyGroup):
    trait_id: bpy.props.StringProperty(
        name="Trait ID"
    )
    
    name: bpy.props.StringProperty(
        name="Name", 
        default=""
    )

    metadata_name: bpy.props.StringProperty(
        name="Metadata Name", 
        default=""
    )

    rarity: bpy.props.FloatProperty(
        name="Rarity", 
        default=0.0, 
        min=0.0, 
        max=100.0, 
        subtype='PERCENTAGE'
    )
    
    enable: bpy.props.BoolProperty(
        description="Enable this trait value", 
        default=True
    )

    object_: bpy.props.PointerProperty(
        type=bpy.types.Object, 
        update=collection_object_update
    )

    collection_: bpy.props.PointerProperty(
        type=bpy.types.Collection, 
        update=collection_object_update
    )

classes = (
    NFTGenProps, 
    Token, 
    Trait, 
    TraitValue
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.nftgen = bpy.props.PointerProperty(type=NFTGenProps)
    bpy.types.Scene.tokens = bpy.props.CollectionProperty(type=Token)
    bpy.types.Scene.traits = bpy.props.CollectionProperty(type=Trait)
    bpy.types.Scene.traits_values = bpy.props.CollectionProperty(type=TraitValue)   

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.nftgen
    del bpy.types.Scene.tokens
    del bpy.types.Scene.traits
    del bpy.types.Scene.traits_values