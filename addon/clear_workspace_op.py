import bpy
from bpy.types import Operator

class clear_workspace_OT_(Operator):
    bl_idname = "object.delet_all"
    bl_label = "Delete all"
    bl_description = "Delete all objects"
        
    def execute(self, context):

        # Code aus Vorlesung 
        bpy.ops.object.select_all(action='SELECT') # selektiert alle Objekte
        bpy.ops.object.delete(use_global=False, confirm=False) # löscht selektierte objekte
        bpy.ops.outliner.orphans_purge() # löscht überbleibende Meshdaten etc.
            
        return{'FINISHED'}