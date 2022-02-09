import bpy
import math
import random
from mathutils import Matrix
# selektiert alle Objekte löscht selektierte objekte
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False, confirm=False)
bpy.ops.outliner.orphans_purge()  # löscht überbleibende Meshdaten etc.

# https://blender.stackexchange.com/questions/34540/how-to-link-append-a-data-block-using-the-python-api?noredirect=1&lq=1
filepath = "//Medival Assets/Medieval_houses_red.blend"
coll_name = "Main_"
link = False
scene = bpy.context.scene
link_to_name = "Environment"

with bpy.data.libraries.load(filepath, link=link) as (data_from, data_to):
    data_to.objects = [
        name for name in data_from.objects if name.startswith(coll_name)]
try:
    link_to = scene.collection.children[link_to_name]
except KeyError:
    link_to = bpy.data.collections.new(link_to_name)
    scene.collection.children.link(link_to)

def generateHouse(obj, x, y, angle):
    offset = random.randint(-1, 1)
    offset = offset*0.3
    a = random.randint(0, 3)
    b = random.randint(0, 2)  # iwie noch die schilder adden
    house = []
    for coll in obj:
        content = True
        #sorry
        if (b == 0 and (a == 0 or a == 2) and coll.name.endswith("Sign")) or (b == 0 and a == 1 and coll.name.endswith("Sign_2")) or (a == 0 and coll.name.endswith("_1")) or (a == 2 and (coll.name.endswith("_1") or coll.name.endswith("_upper")) or (a == 3 and (coll.name.endswith("wood_house")))):
            house_part = coll.copy()
        # wide-small, calc locations
        elif a == 1 and (coll.name.endswith("_1") or coll.name.endswith("_bottom")):
            house_part = coll.copy()
            if(coll.name.startswith("Main_House") or coll.name.startswith("Main_Chimney") or coll.name.startswith("Main_Roof_")):
                house_part.location.z = house_part.location.z + 1.36723
            if(coll.name.startswith("Main_Door")):
                house_part.location.y = house_part.location.y - 0.3
        else:
            content = False

        if content == True:
            house.append(house_part)
            link_to.objects.link(house_part)
            house_part.location.x += x + offset
            house_part.location.y += y + offset
            house_part.rotation_euler[2] = angle

    for i in house:
        i.select_set(True)

def generate():
    nr = 0
    c = 1
    num = 10 # how many houses
    rad = 12 # rad pro kreis
    totalRadius = 100
    towers = 4
    rows = int((totalRadius/rad))
    for j in range(rows):
        for i in range(num):
            x = math.sin(i/num * math.pi * 2) * rad * c
            y = math.cos(i/num * math.pi * 2) * rad * c
            angle = math.radians(random.randint(0,359))
            generateHouse(data_to.objects, x, y, angle)
            nr += 1
        c += 0.5
        num = num + 5
    # #code to add another house
    # for z in range(towers):
    #     print("hi")
    #     x = math.sin(math.pi * 2/towers*(z)) * rad * c
    #     y = math.cos(math.pi * 2/towers*(z)) * rad * c
    #     angle = math.radians(random.randint(0,359))
    #     generateHouse(data_to.objects, x, y, angle)
        
generate()
print("done")

# mehrfaches ausführen funktioniert