import bpy
import uuid
import random
import json
from math import prod
from collections import Counter
import os

def get_props():
    return bpy.context.scene.nftgen

def get_traits():
    return bpy.context.scene.traits

def get_traits_values():
    return bpy.context.scene.traits_values

def get_tokens():
    return bpy.context.scene.tokens

def get_rules():
    return bpy.context.scene.rules

def get_active_token_props():
    return bpy.context.scene.active_token_props

def remove_trait_values(trait):
    trait_values = get_traits_values()

    names_to_remove = [
        tv.name for tv in trait_values if tv.trait_id == trait.name
    ]

    for name in names_to_remove:
        idx = trait_values.find(name)
        trait_values.remove(idx)

def generate_random_id():
    return str(uuid.uuid4())

def pick_random_choice(trait):
    """Pick a random choice from the available trait values for the geven trait"""
    traits_values = get_traits_values()
    current_trait_values = [
        tv for tv in traits_values if tv.trait_id == trait.name
    ]

    # prepare rarity dictionary
    rarity_dict = {}
    for tv in current_trait_values:
        rarity_dict[tv.name] = tv.rarity

    # pick a random choice
    choice = random.choices(
        list(rarity_dict.keys()), 
        weights=list(rarity_dict.values())
    )

    return choice[0]

def update_token(token_dict):
    traits = get_traits()
    traits_values = get_traits_values()

    for trait_name, trait_value_name in token_dict.items():
        trait_index = traits.find(trait_name)
        trait_value_index = traits_values.find(trait_value_name)

        if trait_index == -1 or trait_value_index == -1:
            print("Unable to  update token, some properties have been removed!")
        else:
            update_attribute(traits[trait_name], traits_values[trait_value_name])

    # # hide all relevant objects/collections
    # relevant_objects = [
    #     tv.object_ for tv in traits_values if tv.object_
    # ]

    # for ob in relevant_objects:
    #     ob.hide_set(True)
    #     ob.hide_render = True

    # relevant_collections = [
    #     tv.collection_ for tv in traits_values if tv.collection_
    # ]

    # for col in relevant_collections:
    #     col.hide_viewport = True
    #     col.hide_render = True

    
    # # unhide the given token relevant objects/collections
    # token_attributes = token_dict.values()
    # for attr in token_attributes:
    #     trait_value = traits_values[attr]
    #     if trait_value.object_:
    #         trait_value.object_.hide_set(False)
    #         trait_value.object_.hide_render = False

    #     if trait_value.collection_:
    #         trait_value.collection_.hide_viewport = False
    #         trait_value.collection_.hide_render = False

    # bpy.context.view_layer.update()

def max_unique_tokens():
    """Get maximum number of available unique variations"""
    traits_values = get_traits_values()
    
    rec_list = [tv.trait_id for tv in traits_values]
    counter_dict = Counter(rec_list)

    return prod(list(counter_dict.values()))

def trait_stats(trait):
    """Calculate the percentage of trait value occurences in the tokens stack"""
    tokens = get_tokens()

    trait_values = []
    for tk in tokens:
        token_attributes = json.loads(tk.attributes)
        trait_values.append(token_attributes[trait.name])

    return Counter(trait_values)

def never_with(token_dict, val_1, val_2):
    """Empty token if val_1 and val_2 exist in the token dictionary"""
    if val_1 in token_dict.values() and val_2 in token_dict.values():
        return None
    else:
        return token_dict
    
def only_with(token_dict, val_1, val_2):
    """If val_1 in token change the relevant trait to val_2"""
    traits_values = get_traits_values()

    if val_1 in token_dict.values():
        token_dict[traits_values[val_2].trait_id] = val_2
        return token_dict
    else:
        # do nothing
        return token_dict

