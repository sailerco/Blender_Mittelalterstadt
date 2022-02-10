import bpy
import math

class floor():

    TOWER_COUNT = 10
    RADIUS = 50
    kreis = False
    if(kreis):
        wall_vertices = 32
    else:
        wall_vertices = TOWER_COUNT
    

    def generate_floor(self):
        bpy.ops.mesh.primitive_cylinder_add(vertices=self.wall_vertices, radius=self.RADIUS, depth=0.01, location=(0, 0, 0))

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


#bpy.ops.object.select_all(action='SELECT') # selektiert alle Objekte
#bpy.ops.object.delete(use_global=False, confirm=False) # löscht selektierte objekte
#bpy.ops.outliner.orphans_purge() # löscht überbleibende Meshdaten etc.


f = floor()
f.generate_floor()

