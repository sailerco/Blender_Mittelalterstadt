from multiprocessing import context
from pickle import FALSE
import bpy
import math
from bpy.types import Operator

from addon.generate_house_circle_help import generate_house_circle
from addon.well_help import well
from .church_help import church

class citywall_OT_(Operator):
    #Addon
    bl_idname = "object.add_city_wall_and_tower"
    bl_label = "Add Citywall and Tower"
    bl_description = "Adds the citywall and towers as given by the user"

    #für andere classes 
    scene_context = bpy.context
    scene_data = bpy.data

    #Werden vom Userinput teilweise überschrieben/neuberechnet siehe execute
    tower_count = 5
    radius = 50
    
    tower_height = 12
    tower_radius = 2
    wall_thickness = 0.5

    roof_height = 4
    roof_overhang = 0.5
    roof_color = (1.0, 1.0, 1.0, 1.0)

    texture_scale = 20
 
    wall_height = 8
    wall_thickness= 0
    inner_radius = 0
    
    gate_radius =  0
    GATE_HEIGHT = 4
    GATE_WIDTH = 3

    wall_vertices = 32

## generiert einzelnen Turm
    def generate_base(self, tower_location, tower_height):
        bpy.ops.mesh.primitive_cylinder_add(radius=self.tower_radius, depth=tower_height, location=tower_location)
        
        mod_solid = bpy.context.object.modifiers.new('Wall Thickness','SOLIDIFY')
        mod_solid.thickness = self.wall_thickness
        
        mat_tower_base = bpy.data.materials.new("tower_base")
        mat_tower_base.use_nodes = True

        nodes = mat_tower_base.node_tree.nodes
        node_principled: bpy.types.Node = nodes['Principled BSDF']

        node_brick: bpy.types.Node = nodes.new("ShaderNodeTexBrick")
        node_coords: bpy.types.Node = nodes.new("ShaderNodeTexCoord")

        mat_tower_base.node_tree.links.new(node_brick.outputs[0], node_principled.inputs[0])
        mat_tower_base.node_tree.links.new(node_coords.outputs[2], node_brick.inputs[0])

        node_brick.inputs[1].default_value = [0.35, 0.35, 0.35, 1.0]
        node_brick.inputs[1].default_value = [0.11, 0.13, 0.19, 1.0]
        node_brick.inputs[4].default_value = self.texture_scale

        bpy.context.object.data.materials.append(mat_tower_base)

        mat_tower_roof = bpy.data.materials.new("tower_roof")
        mat_tower_roof.use_nodes = True
        mat_tower_roof.node_tree.nodes["Principled BSDF"].inputs[0].default_value = self.roof_color

        bpy.ops.mesh.primitive_cone_add(radius1= self.tower_radius + self.roof_overhang, radius2=0, depth=self.roof_height, location=(tower_location[0], tower_location[1], tower_height + self.roof_height / 2))

        bpy.context.object.data.materials.append(mat_tower_roof) 
        
