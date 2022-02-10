import bpy
import math
import random
from mathutils import Matrix

class generate_house_circle:
    # # https://blender.stackexchange.com/questions/34540/how-to-link-append-a-data-block-using-the-python-api?noredirect=1&lq=1
    filepath = "//Medival Assets/Medieval_houses_red.blend"
    coll_name = "Main_"
    link = False
    link_to_name = "Environment"

    def generateAssets(self):
        with bpy.data.libraries.load(self.filepath, link=self.link) as (data_from, data_to):
            data_to.objects = [
                name for name in data_from.objects if name.startswith(self.coll_name)]
        return data_to.objects

    def generateCollection(self):
        try:
            link_to = bpy.context.scene.collection.children[self.link_to_name]
        except KeyError:
            link_to = bpy.data.collections.new(self.link_to_name)
            bpy.context.scene.collection.children.link(link_to)
        return link_to
    
    def generateHouse(self, x, y, angle, assets):
        link_to = self.generateCollection()
        offset = random.randint(-1, 1)*0.3
        a = random.randint(0, 3)
        b = random.randint(0, 2) 
        house = []
        for coll in assets:
            content = True
            if (b == 0 and (a == 0 or a == 2) and coll.name.endswith("Sign")):
                house_part = coll.copy()
            elif(b == 0 and a == 1 and coll.name.endswith("Sign_2")):
                house_part = coll.copy()
            elif(a == 0 and coll.name.endswith("_1")):
                house_part = coll.copy()
            elif(a == 2 and (coll.name.endswith("_1") or coll.name.endswith("_upper"))):
                house_part = coll.copy()
            elif(a == 3 and (coll.name.endswith("wood_house"))):
                house_part = coll.copy()
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

    def generate(self, tower_count, radius, is_round, wall_thickness):
        #r⋅cos α2=r⋅cos 180°n
        if(is_round == False):
            alpha_halbe = math.pi / tower_count
            inner_radius = radius * math.cos(alpha_halbe)
            radius = inner_radius 
        assets = self.generateAssets()
        add_radius = 1
        house_number_per_circle = 5 
        rad = 15
        rows = round(((radius - wall_thickness - 3)/rad)) #3 = half house
        #r = radius % rad
        # if(radius > 75):
        #     extra_rows = round((radius-75)/10)
        #     rows += extra_rows
        for j in range(rows):
            for i in range(house_number_per_circle):
                angle = math.radians(random.randint(0,359))
                #fügt Häuser an Ecken ein bei wenig Ecken
                if tower_count < 8 and j == rows-1 and is_round == False and radius < 75:
                    for z in range(tower_count):
                        x = math.sin(math.pi * 2/tower_count*(z)) * rad * add_radius
                        y = math.cos(math.pi * 2/tower_count*(z)) * rad * add_radius
                        self.generateHouse(x, y, angle, assets)
                    break
                else:
                    x = math.sin(i/house_number_per_circle * math.pi * 2) * rad * add_radius
                    y = math.cos(i/house_number_per_circle * math.pi * 2) * rad * add_radius
                    self.generateHouse(x, y, angle, assets)
            add_radius += 1
            house_number_per_circle = house_number_per_circle + 5

# mehrfaches ausführen funktioniert