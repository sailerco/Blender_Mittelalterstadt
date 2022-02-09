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
import bpy


from .test_op import test_OT_test
from .test_op import PROPS
from .mittelalter_PT_panel import mittelalter_PT_panel
from .cityWallGenerator_op import citywall_OT_
from .clear_workspace_op import clear_workspace_OT_


bl_info = {
    "name" : "Mittelalterstadt generieren",
    "author" : "Corinna Simon Janina Tamara",
    "description" : "Creates a medieval town with a wall and towers surrounding it.",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "View3D",
    "warning" : "",
    "category" : "Object"
}

# Alle Operationen die über das Addon ausgeführt werden können + Panel 
classes = (mittelalter_PT_panel, test_OT_test, citywall_OT_, clear_workspace_OT_)

def register():
    for(prop_name, prop_value) in PROPS:
        setattr(bpy.types.Scene, prop_name, prop_value)
    
    for c in classes:
        bpy.utils.register_class(c)

def unregister():
    for(prop_name, _) in PROPS:
        delattr(bpy.types.Scene, prop_name)

    for c in classes:
        bpy.utils.unregister_class(c)