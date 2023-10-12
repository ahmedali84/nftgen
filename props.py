import bpy
from . import functions as func
import json

def active_trait_id_update(self, context):
    traits = func.get_traits()
    all_trait_values = [
        tv for tv in func.get_traits_values()
    ]
        
    # get the last relevant trait value in the list
    relevant_trait_values = [
        tv for tv in all_trait_values if tv.trait_id  == traits[self.active_trait_id].name
    ]
    if relevant_trait_values:
        # print(all_trait_values.index(relevant_trait_values[-1]))
        self.active_trait_value_id = all_trait_values.index(relevant_trait_values[-1])
        
def metadata_name_update(self, context):
    traits = func.get_traits()
    active_trait = traits[self.trait_id]
    trait_type = active_trait.value_type

    TYPE_DATABLOCK_DICT = {
        '0':"object_", 
        '1':"collection_", 
        '2':"material_", 
        '3':"image_", 
        '4':"world_", 
        '5':"action_"
    }

    datablock_name = TYPE_DATABLOCK_DICT.get(trait_type)
    datablock = getattr(self, datablock_name)

    # update metadata name only if it's not assigned yet
    if datablock and not self.metadata_name:
        self.metadata_name = datablock.name

def active_token_update(self, context):
    func.set_active_token_props()

def active_token_set(self, value):
    tokens = func.get_tokens()
    new_value = min(max(0, value), len(tokens) - 1)
    self['active_token_id'] = new_value
 
def active_token_get(self):
    return self.get('active_token_id', 0)

def export_from_set(self, value):
    tokens = func.get_tokens()
    new_value = min(max(0, value), len(tokens) - 1)
    self['export_from'] = new_value

def export_from_get(self):
    return self.get('export_from', 0)

def export_to_set(self, value):
    tokens = func.get_tokens()
    new_value = min(max(0, value), len(tokens) - 1)
    self['export_to'] = new_value

def export_to_get(self):
    return self.get('export_to', 0)

def rules_items(scene, context):
    traits_values = func.get_traits_values()

    items = []
    # add an empty entry
    items.append(("0", "", ""))

    for tv in traits_values:
        items.append((tv.name, tv.metadata_name, ""))

    return items

def active_token_tv_items(self, context):
    items = []
    # items.append(("0", "", ""))

    # active_token_props = func.get_active_token_props()

    if self.trait:
        traits_values = func.get_traits_values()

        active_traits_values = [tv for tv in traits_values if tv.trait_id == self.trait]
        if active_traits_values:
            for tv in active_traits_values:
                items.append((tv.name, tv.metadata_name, ""))

    return items

def active_token_trait_update(self, context):
    # refresh the relevant traits values menu
    active_token_tv_items(context.scene, context)

def active_token_tv_update(self, context):
    token_dict = func.copy_active_token_props()

    # update viewport and render settings
    func.update_token(token_dict)

    # save to active token attributes
    props = func.get_props()
    tokens = func.get_tokens()
    token = tokens[props.active_token_id]
    token.attributes = json.dumps(token_dict)

