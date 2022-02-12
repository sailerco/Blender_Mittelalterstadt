import typing
import bpy

class church():
    
    ##veränderbare Parameter
    basic_plane_width: int = 6
    church_base_location = [0,0,0]
    
    ##fest berechnete Parameter
    church_base_width: float = basic_plane_width*0.4
    church_base_length: float = basic_plane_width*0.6
    church_base_height: float = church_base_width*0.6
    tower_width: float = church_base_width * 0.33
    
    ##color material
    def create_material(self, color) -> bpy.types.Material:
        material: bpy.types.Material = bpy.data.materials.new("Material")
        material.use_nodes = True
        nodes_material: typing.List[bpy.types.Node] = material.node_tree.nodes
        nodes_material["Principled BSDF"].inputs[0].default_value = color

        return material

##Fenster

    ## Fenster Kernteil der Kirche
    def generate_base_windows(self, start_location):
        window_location= start_location
        for i in range(4):
            bpy.ops.mesh.primitive_cube_add(location=window_location, scale=(self.church_base_width*1.02, self.church_base_length*0.065, self.church_base_height*0.5))
            window_location= (window_location[0], window_location[1]-(self.church_base_length*0.4), window_location[2])
            bpy.context.object.data.materials.append(self.create_material([0.1, 0.05, 0.04, 1.000000]))
        
    ## runde Fenster im Dachspitz
    def generate_windows(self):
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, location=(self.church_base_location[0], self.church_base_location[1] + (self.church_base_length *0.93), self.church_base_height*4.2), scale=(self.church_base_width * 0.3,self.church_base_length * 0.05, self.church_base_width * 0.3))
        bpy.context.object.data.materials.append(self.create_material([0.5529, 0.7882, 0.9608, 1.000000]))
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, location=(self.church_base_location[0], self.church_base_location[1] + (-self.church_base_length *0.93), self.church_base_height*4.2), scale=(self.church_base_width * 0.3,self.church_base_length * 0.05, self.church_base_width * 0.3))
        bpy.context.object.data.materials.append(self.create_material([0.5529, 0.7882, 0.9608, 1.000000]))
    
    ## Fenster in den Türmen
    def generate_tower_windows(self, location):
        bpy.ops.mesh.primitive_cube_add(location=location, scale=(self.tower_width*0.2, self.tower_width*1.03, self.church_base_height*0.45))
        bpy.context.object.data.materials.append(self.create_material([0.1, 0.05, 0.04, 1.000000]))
        bpy.ops.mesh.primitive_cube_add(location=location, scale=(self.tower_width*1.03, self.tower_width*0.2, self.church_base_height*0.45))
        bpy.context.object.data.materials.append(self.create_material([0.1, 0.05, 0.04, 1.000000]))

##Extras

    ## Kirchentür & Treppe
    def generate_entrance(self):
        bpy.ops.mesh.primitive_cube_add(location=(self.church_base_location[0], self.church_base_location[1] + (self.church_base_length), self.church_base_height * 0.8), scale=(self.church_base_width * 0.2, self.church_base_width * 0.03, self.church_base_height*0.5))
        bpy.context.object.data.materials.append(self.create_material([0.2235, 0.1686, 0.1059, 1.000000]))
        bpy.ops.mesh.primitive_cylinder_add(vertices=20, location=(self.church_base_location[0], self.church_base_location[1] + (self.church_base_length * 0.995), self.church_base_height * 1.3), scale=(self.church_base_width * 0.2, self.church_base_width * 0.12, self.church_base_width * 0.03))
        bpy.context.object.rotation_euler[0] = 1.5708
        bpy.context.object.data.materials.append(self.create_material([0.2667, 0.1608, 0.1412, 1.000000]))
        bpy.ops.mesh.primitive_cube_add(location=(self.church_base_location[0], self.church_base_location[1] + (self.church_base_length), self.church_base_height*0.15), scale=(self.church_base_width * 0.3, self.church_base_width * 0.2, self.church_base_height*0.15))
        bpy.context.object.data.materials.append(self.create_material([0.2667, 0.1608, 0.1412, 1.000000]))
        bpy.ops.mesh.primitive_cube_add(location=(self.church_base_location[0], self.church_base_location[1] + (self.church_base_length), self.church_base_height*0.15), scale=(self.church_base_width * 0.4, self.church_base_width * 0.35, self.church_base_height*0.05))
        bpy.context.object.data.materials.append(self.create_material([0.2667, 0.1608, 0.1412, 1.000000]))    

