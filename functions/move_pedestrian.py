import carla
import math
def move_pedestrian(pedestrian, vehicle, calc_distance, ped_distance, target_ped_x, target_ped_y, target_ped_z, vehicle_velocity):
    """
    ADD COMMENTS LATER
    """
    # moves pedestrian based on the distance to the ego vehicle
    ped_loc = pedestrian.get_location()
    distance = calc_distance(vehicle.get_location(), ped_loc)
    if distance < ped_distance:
        # Get the speed of the vehicle based on the velocity
        speed_m_s = math.sqrt(
            vehicle_velocity.x**2 + 
            vehicle_velocity.y**2 + 
            vehicle_velocity.z**2
        )
        # Make walker controller
        walker_control = carla.WalkerControl(
            direction=carla.Location(x= target_ped_x, y=target_ped_y, z=target_ped_z),
            speed= speed_m_s,
            jump=False 
        )
        pedestrian.apply_control(walker_control)