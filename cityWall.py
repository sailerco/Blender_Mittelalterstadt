import bpy
import math


class cityWall():

    TOWER_COUNT = 10
    RADIUS = 50
    
    tower_height = 12
    tower_radius = 2
    wall_thickness = 0.5

    roof_height = 4
    roof_overhang = 0.5

    texture_scale = 20

    wall_height = 8
    wall_thickness=tower_radius-0.5
    INNER_RADIUS = RADIUS - wall_thickness
    
    gate_radius =  math.radians(360/TOWER_COUNT)
    GATE_HEIGHT = 1
    GATE_WIDTH = 1.4
    WALL_WIDTH = wall_thickness
    
    x = []
    y = []
   


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
        mat_tower_roof.node_tree.nodes["Principled BSDF"].inputs[0].default_value = [0.07, 0.31, 0.19, 1.0]

        bpy.ops.mesh.primitive_cone_add(radius1= self.tower_radius + self.roof_overhang, radius2=0, depth=self.roof_height, location=(tower_location[0], tower_location[1], tower_height + self.roof_height / 2))

        bpy.context.object.data.materials.append(mat_tower_roof) 
        
##generiert alle Türme
    def generate_towers(self):
        for i in range(self.TOWER_COUNT):
        #my_tower = tower()
            x_value = math.sin(2*math.pi/self.TOWER_COUNT * i) * self.RADIUS
            y_value = math.cos(2*math.pi/self.TOWER_COUNT * i) * self.RADIUS
            tower_location=(x_value, y_value, self.tower_height/2)
            self.x.append(x_value)
            self.y.append(y_value)
            self.generate_base(tower_location, self.tower_height)

            t = bpy.context.object
    
            bpy.ops.transform.rotate(value=(2*math.pi/self.TOWER_COUNT * i), orient_axis='Z', orient_type='GLOBAL')
    
    def generateGates(self):
        print("start")
        x1 = self.x[0]
        y1 = self.y[0]
        for i in range(len(self.x)+1):
            x_value = math.sin(2*math.pi/self.TOWER_COUNT * (i + 0.5)) * self.RADIUS -1
            y_value = math.cos(2*math.pi/self.TOWER_COUNT * (i +0.5)) * self.RADIUS -1
            # if(i != len(self.x)):
            #     print(i)
            #     x_value = self.x[i+1]-self.x[i]
            #     y_value = self.y[i+1]-self.y[i]
            # else:
            #     print("10")
            #     x_value = self.x[0]-self.x[i]
            #     y_value = self.x[0]-self.x[i]
            gate_cube = bpy.ops.mesh.primitive_cube_add(location=(x_value, y_value, 0), scale=(self.WALL_WIDTH + 1, self.GATE_WIDTH, self.GATE_HEIGHT))
            bpy.ops.transform.rotate(value=(2*math.pi/self.TOWER_COUNT * i+math.pi/self.TOWER_COUNT) + 1.5708, orient_axis='Z', orient_type='GLOBAL')
            gate_cylinder = bpy.ops.mesh.primitive_cylinder_add(enter_editmode=False, align='WORLD', location=(x_value, y_value, self.GATE_HEIGHT), scale=(1, self.GATE_WIDTH, self.WALL_WIDTH + 1))
            bpy.ops.transform.rotate(value=1.5708, orient_axis='Y', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, True, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
            bpy.ops.transform.rotate(value=(2*math.pi/self.TOWER_COUNT * i+math.pi/self.TOWER_COUNT) + 1.5708, orient_axis='Z', orient_type='GLOBAL')
##generiert Stadtmauer
    def generate_wall(self):
        bpy.ops.mesh.primitive_cylinder_add(vertices=self.TOWER_COUNT, radius=self.RADIUS, depth=self.wall_height, location=(0, 0, self.wall_height/2))


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
        bpy.ops.mesh.primitive_cylinder_add(vertices=self.TOWER_COUNT, radius=self.INNER_RADIUS, depth=self.wall_height, location=(0, 0, self.wall_height/2))
        bpy.context.object.display_type = 'WIRE'

        cube_context = bpy.context.object          
        boolean_mod = cube_contextBigC.modifiers.new("boolean", "BOOLEAN")
        boolean_mod.object = cube_context
        ##bpy.context.object.modifiers["boolean"].operation = 'DIFFERENCE'
        #bpy.ops.object.modifier_apply(apply_as='DATA', modifier="boolean")

        bpy.ops.mesh.primitive_cylinder_add(vertices=self.TOWER_COUNT, radius=self.RADIUS + self.RADIUS*0.01, depth=self.wall_height*0.02, location=(0, 0, self.wall_height))
        
        mat_wall_top = bpy.data.materials.new("material_wall_top")
        mat_wall_top.use_nodes = True
        mat_wall_top.node_tree.nodes["Principled BSDF"].inputs[0].default_value = [0.047, 0.055, 0.078, 1.0]
        bpy.context.object.data.materials.append(mat_wall_top) 
        
        cylinder_top = bpy.context.object 
        bpy.ops.mesh.primitive_cylinder_add(vertices=self.TOWER_COUNT, radius=self.INNER_RADIUS, depth=self.wall_height*0.02, location=(0, 0, self.wall_height))
        bpy.context.object.display_type = 'WIRE'
        cylinder_top_inner = bpy.context.object
        boolean_cylinder_top = cylinder_top.modifiers.new("booleantop", "BOOLEAN")
        boolean_cylinder_top.object = cylinder_top_inner
        
        self.generateGates()
        #door calc
           
    

bpy.ops.object.select_all(action='SELECT') # selektiert alle Objekte
bpy.ops.object.delete(use_global=False, confirm=False) # löscht selektierte objekte
bpy.ops.outliner.orphans_purge() # löscht überbleibende Meshdaten etc.


cw = cityWall()
cw.generate_towers()
cw.generate_wall()

#Spawnen von gescaltem Cube und Zylinder

#Platzieren von Objekten an richtiger Location

#Einfach Code kopieren von Turmplatzierung (bzw dort reinkopieren)
#Da dann Abstandsberechnung für Position und halben Winkelabstand für Rotation
