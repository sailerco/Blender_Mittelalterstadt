import bpy 

from bpy.types import Panel
from .test_op import PROPS

# _PT_ muss im Namen drin sein! 
class mittelalter_PT_panel(Panel):
    # space und region zuständig für Ort der Darstellung, nicht ändern
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    # bl_space_type = "PROPERTIES"
    # bl_region_type = "WINDOW"
    # bl_context = "material"
    bl_label = "Mittelalterstadt generieren"
    bl_category = "Mittelalterstadt"

# Layout machen und Buttons etc
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        col = self.layout.column()
        for(prop_name, _) in PROPS:
            row = col.row()
            row.prop(context.scene, prop_name)
        col.operator("object.add_city_wall_and_tower", text="Generate")
        col.operator("object.delet_all", text="Clear Workspace")