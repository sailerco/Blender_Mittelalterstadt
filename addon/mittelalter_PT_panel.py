import bpy 

from bpy.types import Panel

# Usereingaben, inspiriert von: https://medium.com/geekculture/creating-a-custom-panel-with-blenders-python-api-b9602d890663 
PROPS=  [
            ('tower_count', bpy.props.IntProperty(name = 'Tower', description='int value of Towers', default=7, min=5, max=15)),
            ('radius', bpy.props.IntProperty(name = 'Radius', description='int value of Radius', default=40, min=30, max=200)),
            ('has_church', bpy.props.BoolProperty(name='Show church', default=True)),
            ('is_round', bpy.props.BoolProperty(name='Round shape', default=False)),
            ('color_roof', bpy.props.FloatVectorProperty(name="Roof color Tower", subtype="COLOR",size=4,min=0.0,max=1.0,default=(0.027, 0.067, 0.296, 1.0)))
        ]

# _PT_ muss im Namen drin sein! 
class mittelalter_PT_panel(Panel):
    # space und region zuständig für Ort der Darstellung, nicht ändern
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Mittelalterstadt generieren"
    bl_category = "Mittelalterstadt"

# Layout machen und Buttons etc. 
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        col = self.layout.column()
        for(prop_name, _) in PROPS:
            row = col.row()
            row.prop(context.scene, prop_name)
        col.operator("object.add_city_wall_and_tower", text="Generate")
        col.operator("object.delet_all", text="Clear Workspace")