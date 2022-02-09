import bpy
from bpy.types import Operator

PROPS=  [
            ('towerCount', bpy.props.IntProperty(name = 'Tower', description='int value of Towers', default=7, min=5, max=15)),
            ('radius', bpy.props.IntProperty(name = 'Radius', description='int value of Radius', default=40, min=10, max=60)),
            ('hasChurch', bpy.props.BoolProperty(name='Show church', default=True)),
            ('isRound', bpy.props.BoolProperty(name='Round shape', default=False))
        ]

class test_OT_test(Operator):
    bl_idname = "object.apply_all_mods"
    bl_label = "Apply all"
    bl_description = "Apply all operators of the active object"
        
    def execute(self, context):
        print('Test, Testclasse')

        return{'FINISHED'}