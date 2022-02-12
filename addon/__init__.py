import bpy
from .mittelalter_PT_panel import mittelalter_PT_panel, PROPS
from .city_wall_generator_op import citywall_OT_
from .clear_workspace_op import clear_workspace_OT_

# Struktur Addon-Aufteilung inspiriert von: https://www.youtube.com/watch?v=yNdjdmepMMQ
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

# Alle Operationen/Buttons die über das Addon ausgeführt werden können + Panel 
classes = (mittelalter_PT_panel, citywall_OT_, clear_workspace_OT_)

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