import carla
import math
def move_pedestrian(pedestrians, vehicle, calc_distance, ped_distance, move_ped_x, move_ped_y, move_ped_z, target_ped_x, target_ped_y, target_ped_z, vehicle_velocity):
    """
    ADD COMMENTS LATER
    """
    # moves pedestrian based on the distance to the ego vehicle
    ped_loc = pedestrians[0].get_location()
    distance = calc_distance(vehicle.get_location(), ped_loc)
    distance_to_target = calc_distance(ped_loc, carla.Location(x=target_ped_x, y=target_ped_y, z=target_ped_z))

    if (distance < ped_distance) and (distance_to_target > 0.6):
        # Get the speed of the vehicle based on the velocity
        speed_m_s = math.sqrt(
            vehicle_velocity.x**2 + 
            vehicle_velocity.y**2 + 
            vehicle_velocity.z**2
        )
        # Make walker controller
        walker_control = carla.WalkerControl(
            direction=carla.Location(x=move_ped_x, y=move_ped_y, z=move_ped_z),
            speed= speed_m_s,
            jump=False 
        )
        for ped in pedestrians:
            ped.apply_control(walker_control)
    else:
        # Stop the pedestrian when close to target or far from vehicle
        walker_control = carla.WalkerControl(
            direction=carla.Location(x=0, y=0, z=0),
            speed=0,
            jump=False 
        )
        for ped in pedestrians:
            ped.apply_control(walker_control)