import bpy
from .set_particle_density import *


bl_info = {
    "name": "Particle system density",
    "description": "Set particle count on named systems across multiple \
                    objects, with a given density",
    "version": (0, 0, 1),
    "category": "Particles"
}


def register():
    bpy.utils.register_class(SetParticleDensityOperator)
    bpy.utils.register_class(SetParticleDensityPanel)


def unregister():
    bpy.utils.unregister_class(SetParticleDensityOperator)
    bpy.utils.unregister_class(SetParticleDensityPanel)
