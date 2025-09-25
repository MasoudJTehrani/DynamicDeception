import carla

def spawn_pedestrian(world, bpLibrary, ped_spawn_point, pedestrian_name, x, y, z, pitch, yaw, roll):
    """
    Spawns a pedestrian at a predefined location in the CARLA world.
    Args:
        world (carla.World): The CARLA world instance where the pedestrian will be spawned.
        bpLibrary (carla.BlueprintLibrary): The blueprint library to fetch pedestrian blueprints.
        ped_spawn_point (carla.Transform): The transform (location and rotation) where the pedestrian will be spawned.
        pedestrian_name (str): The name of the pedestrian blueprint to use.
        x, y, z (float): coordinates for the spawn location.
        pitch, yaw, roll (float): rotation angles for the spawn orientation.
    Returns:
        carla.Actor or None: The spawned pedestrian actor or None if not spawned.
    """
    pedestrian_bp = bpLibrary.filter(pedestrian_name)[0]
    ped_spawn_point = carla.Transform(
        carla.Location(x=x, y=y, z=z),
        carla.Rotation(pitch=pitch, yaw=yaw, roll=roll)
    )
    pedestrian = world.try_spawn_actor(pedestrian_bp, ped_spawn_point)
    world.tick()
    return pedestrian
