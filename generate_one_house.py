import bpy
import math
import random
# selektiert alle Objekte löscht selektierte objekte
print("delete")
# bpy.ops.object.select_all(action='SELECT')
# bpy.ops.object.delete(use_global=False, confirm=False)
# bpy.ops.outliner.orphans_purge()  # löscht überbleibende Meshdaten etc.
print("dddd")
filepath = "//Medival Assets/Medieval_houses_red.blend"
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

def generateHouse(obj):
    a = random.randint(0, 2)
    b = random.randint(0, 1)  # iwie noch die schilder adden
    print(a, b)
    print("hello")
    house = []
    for coll in obj:
        if(b == 0 and (a == 0 or a == 2) and coll.name.endswith("Sign")):  # niedriges schild
            house_part = coll.copy()
            link_to.objects.link(house_part)
            house.append(house_part)
        elif(b == 0 and a == 1 and coll.name.endswith("Sign_2")):  # hohes schild
            house_part = coll.copy()
            link_to.objects.link(house_part)
            house.append(house_part)
        elif(a == 0 and coll.name.endswith("_1")):  # basic haus
            house_part = coll.copy()
            link_to.objects.link(house_part)
            house.append(house_part)
        # wide-small, calc locations
        elif(a == 1 and (coll.name.endswith("_1") or coll.name.endswith("_bottom"))):
            house_part = coll.copy()
            if(coll.name.startswith("Main_House") or coll.name.startswith("Main_Chimney") or coll.name.startswith("Main_Roof_")):
                house_part.location.z = house_part.location.z + 0.599418*2
            if(coll.name.startswith("Main_Door")):
                house_part.location.y = 1.2717
            link_to.objects.link(house_part)
            house.append(house_part)
        elif(a == 2 and (coll.name.endswith("_1") or coll.name.endswith("_upper"))):  # small wide
            house_part = coll.copy()
            link_to.objects.link(house_part)
            house.append(house_part)
        elif(a == 3 and (coll.name.endswith("wood_house"))):  # wood
            house_part = coll.copy()
            link_to.objects.link(house_part)
            house.append(house_part)
    print("after for loop")
    if(len(house) > 0):
        print("if abfrage")
        ob = []
        for h in house:
            if(h.type == 'MESH'):
                print("true")
                ob.append(h)
        print("was geht?")
        ctx = bpy.context.copy()
        print("naa?")
        ctx['active_object'] = ob[0]
        print("yay")
        ctx['selected_editable_objects'] = ob
        print("damn")
        bpy.ops.object.join(ctx)
        print("yoooo")
        #link_to.objects.link(ctx)
generateHouse(data_to.objects)

#stürzt nur nicht ab wenn löschen auskommentiert ist, 2 mal run start geht nicht??
