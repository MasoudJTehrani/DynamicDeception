def calc_distance(loc1, loc2):
    """
    Checks if two carla.Location objects are close to each other.
    Args:
        loc1 (carla.Location): The first location.
        loc2 (carla.Location): The second location.
    Returns:
        float: The distance between the two locations.
    """
    return loc1.distance(loc2)