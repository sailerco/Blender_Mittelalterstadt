import bpy
import math
import random
# selektiert alle Objekte löscht selektierte objekte
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False, confirm=False)
bpy.ops.outliner.orphans_purge()  # löscht überbleibende Meshdaten etc.

filepath = "//Medival Assets/Medieval_houses.blend"
coll_name = "Cube"
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

rad = 10
nr = 0
c = 1
TOWER_COUNT = 5
RADIUS = 50
for j in range(10):
    for i in range(TOWER_COUNT):
        x1 = math.sin(i/TOWER_COUNT * math.pi * 2) * rad * c
        y1 = math.cos(i/TOWER_COUNT * math.pi * 2) * rad * c
        x2 = math.sin((i+1)/TOWER_COUNT * math.pi * 2) * rad * c
        y2 = math.cos((i+1)/TOWER_COUNT * math.pi * 2) * rad * c
        #steigung
        a = math.sqrt(pow(x2-x1, 2) + pow(y2-y1,2))
        x3 = x1 - x2
        y3 = y1 - y2
        xy = a
        count = 0
        print("x3")
        print(x3)
        for p in range(i):
            #random haus
            a = random.randint(0,10)
            obj = data_to.objects[a]
            obj1 = obj.copy()
            obj1.name = obj1.name + "_" + str(nr)
            link_to.objects.link(obj1)
            x = x1 + xy*p
            y = y1 + xy*p
            print("x y")
            print(x,y)
            angle = math.radians(random.randint(0,359))
            obj1.location.x = x
            obj1.location.y = y
            obj1.rotation_euler[2] = angle
            nr += 1
            count += 1
    c += 0.5