class NFTGenProps(bpy.types.PropertyGroup):
    active_token_id: bpy.props.IntProperty(
        name="Active Token", 
        description="Active Token Number", 
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

    active_rule_id: bpy.props.IntProperty(default=0, min=0)

    mode: bpy.props.EnumProperty(
        items= [
            ("0", "Generate", "Generate", '', 0),
            ("1", "Edit", "Edit", '', 1), 
            ("2", "Export", "Export", '', 2)
        ],
        default= '0'
    )

    tokens_count: bpy.props.IntProperty(
        name="Tokens Count", 
        description="Number of Tokens to Generate", 
        min=1, 
        default=1
    )

    # render/export props
    export_from: bpy.props.IntProperty(
        name="From", 
        description="Token Index to Start Render/Export From", 
        min=0, 
        default=0, 
        get=export_from_get, 
        set=export_from_set
    )
    export_to: bpy.props.IntProperty(
        name="To", 
        description="Token Index to End Render/Export To", 
        min=0, 
        default=0, 
        get=export_to_get, 
        set=export_to_set
    )

    output_dir: bpy.props.StringProperty(
        name="Output Folder", 
        description="All Renders and Metadata will be Exported to this Folder", 
        default="//", 
        subtype="DIR_PATH"
    )

    # only true if traits order has been changed
    # or new traits have been added/removed
    traits_updated: bpy.props.BoolProperty(
        default=False
    )

    # Additional metadata props
    description: bpy.props.StringProperty(
        name="Description", 
        description="Description of This Project", 
        default=""
    )

    external_url: bpy.props.StringProperty(
        name="External URL", 
        description="URL for the Project Homepage", 
        default=""
    )

    token_name: bpy.props.StringProperty(
        name="Token Name", 
        description="Token Name Attribute in metadata\nHash symbol '#' resembles token index\nExample: 'monkey_#' for token no. 22 will be 'monkey_22'", 
        default="#"
    )

    image_url:bpy.props.StringProperty(
        name="Image URL", 
        description="URL of the Token Image in Metadata\nHash symbol '#' resembles token index\nExample 'http://myurl/monkey_#' for token no. 22 will be 'http://myurl/monkey_22.png'", 
        default="#"
    )

class Token(bpy.types.PropertyGroup):
    # index: bpy.props.IntProperty(
    #     name="Index", 
    #     default=0
    # )
    attributes: bpy.props.StringProperty(
        default=""
    )

    is_locked: bpy.props.BoolProperty(
        name="Lock", 
        description="This token will not be removed if a new collection of tokens is generated", 
        default=False
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
            ("0", "Objects", "Objects", 'OBJECT_DATA', 0),
            ("1", "Collections", "Collections", 'OUTLINER_COLLECTION', 1), 
            ("2", "Materials", "Materials", 'MATERIAL_DATA', 2), 
            ("3", "Images", "Images", 'IMAGE_DATA', 3), 
            ("4", "Worlds", "Worlds", 'WORLD_DATA', 4),
            ("5", "Actions", "Actions", 'ACTION', 5)
        ],
        default= '0'
    )

    expanded: bpy.props.BoolProperty(
        name="Expand", 
        default=False
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
        default=100.0, 
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
        update=metadata_name_update
    )

    collection_: bpy.props.PointerProperty(
        type=bpy.types.Collection, 
        update=metadata_name_update
    )

    material_: bpy.props.PointerProperty(
        type=bpy.types.Material, 
        update=metadata_name_update
    )

    image_: bpy.props.PointerProperty(
        type=bpy.types.Image, 
        update=metadata_name_update
    )

    world_: bpy.props.PointerProperty(
        type=bpy.types.World, 
        update=metadata_name_update
    )

    action_: bpy.props.PointerProperty(
        type=bpy.types.Action, 
        update=metadata_name_update
    )

class Rule(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(
        default="Rule"
    )

    enable: bpy.props.BoolProperty(
        default=True, 
        description="Enable/Disable runle in Tokens generation"
    )

    value_1: bpy.props.EnumProperty(
        items=rules_items
    )

    value_2: bpy.props.EnumProperty(
        items=rules_items
    )

    relation: bpy.props.EnumProperty(
        items= [
            ("0", "Never With", "Never with", '', 0),
            ("1", "Only With", "Only With", '', 1), 
            ("2", "Always Pair With", "Always Pair With", '', 2)
        ],
        default= '0'
    )

class ActiveTokenProps(bpy.types.PropertyGroup):
    trait: bpy.props.StringProperty(default="")
    trait_value: bpy.props.EnumProperty(
        items=active_token_tv_items, 
        update=active_token_tv_update
    )

classes = (
    NFTGenProps, 
    Token, 
    Trait, 
    TraitValue, 
    Rule, 
    ActiveTokenProps
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.nftgen = bpy.props.PointerProperty(type=NFTGenProps)
    bpy.types.Scene.tokens = bpy.props.CollectionProperty(type=Token)
    bpy.types.Scene.traits = bpy.props.CollectionProperty(type=Trait)
    bpy.types.Scene.traits_values = bpy.props.CollectionProperty(type=TraitValue)
    bpy.types.Scene.rules = bpy.props.CollectionProperty(type=Rule)
    bpy.types.Scene.active_token_props = bpy.props.CollectionProperty(type=ActiveTokenProps)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.nftgen
    del bpy.types.Scene.tokens
    del bpy.types.Scene.traits
    del bpy.types.Scene.traits_values
    del bpy.types.Scene.rules
    del bpy.types.Scene.active_token_props