import bpy
import bmesh


def calc_object_area(object):
    """Total mesh area, taking in account object scale and modifiers."""
    bm = bmesh.new()
    bm.from_object(object, bpy.context.scene)
    bm.transform(object.matrix_world)
    area = sum(f.calc_area() for f in bm.faces)
    bm.free()
    return area


def set_particle_density(object, system_name, density):
    """Set particle count for the given system, according to density."""
    # access the particle system
    system = object.particle_systems.get(system_name)
    if system is None:
        return
    # set particle count according to density
    area = calc_object_area(object)
    system.settings.count = int(area * density)


def set_particle_density_on_selection(system_name, density):
    """Set particle density on current object selection."""
    for o in bpy.context.selected_objects:
        set_particle_density(o, system_name, density)


def get_particle_system_names_enum(scene, context):
    """Enum callback for the particle systems names."""
    items = set()
    for o in context.selected_objects:
        for p in o.particle_systems:
            items.add((p.name, p.name, ""))
    return list(items)


class SetParticleDensityOperator(bpy.types.Operator):
    """Set particle density on specified system of selected objects."""
    bl_idname = "cube.set_particle_systems_density"
    bl_label = "Set particle system density"
    bl_options = {"REGISTER", "UNDO"}

    density = bpy.props.FloatProperty(name="Density",
                                      description="Particle density",
                                      default=10)

    system_name = bpy.props.EnumProperty(name="Systems name",
                                         description="Name of the particle system slot to be affected",
                                         items=get_particle_system_names_enum)

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        set_particle_density_on_selection(self.system_name, self.density)
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)


class SetParticleDensityPanel(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_label = "Particle density"
    bl_category = "Cube"

    def draw(self, context):
        self.layout.operator("cube.set_particle_systems_density")
