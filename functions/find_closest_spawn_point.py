import carla

def find_closest_spawn_point(world, target_location, vehicle_spawn_points):
    """
    Finds the closest vehicle spawn point to a given target location.
    Args:
        world: The CARLA world object.
        target_location: A carla.Location object representing the target location.
        vehicle_spawn_points: A list of carla.Transform objects representing vehicle spawn points.
    Returns:
        closest_spawn_point: The carla.Transform of the closest spawn point.
        closest_spawn_number: The index of the closest spawn point in the vehicle_spawn_points list.
    """

    closest_spawn_point = None
    min_distance_sq = float('inf')

    # Iterate through each spawn point to find the closest one
    for i, spawn_point in enumerate(vehicle_spawn_points):
        # Calculate the squared distance to avoid a computationally expensive square root
        distance_sq = (spawn_point.location.x - target_location.x)**2 + \
                      (spawn_point.location.y - target_location.y)**2 + \
                      (spawn_point.location.z - target_location.z)**2

        # If this spawn point is closer, update the closest one
        if distance_sq < min_distance_sq:
            min_distance_sq = distance_sq
            closest_spawn_point = spawn_point
            closest_spawn_number = i 

    return closest_spawn_point, closest_spawn_number