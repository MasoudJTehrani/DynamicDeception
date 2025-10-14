import carla

def spawn_pedestrian(world, bpLibrary, pedestrian_names, x, y, z, pitch, yaw, roll, sec_ped_distance_x, sec_ped_distance_y):
    """
    Spawns pedestrians at a predefined location in the CARLA world.
    Args:
        world (carla.World): The CARLA world instance where the pedestrian will be spawned.
        bpLibrary (carla.BlueprintLibrary): The blueprint library to fetch pedestrian blueprints.
        ped_spawn_point (carla.Transform): The transform (location and rotation) where the pedestrian will be spawned.
        pedestrian_names (str): The names of the pedestrians blueprint to use.
        x, y, z (float): coordinates for the spawn location.
        pitch, yaw, roll (float): rotation angles for the spawn orientation.
    Returns:
        carla.Actor or None: The spawned pedestrians actor or None if not spawned.
    """
    pedestrian_bp = []
    for name in pedestrian_names:
        pedestrian_bp.append(bpLibrary.filter(name)[0])
    ped_spawn_points = [
        carla.Transform(
            carla.Location(x=x, y=y, z=z),
            carla.Rotation(pitch=pitch, yaw=yaw, roll=roll)
        ), 
        carla.Transform(
            carla.Location(x=x + + sec_ped_distance_x, y= y + sec_ped_distance_y, z=z),
            carla.Rotation(pitch=pitch, yaw=yaw, roll=roll)
        )
    ]

    pedestrians = []

    for bp, sp_point in zip(pedestrian_bp, ped_spawn_points):
        pedestrians.append(world.try_spawn_actor(bp, sp_point))

    world.tick()
    return pedestrians
