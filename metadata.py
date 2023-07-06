import bpy
from . import functions as func
import json

class ExportMetadata(bpy.types.Operator):
    bl_idname = "nftgen.export_metadata"
    bl_label = "Export Metadata"
    bl_description = "Export metadata to destination folder"
    bl_options = {'UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        self.report({'INFO'}, "Export Metadata")
        props = func.get_props()
        tokens = func.get_tokens()

        start = props.export_from
        end = props.export_to

        metadata_dir = func.get_metadata_export_folder()
        render_file_ext = func.get_render_ext()

        # get the token attributes dictionary
        for i in range(start, end + 1):
            token = tokens[i]
            token_dict = json.loads(token.attributes)

            ID_NAME_DICT = func.get_id_name_dict()
            
            # change dict data to use names instead of uuid's
            renamed_keys = [ID_NAME_DICT[key] for key in token_dict.keys()]
            renamed_values = [ID_NAME_DICT[value] for value in token_dict.values()]
            token_json_dict = dict(zip(renamed_keys, renamed_values))
        
            # prepare the json data to export
            attributes = [
                {
                    "trait_type": name, 
                    "value": value
                }
                for name, value in token_json_dict.items()
            ]

            metadata = {
                "attributes": attributes,
                "description": "My project is awesome!",
                "external_url": f"https://my_url.nft",
                "image": f"{i}{render_file_ext}", 
                "name": f"{i}"
            }

            func.export_json(metadata_dir, metadata, i)

        # get the metadata export folder
        return {'FINISHED'}