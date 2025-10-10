def is_far_from(loc1, loc2, max_distance=2.0):
    """
    Checks if two carla.Location objects are close to each other.
    Args:
        loc1 (carla.Location): The first location.
        loc2 (carla.Location): The second location.
        max_distance (float): The maximum distance to consider them "not far".
    Returns:
        bool: True if the locations are farther apart than max_distance, False otherwise.
    """
    # The carla.Location.distance() method calculates the Euclidean distance
    distance = loc1.distance(loc2.location)
    return distance > max_distance