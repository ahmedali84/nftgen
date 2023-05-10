import bpy
import uuid
import random
import json

def get_props():
    return bpy.context.scene.nftgen

def get_traits():
    return bpy.context.scene.traits

def get_traits_values():
    return bpy.context.scene.traits_values

def get_tokens():
    return bpy.context.scene.tokens

def remove_trait_values(trait_name):
    trait_values = get_traits_values()

    names_to_remove = [
        tv.name for tv in trait_values if tv.trait_id == trait_name
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

def update_token(token_index):
    tokens = get_tokens()
    token = tokens[token_index]

    traits_values = get_traits_values()

    # hide all relevant objects/collections
    relevant_objects = [
        tv.object_ for tv in traits_values if tv.object_
    ]

    for ob in relevant_objects:
        ob.hide_set(True)
        ob.hide_render = True

    relevant_collections = [
        tv.collection_ for tv in traits_values if tv.collection_
    ]

    for col in relevant_collections:
        col.hide_viewport = True
        col.hide_render = True

    
    # unhide the given token relevant objects/collections
    token_attributes = json.loads(token.attributes).values()
    for attr in token_attributes:
        trait_value = traits_values[attr]
        if trait_value.object_:
            trait_value.object_.hide_set(False)
            trait_value.object_.hide_render = False

        if trait_value.collection_:
            trait_value.collection_.hide_viewport = False
            trait_value.collection_.hide_render = False

    bpy.context.view_layer.update()