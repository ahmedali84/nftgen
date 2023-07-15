import bpy
from . import functions as func
import json

class ExportMetadata(bpy.types.Operator):
    bl_idname = "nftgen.export_metadata"
    bl_label = "Export Metadata"
    bl_description = "Export All Tokens Metadata of Indices in Range 'From' to 'To'"
    bl_options = {'UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        self.report({'INFO'}, "Export Metadata")
        props = func.get_props()
        tokens = func.get_tokens()

        # check if # exists in token name and image url
        hash_symbol_exists = all([
            "#" in props.token_name, 
            "#" in props.image_url
        ])
        if not hash_symbol_exists:
            self.report(type={'ERROR'}, message="Token Name and Image URL must include a # symbol")
            return {'CANCELLED'}

        start = props.export_from
        end = props.export_to

        metadata_dir = func.get_export_folder("metadata")
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
                "description": props.description,
                "external_url": props.external_url,
                "image": props.image_url.replace("#", f"{i}{render_file_ext}"), 
                "name": props.token_name.replace("#", str(i)), 
                "attributes": attributes,
            }

            func.export_json(metadata_dir, metadata, i)
        return {'FINISHED'}