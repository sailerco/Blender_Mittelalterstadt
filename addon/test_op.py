import bpy
from bpy.types import Operator

PROPS=  [
            ('towerCount', bpy.props.IntProperty(name = 'Tower', description='int value of Towers', default=7, min=4, max=15)),
            ('radius', bpy.props.IntProperty(name = 'Radius', description='int value of Radius', default=25, min=4, max=95)),
            ('hasChurch', bpy.props.BoolProperty(name='Show church', default=True)),
            ('isRound', bpy.props.BoolProperty(name='Round shape', default=False))
        ]

class test_OT_test(Operator):
    bl_idname = "object.apply_all_mods"
    bl_label = "Apply all"
    bl_description = "Apply all operators of the active object"

    @classmethod
    def poll(cls, context):
        obj = context.object 

        if obj is not None:
            if obj.mode == "OBJECT":
                return True
            return False
        
    def execute(self, context):
        active_obj = context.view_layer.objects.active

        for mod in active_obj.modifiers: 
            bpy.ops.object.modifier_apply(modifier=mod.name)

        return{'FINISHED'}