import bpy
import math
import random
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
    data_to.objects = [name for name in data_from.objects if name.startswith(coll_name)]
try:
    link_to = scene.collection.children[link_to_name]
except KeyError:
    link_to = bpy.data.collections.new(link_to_name)
    scene.collection.children.link(link_to)

num = 10
rad = 15
nr = 0
c = 1
def generateHouse(obj):
    a = 1 #random.randint(0,2)
    house = []
    for coll in obj:
        if(a == 0 and coll.name.endswith("_1")):
            house_part = coll.copy()
            link_to.objects.link(house_part)
            house.append(house_part)
        elif(a==1 and (coll.name.endswith("_1") or coll.name.endswith("_bottom"))):
            house_part = coll.copy()
            if(coll.name.startswith("Main_House") or coll.name.startswith("Main_Chimney") or coll.name.startswith("Main_Roof_")):
                house_part.location.z = house_part.location.z + 0.599418*2
            link_to.objects.link(house_part)
            house.append(house_part)
        elif(a==2 and (coll.name.endswith("_1") or coll.name.endswith("_upper"))):
            print("wow")
    for i in house:
        i.select_set(True)
        #bpy.context.view_layer.objects.active = i
    bpy.ops.object.join()
generateHouse(data_to.objects)