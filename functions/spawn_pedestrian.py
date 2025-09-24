import carla

def spawn_pedestrian(spawn_pedestrian, world, bpLibrary):
    """
    Spawns a pedestrian at a predefined location in the CARLA world.
    Args:
        spawn_pedestrian (bool): Flag to determine whether to spawn the pedestrian.
        world (carla.World): The CARLA world instance where the pedestrian will be spawned.
        bpLibrary (carla.BlueprintLibrary): The blueprint library to fetch pedestrian blueprints.
    Returns:
        carla.Actor or None: The spawned pedestrian actor or None if not spawned.
    """
    if spawn_pedestrian:
        pedestrian_bp = bpLibrary.filter('walker.pedestrian.0062')[0]
        ped_spawn_point = carla.Transform()
        ped_spawn_point.location = carla.Location(x=5.5, y=55.5, z=1.5)
        ped_spawn_point.rotation = carla.Rotation(pitch=0, yaw=180, roll=0)
        pedestrian = world.try_spawn_actor(pedestrian_bp, ped_spawn_point)
        world.tick()
        return pedestrian
