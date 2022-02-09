import bpy 

from bpy.types import Panel

# _PT_ muss im Namen drin sein! 
class mittelalter_PT_panel(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Mittelalterstadt generieren"
    bl_category = "Mittelalterstadt"

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        col = row.column()
        #todo
        col.operator("object.apply_all_mods", text="Generate") 

        #col = row.column()
        #todo
        #col.operator("object.chancel_all_mods", text="Alles löschen")