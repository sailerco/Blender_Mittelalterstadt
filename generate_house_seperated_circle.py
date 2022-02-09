import bpy
import math
import random
from mathutils import Matrix
# selektiert alle Objekte löscht selektierte objekte
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False, confirm=False)
bpy.ops.outliner.orphans_purge()  # löscht überbleibende Meshdaten etc.

filepath = "//Medival Assets/Medieval_houses-Kopie.blend"
coll_name = "Main_"
link = False
scene = bpy.context.scene
link_to_name = "Environment"
# https://blender.stackexchange.com/questions/34540/how-to-link-append-a-data-block-using-the-python-api?noredirect=1&lq=1

with bpy.data.libraries.load(filepath, link=link) as (data_from, data_to):
    data_to.objects = [
        name for name in data_from.objects if name.startswith(coll_name)]
try:
    link_to = scene.collection.children[link_to_name]
except KeyError:
    link_to = bpy.data.collections.new(link_to_name)
    scene.collection.children.link(link_to)

def generateHouse(obj, x, y, angle):
    a = random.randint(0, 2)
    b = random.randint(0, 1)  # iwie noch die schilder adden
    house = []
    for coll in obj:
        content = True
        if(b == 0 and (a == 0 or a == 2) and coll.name.endswith("Sign")):  # niedriges schild
            house_part = coll.copy()
            house.append(house_part)
        elif(b == 0 and a == 1 and coll.name.endswith("Sign_2")):  # hohes schild
            house_part = coll.copy()
            house.append(house_part)
        elif(a == 0 and coll.name.endswith("_1")):  # basic haus
            house_part = coll.copy()
            house.append(house_part)
        # wide-small, calc locations
        elif(a == 1 and (coll.name.endswith("_1") or coll.name.endswith("_bottom"))):
            house_part = coll.copy()
            if(coll.name.startswith("Main_House") or coll.name.startswith("Main_Chimney") or coll.name.startswith("Main_Roof_")):
                house_part.location.z = house_part.location.z + 1.36723
            if(coll.name.startswith("Main_Doo")):
                house_part.location.y = house_part.location.y - 0.3
            house.append(house_part)
        elif(a == 2 and (coll.name.endswith("_1") or coll.name.endswith("_upper"))):  # small wide
            house_part = coll.copy()
            house.append(house_part)
        elif(a == 3 and (coll.name.endswith("wood_house"))):  # wood
            house_part = coll.copy()
            house.append(house_part)
        else:
            content = False
        if(content == True):
            link_to.objects.link(house_part)
            house_part.location.x += x
            house_part.location.y += y
    for i in house:
        x1 = i.location.x
        y1 = i.location.y
        i.location.x = 0
        i.location.y = 0
        i.rotation_euler[2] = angle
        i.location.x = x
        i.location.y = y
        i.select_set(True)
    #bpy.ops.transform.rotate(value=angle,  axis=(0, 0, 1))  
num = 1
rad = 15
nr = 0
c = 1
for j in range(10):
    for i in range(num):
        x = math.sin(i/num * math.pi * 2) * rad * c
        y = math.cos(i/num * math.pi * 2) * rad * c
        angle = math.radians(random.randint(0,359))
        generateHouse(data_to.objects, x, y, angle)
        nr += 1
    c += 0.5
    num = num + 5
print("done")
#generateHouse(data_to.objects)

# mehrfaches ausführen funktioniert