def always_pair_with(token_dict, val_1, val_2):
    """Always make sure if either values exist in token the relevant trait 
    updeted to equal the other one"""
    traits_values = get_traits_values()

    if val_1 in token_dict.values():
        token_dict[traits_values[val_2].trait_id] = val_2
        return token_dict
    
    elif val_2 in token_dict.values():
        token_dict[traits_values[val_1].trait_id] = val_1
        return token_dict
    
    else:
        # do nothing
        return token_dict

def apply_rules(token_dict):
    """Apply all the rules in the rules stack"""
    RELATIONS = {
        '0': never_with, 
        '1': only_with, 
        '2': always_pair_with
    }

    rules = get_rules()
    for rule in rules:
        if token_dict and rule.enable and is_rule_valid(rule):
            token_dict = RELATIONS[rule.relation](token_dict, rule.value_1, rule.value_2)

    return token_dict

def is_rule_valid(rule):
    """Detect if rule is valid"""
    # value_1 and value_2 are not empty
    if '0' in [rule.value_1, rule.value_2]:
        return False

    # value_1 doesn't equel value_2
    if rule.value_1 == rule.value_2:
        return False
    
    return True

def set_active_token_props():
    props = get_props()
    tokens = get_tokens()
    active_token = tokens[props.active_token_id]
    active_token_dict = json.loads(active_token.attributes)

    active_token_props = get_active_token_props()
    active_token_props.clear()

    for trait_id, trait_value_id in active_token_dict.items():
        new_token_prop = active_token_props.add()
        new_token_prop.trait = trait_id
        try:
            new_token_prop.trait_value = trait_value_id
        except:
            pass

def copy_active_token_props():
    active_token_props = get_active_token_props()

    token_data = {}
    for entry in active_token_props:
        token_data[entry.trait] = entry.trait_value

    return token_data

def generate_token_data(traits):
    """Randomly generate token data according to the given traits"""
    token_data = {}
    for tt in traits:
        choice = pick_random_choice(tt)
        token_data[tt.name] = choice

    return token_data

def get_id_name_dict():
    """Return a dictionary of id: metadata_name for all traits and trait values"""
    traits = get_traits()
    traits_values = get_traits_values()

    id_name_dict = {}
    for t in traits:
        id_name_dict[t.name] = t.metadata_name

    for t in traits_values:
        id_name_dict[t.name] = t.metadata_name

    return id_name_dict

def get_export_folder(name):
    """Get metadata export folder, create if not exist"""
    props = get_props()
    output_dir = bpy.path.abspath(props.output_dir)
    export_dir = os.path.join(output_dir, name)
    if not os.path.exists(export_dir):
        os.makedirs(export_dir)
    
    return export_dir

def export_json(export_dir, metadata, i):
    """Export json file to the designated folder with the id as a name"""
    json_filepath = os.path.join(export_dir, f"{i}.json")
    with open(json_filepath, "w") as output:
        json.dump(metadata, output, indent=4)

def get_render_ext():
    """Get the file extension for output render"""
    scene = bpy.context.scene
    file_format = scene.render.image_settings.file_format

    if file_format in ['AVI_JPEG', 'AVI_RAW', 'FFMPEG']:
        ext = {
            'MPEG1': 'mpeg1',
            'MPEG2': 'mpeg2',
            'MPEG4': 'mp4',
            'AVI': 'avi',
            'QUICKTIME': 'mov',
            'DV': 'dv',
            'OGG': 'ogg',
            'MKV': 'mkv',
            'FLASH': 'flv',
            'WEBM': 'webm'
        }
        return '.' + ext[bpy.context.scene.render.ffmpeg.format]
    
    else:
        return scene.render.file_extension
    
def traits_updated():
    """Compare traits to active token traits to detect any change in traits
    that requires re-generating the tokens"""
    tokens = get_tokens()
    traits = get_traits()
    active_token_props = get_active_token_props()

    traits_list = tuple([t.name for t in traits])
    active_token_list = tuple([prop.trait for prop in active_token_props])

    return all([bool(tokens), hash(traits_list) != hash(active_token_list)])

