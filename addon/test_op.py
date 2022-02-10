import bpy
from bpy.types import Operator

PROPS=  [
            ('tower_count', bpy.props.IntProperty(name = 'Tower', description='int value of Towers', default=7, min=5, max=15)),
            ('radius', bpy.props.IntProperty(name = 'Radius', description='int value of Radius', default=40, min=15, max=200)),
            ('has_church', bpy.props.BoolProperty(name='Show church', default=True)),
            ('is_round', bpy.props.BoolProperty(name='Round shape', default=False))
        ]

class test_OT_test(Operator):
    bl_idname = "object.apply_all_mods"
    bl_label = "Apply all"
    bl_description = "Apply all operators of the active object"
        
    def execute(self, context):
        
        params = {
            context.scene.radius,
            context.scene.tower_count
        }

        print(context.scene.tower_count)
        print(PROPS[1])
    
        return{'FINISHED'}