## Grundmauern

    ## Kernteil der Kirche
    def generate_church_base(self):
        ##Stockwerk 1
         bpy.ops.mesh.primitive_cube_add(location=(self.church_base_location[0], self.church_base_location[1], self.church_base_height), scale=(self.church_base_width, self.church_base_length, self.church_base_height))
         bpy.context.object.data.materials.append(self.create_material([0.4431, 0.2353, 0.1961, 1.000000]))

         ##Stockwerk 1 Fenster
         window_start_location= (self.church_base_location[0], self.church_base_location[1]+(self.church_base_length*0.45), self.church_base_height)
         self.generate_base_windows(window_start_location)
         
         ##Zwischenstück 1
         bpy.ops.mesh.primitive_cube_add(location=(self.church_base_location[0], self.church_base_location[1], self.church_base_height*2), scale=(self.church_base_width * 1.05, self.church_base_length * 1.05, self.church_base_height * 0.1))
         bpy.context.object.data.materials.append(self.create_material([0.2667, 0.1608, 0.1412, 1.000000]))
         
         ##Stockwerk 2
         bpy.ops.mesh.primitive_cube_add(location=(self.church_base_location[0], self.church_base_location[1], self.church_base_height*2.7), scale=(self.church_base_width, self.church_base_length, self.church_base_height * 0.8))
         bpy.context.object.data.materials.append(self.create_material([0.4431, 0.2353, 0.1961, 1.000000]))
         
         ##Stockwerk 2 Fenster
         window_start_location= (self.church_base_location[0], self.church_base_location[1]+(self.church_base_length*0.45), self.church_base_height*2.7)
         self.generate_base_windows(window_start_location)

         ##Zwischenstück 2
         bpy.ops.mesh.primitive_cube_add(location=(self.church_base_location[0], self.church_base_location[1], self.church_base_height*3.5), scale=(self.church_base_width * 1.05, self.church_base_length * 1.05, self.church_base_height * 0.1))
         bpy.context.object.data.materials.append(self.create_material([0.2667, 0.1608, 0.1412, 1.000000]))
         
         ##Dach
         bpy.ops.mesh.primitive_cylinder_add(vertices = 3, location=(self.church_base_location[0], self.church_base_location[1], self.church_base_height*4), scale=(self.church_base_width * 1.1, self.church_base_height, self.church_base_length * 0.9))
         bpy.context.object.rotation_euler[0] = 1.5708
         bpy.context.object.data.materials.append(self.create_material([0.103312, 0.236954, 0.177671, 1.000000]))
         bpy.ops.mesh.primitive_cylinder_add(vertices = 3, location=(self.church_base_location[0], self.church_base_location[1] + (self.church_base_length * 0.9), self.church_base_height*4.2), scale=(self.church_base_width * 1.2, self.church_base_height * 1.2, self.church_base_length * 0.05))
         bpy.context.object.rotation_euler[0] = 1.5708
         bpy.context.object.data.materials.append(self.create_material([0.4431, 0.2353, 0.1961, 1.000000]))
         bpy.ops.mesh.primitive_cylinder_add(vertices = 3, location=(self.church_base_location[0], self.church_base_location[1] + (-self.church_base_length * 0.9), self.church_base_height*4.2), scale=(self.church_base_width * 1.2, self.church_base_height * 1.2, self.church_base_length * 0.05))
         bpy.context.object.rotation_euler[0] = 1.5708
         bpy.context.object.data.materials.append(self.create_material([0.4431, 0.2353, 0.1961, 1.000000]))
         
    

##Türme

    ## einzelner Turm
    def generate_single_tower(self, tower_start_location):
        tower_location = tower_start_location 
        for i in range(3):
            bpy.ops.mesh.primitive_cube_add(location=tower_location, scale=(self.tower_width, self.tower_width, self.church_base_height))
            bpy.context.object.data.materials.append(self.create_material([0.4431, 0.2353, 0.1961, 1.000000]))
            bpy.ops.mesh.primitive_cube_add(location=(tower_location[0], tower_location[1], tower_location[2] + self.church_base_height), scale=(self.tower_width * 1.1, self.tower_width * 1.1, self.church_base_height * 0.1))
            bpy.context.object.data.materials.append(self.create_material([0.2667, 0.1608, 0.1412, 1.000000]))

            ##tower windows
            self.generate_tower_windows(tower_location)

            tower_location = (tower_location[0], tower_location[1], tower_location[2] + self.church_base_height * 2)
        bpy.ops.mesh.primitive_cone_add(vertices=4, location=tower_location, scale=(self.tower_width * 1.5, self.tower_width * 1.5, self.tower_width * 2))
        bpy.context.object.rotation_euler[2] = 0.785398
        bpy.context.object.data.materials.append(self.create_material([0.103312, 0.236954, 0.177671, 1.000000]))


    ## alle Türme
    def generate_towers(self):
    ##tower one
        tower_location_one = (self.church_base_location[0] + (self.church_base_width * 1.1 - self.tower_width), self.church_base_location[1] + (self.church_base_length * 1.1 - self.tower_width), self.church_base_height)
        self.generate_single_tower(tower_location_one)
        
    ##tower two
        tower_location_two = (self.church_base_location[0] + (-self.church_base_width * 1.1 + self.tower_width), self.church_base_location[1] + (self.church_base_length * 1.1 - self.tower_width), self.church_base_height)
        self.generate_single_tower(tower_location_two)

    def generate_church(self):
        self.generate_church_base()
        self.generate_entrance()
        self.generate_towers()
        self.generate_windows()