def sum_rarities(trait):
    """Check if the given trait has sum(rarities) == 0
    since this case causes an issue with the random generation function"""
    all_traits_values = get_traits_values()
    trait_rarities = [
        tv.rarity for tv in all_traits_values if tv.trait_id == trait.name
    ]
    return sum(trait_rarities)

def get_candidate_tv(trait_value):
    """Get the index of the next candidate trait value after removing the trait_value
    in function input"""
    # get preceding and secceeding tvs in the active trait
    active_trait_id = trait_value.trait_id

    traits_values = get_traits_values()
    active_trait_values = [tv for tv in traits_values if tv.trait_id == active_trait_id]
    active_trait_value_index = active_trait_values.index(trait_value)

    upper_tv_index = max(0, active_trait_value_index - 1 )
    lower_tv_index = min(len(active_trait_values) - 1, active_trait_value_index + 1)

    if len(active_trait_values) == 1:
        # the only trait value in the list
        return None
    
    if upper_tv_index == active_trait_value_index == 0:
        # active trait value is the first one in the list
        return active_trait_values[lower_tv_index].name
    else:
        return active_trait_values[upper_tv_index].name
    
def update_attribute(trait, trait_value):
    """Update attribute in viewport depending on trait type
    This is a wrapper function for viewport update functions"""
    # get trait

    # assign an update function depending on trait type
    UPDATE_FUNC = {
        '0':update_object, 
        '1':update_collection, 
        '2':update_material, 
        '3':update_world,  
    }

    # update the relevant trait in viewport
    UPDATE_FUNC[trait.value_type](trait, trait_value)

def update_object(trait, trait_value):
    """Update object in viewport"""
    # hide all objects relevant to trait
    traits_values = get_traits_values()
    relevant_objects = [
        tv.object_ for tv in traits_values if tv.trait_id == trait.name 
        and bool(tv.object_)
    ]

    for ob in relevant_objects:
        ob.hide_set(True)
        ob.hide_render = True

    # unhide object with the name value
    ob = trait_value.object_
    ob.hide_set(False)
    ob.hide_render = False

    bpy.context.view_layer.update()

def update_collection(trait, trait_value):
    """Update collection in viewport"""
    # hide all collections relevant to the givven trait
    traits_values = get_traits_values()
    relevant_collections = [
        tv.collection_ for tv in traits_values if tv.trait_id == trait.name 
        and bool(tv.collection_)
    ]

    for col in relevant_collections:
        col.hide_viewport = True
        col.hide_render = True

    col = trait_value.collection_
    col.hide_viewport = False
    col.hide_render = False
    
    bpy.context.view_layer.update()

def update_material(trait, trait_value):
    # get all objects using this material
    # but how to get relevant objects
    traits_values = get_traits_values()
    trait_materials = [
        tv.material_ for tv in traits_values 
        if tv.trait_id == trait.name and bool(tv.material_)
    ]

    # get a list of all objects using any of the trait materials
    relevant_objects_slots = set()
    for mat in trait_materials:
        user_objects_slots = get_material_users(mat)
        if user_objects_slots:
            relevant_objects_slots.update(user_objects_slots)

    # replace all materials in the relevant objects material sockets
    material = trait_value.material_

    for ob, slot_index in relevant_objects_slots:
        ob.material_slots[slot_index].material = material

    bpy.context.view_layer.update()

def update_world(trait, trait_value):
    """Update world in viewport"""
    scene = bpy.context.scene
    world = trait_value.world_

    if world:
        scene.world = world

    bpy.context.view_layer.update()

def get_material_users(material):
    """Return a list of all objects that use this material and the relevant
    material slot"""
    user_objects = set()
    for ob in bpy.data.objects:
        try:
            for slot in ob.material_slots:
                if slot.material == material:
                    user_objects.add((ob, slot.slot_index))
        except:
            pass
    
    return user_objects

def existing_tokens_msg(operator):
    operator.report({'ERROR'}, message="Clear Existing Tokens")