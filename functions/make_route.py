
def make_route(client, start_loc, end_loc, vehicle_spawn_points, PCLA):
    """
    Function to create a route file for PCLA between two spawn points.
    Args:
        client: Carla client object
        start_loc: Index of the starting spawn point
        end_loc: Index of the ending spawn point
    """
    startLoc = vehicle_spawn_points[start_loc].location # Start location
    endLoc = vehicle_spawn_points[end_loc].location # End location
    waypoints = PCLA.location_to_waypoint(client, startLoc, endLoc)  # Returns waypoints between two locations
    PCLA.route_maker(waypoints, "route.xml")  # Returns waypoints usable for PCLA
