import bpy
import math


class cityWall():

    TOWER_COUNT = 10
    RADIUS = 30

    tower_height = 12
    tower_radius = 2
    wall_thickness = 0.5

    roof_height = 4
    roof_overhang = 0.5

    texture_scale = 20

    wall_height = 8
    wall_thickness=tower_radius-0.5
    INNER_RADIUS = RADIUS - wall_thickness
    
   


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
            tower_location=((math.sin(2*math.pi/self.TOWER_COUNT * i) * self.RADIUS, math.cos(2*math.pi/self.TOWER_COUNT * i) * self.RADIUS, self.tower_height/2))
            self.generate_base(tower_location, self.tower_height)

            t = bpy.context.object
    
            bpy.ops.transform.rotate(value=(2*math.pi/self.TOWER_COUNT * i), orient_axis='Z', orient_type='GLOBAL')
    
    
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
      
        


bpy.ops.object.select_all(action='SELECT') # selektiert alle Objekte
bpy.ops.object.delete(use_global=False, confirm=False) # löscht selektierte objekte
bpy.ops.outliner.orphans_purge() # löscht überbleibende Meshdaten etc.


cw = cityWall()
cw.generate_towers()
cw.generate_wall()
