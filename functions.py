import bpy
import uuid
import random
import json
from math import prod
from collections import Counter

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
        if token_dict and rule.enable:
            token_dict = RELATIONS[rule.relation](token_dict, rule.value_1, rule.value_2)

    return token_dict