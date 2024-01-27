# NFT Generator
NFT Generator **turbocharges your creativity** by transforming isolated assets into **an explosion of unique NFT possibilities.** Forget painstaking manual combinations – The addon **randomizes, renders, and rules** your way to a diverse, stunning collection in a **single click.**
## Features
* **Randomly combine** your Objects, Collections, Materials, Textures, Worlds or Animation Actions – generate **thousands of unique variations** in an instant.
* **Batch-render** your entire collection with one click.
* **Automate metadata generation:** Say goodbye to manual data entry. NFT Generator **populates essential details** for each NFT, saving you precious time.
* **Fine-tune your chaos:** Define **rarity** for individual assets, controlling the frequency they appear in your collection. Craft **ultra-rare masterpieces** that stand out from the crowd!
* **Bend the rules of reality:** Go beyond random chance. Set **rules** to **associate or disassociate traits,** ensuring specific combinations appear (or never do) – **inject your artistic vision** into every generated NFT.
## Generate
### Trait
A trait refers to a specific characteristic or element that can be present on an NFT. It's a building block that, when combined with others, contributes to the overall visual and metadata makeup of each unique NFT in the collection.
#### Examples
- Skin Color
- Eyewear
- Background
#### Traits Types
![](./README_FILES/blender_a8TDo7Flab.png)

Traits can be used to control many aspects in the scene, not just `Objects` and `Collections`.
##### On `Materials`, `Images` and `Actions`
These 3 trait types need a `datablock` to be assigned to, the addon looks into all the trait choices and tries to find this `datablock`, otherwise it doesn't know which `datablock` in the scene to operate on, so:
- At least one of the **materials** in a trait needs to be assigned to an **object**.
- At least one of the **images** in a trait needs to be assigned to a **material** (as a texture in the shader nodes tree).
- At least one **action** in a trait needs to be assigned to an **object**. 
### Choice
Choices are the selected attributes to be assigned to a [trait](#Trait).
#### Examples
- Skin Color: Brown
- Eyewear: Sunglasses
- Background: Blue
#### Rarity
A percentage that resembles (approximately) how frequently a choice will be assigned to a trait.
##### Example
![](./README_FILES/blender_D6EMYBsgls.png)

`Pirate Eyepatch` will show up only in 10% of the tokens.
##### Max Unique Tokens
Is the maximum count of tokens that can be generated from all the assigned traits and choices, this number does not account for changes in `Rarity` and `Rules`.
### Rules
Rules let you say "yes, this goes together" or "no, that's not allowed" for different traits, shaping your collection's look and rarity.
#### Never With
Never associate Choice 1 and Choice 2 in the same token
#### Only With
Pick Choice 2 whenever Choice 1 exists
#### Always Pair With
Always associate Choice 1 and Choice 2 together, whenever any of them exists, the other should be assigned
#### Example
![](./README_FILES/blender_632B9aw5Yt.png)
1. `Sunglasses` will never show up in `Night` lighting.
2. `Blonde Moustache` will only show up on tokens with `Yellow Skin`.
3. Any token with `Pirate Eyepatch` will always use a `Pirate Sword` and vice versa.
## Edit
### Navigate Tokens
 ![](./README_FILES/blender_5YmE7ywauh.png)

 Change `Active Token` value to navigate through the collection, the addon will update the viewport to reflect the active token choices.
### Edit Individual Token Traits
![](./README_FILES/blender_Q9WTdg4Kjr.png)

Ever stare at your NFT collection, wishing you could tweak just one thing here or there? NFT Generator empowers you to change any choice of a token individually to fine tune your perfect collection.
### Tokens Stats
![](./README_FILES/blender_JMB9G4ENUD.png)

The `Token Stats` is a **read only** section that provides a comprehensive overview of your generated collection, revealing the frequency of each trait choice.
## Export
### Output Folder
![](./README_FILES/blender_XopMnzJmMV.png)

- `Output folder` is the parent folder where the rendered images and their metadata files are exported (`render` and `metadata`).
- By default output folder is set to `//` which an eloquent way to say it's the same folder where your blend file is saved, the addon creates the `render` and `metadata` folders for you if they don't exist. 
- `Open Output Folder` is a quick option to open the output folder in your OS file manager.
### Token Metadata
![](./README_FILES/blender_EGz4D3QXrn.png)
- `Description`: A description for your collection.
- `External URL`: The homepage of your collection.
- Token Name: The token id that shows up in the `name` key in metadata file, the hash `#` symbol is a placeholder for the **token number (index)**, you can add any suffix or prefix to it, make sure not to delete the `#` symbol otherwise all the tokens will end up having the same name or image in the collection.
#### Sample JSON metadata
```json
{
    "description": "My Awesome Project!",
    "external_url": "mywebsite.com",
    "image": "14.png",
    "name": "14",
    "attributes": [
        {
            "trait_type": "Face Hair",
            "value": "Paper Moustache"
        },
        {
            "trait_type": "Background Text",
            "value": "D"
        },
        {
            "trait_type": "Clothes",
            "value": "Tanktop"
        },
        {
            "trait_type": "Eyewear",
            "value": "Pirate Eyepatch"
        },
        {
            "trait_type": "Skin Color",
            "value": "Yellow Skin"
        },
        {
            "trait_type": "Face Tattoo",
            "value": "Empty"
        },
        {
            "trait_type": "Lighting",
            "value": "Night"
        },
        {
            "trait_type": "Facial Expression",
            "value": "Angry"
        }
    ]
}
```
#### Token Name and URL
Example of  `token name` and `image URL` prefixes:
![](./README_FILES/blender_pfSpPwelQV.png)
#### Sample JSON metadata
```json
{
    "description": "My Awesome Project!",
    "external_url": "mywebsite.com",
    "image": "mywebsite.com/monkey16.png",
    "name": "monkey16",
    "attributes": [
        {
            "trait_type": "Face Hair",
            "value": "None"
        },
        {
            "trait_type": "Background Text",
            "value": "B"
        },
        {
            "trait_type": "Clothes",
            "value": "Ballmer Shirt"
        },
        {
            "trait_type": "Eyewear",
            "value": "Pirate Eyepatch"
        },
        {
            "trait_type": "Skin Color",
            "value": "Brown Skin"
        },
        {
            "trait_type": "Face Tattoo",
            "value": "Tyson"
        },
        {
            "trait_type": "Lighting",
            "value": "Day"
        },
        {
            "trait_type": "Facial Expression",
            "value": "Angry"
        }
    ]
}
```
### Render/Export
![](./README_FILES/blender_d5HanXYAWB.png)
- `From` and `To` could be helpful if you had to edit some tokens after all the collection was rendered already, you can assign only the updated ones.
- `Render` to render all your tokens within the `From`: `To` range.
- `Export Metadata` to export all metadata files within the same `From`: `To` range.
## Installation
## Contact Me
- On the bird website: [@ahmed_ali](https://twitter.com/ahmed_ali)
- Mastodon: [premiero@mastodon.world](https://mastodon.world/@premiero)
- Hire me on [Upwork](https://www.upwork.com/freelancers/~0139b13dfd3e208f29)
## Get the Full Version
The addon version on Github has `Materials`, `Images`, `Worlds` and `Actions` commented out in the addon code, The full version is available at:
	- Blender Market (add link)
	- Gumroad (add link)
If you REALLY don't want to pay for it, and you happen to know `Python` feel free to uncomment them yourself, no hard feelings you earned it mate! 💪