##generiert alle Türme
    def generate_towers(self):
        for i in range(self.tower_count):
        #my_tower = tower()
            x_value = math.sin(2*math.pi/self.tower_count * i) * self.radius
            y_value = math.cos(2*math.pi/self.tower_count * i) * self.radius
            tower_location=(x_value, y_value, self.tower_height/2)
            self.generate_base(tower_location, self.tower_height)
    
            bpy.ops.transform.rotate(value=(2*math.pi/self.tower_count * i), orient_axis='Z', orient_type='GLOBAL')
    
    def generateGates(self, wall):
        wall_obj = wall
        
        for i in range(self.tower_count):
            x_value = math.sin(2*math.pi/self.tower_count * (i + 0.5)) * self.radius 
            y_value = math.cos(2*math.pi/self.tower_count * (i +0.5)) * self.radius 
           
            #gate_cube     
            bpy.ops.mesh.primitive_cube_add(location=(x_value, y_value, 0), scale=(self.radius, self.GATE_WIDTH, self.GATE_HEIGHT))
            gate_cube = bpy.context.object
            bpy.ops.transform.rotate(value=(2*math.pi/self.tower_count * i+math.pi/self.tower_count) + 1.5708, orient_axis='Z', orient_type='GLOBAL')
            bpy.context.object.hide_viewport = True
            
            wall_boolean = wall_obj.modifiers.new("booleantop", "BOOLEAN")
            wall_boolean.object = gate_cube
            
            #gate_cylinder
            bpy.ops.mesh.primitive_cylinder_add(enter_editmode=False, align='WORLD', location=(x_value, y_value, self.GATE_HEIGHT), scale=(1, self.GATE_WIDTH, self.radius))
            gate_cylinder = bpy.context.object
            bpy.ops.transform.rotate(value=1.5708, orient_axis='Y', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, True, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
            bpy.ops.transform.rotate(value=(2*math.pi/self.tower_count * i+math.pi/self.tower_count) + 1.5708, orient_axis='Z', orient_type='GLOBAL')
            bpy.context.object.hide_viewport = True
            
            wall_boolean = wall_obj.modifiers.new("booleantop", "BOOLEAN")
            wall_boolean.object = gate_cylinder


##generiert Stadtmauer
    def generate_wall(self):
        bpy.ops.mesh.primitive_cylinder_add(vertices=self.wall_vertices, radius=self.radius, depth=self.wall_height, location=(0, 0, self.wall_height/2))
       
        mat_wall = bpy.data.materials.new("material_wall")
        mat_wall.use_nodes = True
        nodes = mat_wall.node_tree.nodes
        node_principled: bpy.types.Node = nodes['Principled BSDF']
        node_brick: bpy.types.Node = nodes.new("ShaderNodeTexBrick")
        node_coords: bpy.types.Node = nodes.new("ShaderNodeTexCoord")
        mat_wall.node_tree.links.new(node_brick.outputs[0], node_principled.inputs[0])
        mat_wall.node_tree.links.new(node_coords.outputs[2], node_brick.inputs[0])
        node_brick.inputs[1].default_value = [0.35, 0.35, 0.35, 1.0]
        node_brick.inputs[1].default_value = [0.11, 0.13, 0.19, 1.0]
        ##Brick Scale
        node_brick.inputs[4].default_value = 50
        ##Brick Höhe
        node_brick.inputs[9].default_value = 0.65
        ##Brick Länge
        node_brick.inputs[8].default_value = 0.35
        node_brick.inputs[5].default_value = 0.01

        bpy.context.object.data.materials.append(mat_wall)

        cube_contextBigC = bpy.context.object 
        bpy.ops.mesh.primitive_cylinder_add(vertices=self.wall_vertices, radius=self.inner_radius, depth=self.wall_height, location=(0, 0, self.wall_height/2))
        bpy.context.object.hide_viewport = True

        cube_context = bpy.context.object          
        boolean_mod = cube_contextBigC.modifiers.new("boolean", "BOOLEAN")
        boolean_mod.object = cube_context

        bpy.ops.mesh.primitive_cylinder_add(vertices=self.wall_vertices, radius=self.radius + self.radius*0.01, depth=self.wall_height*0.02, location=(0, 0, self.wall_height))
        
        mat_wall_top = bpy.data.materials.new("material_wall_top")
        mat_wall_top.use_nodes = True
        mat_wall_top.node_tree.nodes["Principled BSDF"].inputs[0].default_value = [0.047, 0.055, 0.078, 1.0]
        bpy.context.object.data.materials.append(mat_wall_top) 
        
        cylinder_top = bpy.context.object 
        bpy.ops.mesh.primitive_cylinder_add(vertices=self.wall_vertices, radius=self.inner_radius, depth=self.wall_height*0.02, location=(0, 0, self.wall_height))
       
        bpy.context.object.hide_viewport = True
        cylinder_top_inner = bpy.context.object
        boolean_cylinder_top = cylinder_top.modifiers.new("booleantop", "BOOLEAN")
        boolean_cylinder_top.object = cylinder_top_inner
        
        self.generateGates(cube_contextBigC)

    ## generiert Boden für die gesamte Stadt
    def generate_city_floor(self):
        bpy.ops.mesh.primitive_cylinder_add(vertices=self.wall_vertices, radius=self.radius, depth=0.1, location=(0, 0, -0.05))

        ##Textur
        mat_floor = bpy.data.materials.new("floor_material")
        mat_floor.use_nodes = True
        
        nodes = mat_floor.node_tree.nodes
        node_principled: bpy.types.Node = nodes['Principled BSDF']

        node_floor: bpy.types.Node = nodes.new("ShaderNodeTexBrick")

        mat_floor.node_tree.links.new(node_floor.outputs[0], node_principled.inputs[0])
        node_floor.inputs[1].default_value = (0.170835, 0.0679258, 0.029515, 1)
        node_floor.inputs[2].default_value = (0.0952764, 0.0134412, 0, 1)
        #Scale
        node_floor.inputs[4].default_value = 100
        #Brick Höhe
        node_floor.inputs[9].default_value = 0.3
        #Brick Länge
        node_floor.inputs[8].default_value = 0.2
       
        bpy.context.object.data.materials.append(mat_floor)        

    #Keine Paramter löschen, wird zum Erkennen benögitgt 
    def execute(self, context):
        #Userinput übernehmen/ damit rechnen
        self.tower_count = context.scene.tower_count
        self.radius = context.scene.radius

        self.wall_thickness= self.tower_radius-0.5
        self.inner_radius = self.radius - self.wall_thickness
        
        self.gate_radius =  math.radians(360/self.tower_count)

        #Default 32 = Kreis
        if(context.scene.is_round == False):
            self.wall_vertices = self.tower_count
        
        self.roof_color = context.scene.color_roof

        self.generate_towers()
        self.generate_wall()
        self.generate_city_floor()

        houseClass = generate_house_circle()
        houseClass.generate(self.tower_count, self.radius, context.scene.is_round, self.wall_thickness)

        wellClass = well()
        wellClass.generateWell()

        #Kirche
        if context.scene.has_church:
            church_class = church()
            church_class.generate_church()

        return{'FINISHED'}