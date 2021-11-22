import bpy
import random
import math


bpy.ops.object.select_all(action='SELECT') # selektiert alle Objekte
bpy.ops.object.delete(use_global=False, confirm=False) # löscht selektierte objekte
bpy.ops.outliner.orphans_purge() # löscht überbleibende Meshdaten etc.

bpy.ops.mesh.primitive_cube_add(size=1, location=(0,0,0), scale=(1,1,1))
