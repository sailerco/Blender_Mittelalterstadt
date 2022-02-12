import bpy
import math

class well:
    filepath = "/medival_assets/well_normalSized.blend"
    coll_name = "Main_"
    link = False
    link_to_name = "Well"

    def generateWell(self):
        #Start Code von: https://blender.stackexchange.com/questions/34540/how-to-link-append-a-data-block-using-the-python-api?noredirect=1&lq=1
        with bpy.data.libraries.load(self.filepath, link=self.link) as (data_from, data_to):
            data_to.objects = [name for name in data_from.objects if name.startswith(self.coll_name)]
        try:
            link_to = bpy.context.scene.collection.children[self.link_to_name]
        except KeyError:
            link_to = bpy.data.collections.new(self.link_to_name)
            bpy.context.scene.collection.children.link(link_to)
        #Ende Code von: Blender.stackexchange.com 

        well_data = data_to.objects[0]
        well = well_data.copy()
        well.name = well.name
        well.location.y = 8
        well.rotation_euler[2] = math.pi/2
        link_to.objects.link(well)