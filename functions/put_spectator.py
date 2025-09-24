import carla

def put_spectator(location):
    """
    Puts the spectator in the location given to starting point of the vehicle
    Args:
        location: Transform of the vehicle
    Returns:
        Transform for the spectator
    """
    # Puts the spectator in the location given to starting point of the vehicle
    loc = carla.Location(x=location.location.x, y=location.location.y, z=location.location.z + 20)
    rot = carla.Rotation(pitch=location.rotation.pitch - 50, yaw=location.rotation.yaw, roll=location.rotation.roll)
    return carla.Transform(loc, rot)
