import bpy
import math
import random

from generate_house_circle import generateHouse
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
for j in range(10):
    for i in range(num):
        obj = generateHouse(data_to.objects)
        obj1 = obj.copy()
        obj1.name = obj1.name + "_" + str(nr)
        link_to.objects.link(obj1)
        x = math.sin(i/num * math.pi * 2) * rad * c
        y = math.cos(i/num * math.pi * 2) * rad * c
        angle = math.radians(random.randint(0,359))
        obj1.location.x = x
        obj1.location.y = y
        obj1.rotation_euler[2] = angle
        nr += 1
    c += 0.5
    num = num + 5