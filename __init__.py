# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import importlib
if "bpy" in locals():
    importlib.reload(functions)
    importlib.reload(props)
    importlib.reload(ops)
    importlib.reload(generate_tokens)
    importlib.reload(ui)
    importlib.reload(metadata)
    importlib.reload(render)
else:
    import bpy
    from. import functions
    from . import props
    from . import ops
    from . import generate_tokens
    from . import ui
    from . import metadata
    from . import render


bl_info = {
    "name" : "NFT Generator",
    "author" : "@ahmed_ali",
    "description" : "Generate Non Fungible Tokens using Blender",
    "blender" : (3, 40, 1),
    "version" : (0, 0, 1),
    "location" : "View 3D > NFT Generator",
    "warning" : "",
    "category" : "3D View",
    "wiki_url": ""
}


def register():
    props.register()
    ops.register()
    generate_tokens.register()
    ui.register()

def unregister():
    props.unregister()
    ops.unregister()
    generate_tokens.unregister()
    ui.unregister()