import carla
import os
import sys
import yaml
import json
# import all the functions in the functions directory
from functions import *


# Add the directory containing PCLA.py to the Python path
sys.path.append(os.path.dirname(os.path.abspath("/home/vortex/PCLA")))
current_dir = os.path.dirname(os.path.abspath(__file__))
yaml_file_path = os.path.join(current_dir, 'scenarios', 'dynamic_single_scenario.yaml')
json_file_path = os.path.join(current_dir, 'scenarios', 'single_evaluation.json')

from PCLA import PCLA

def main():

    client = carla.Client('localhost', 2000)
    client.set_timeout(10.0)

    # Load scenario configuration from YAML file
    with open(yaml_file_path, 'r') as file:
        config = yaml.safe_load(file)
    
    for key, value in config.items():
        globals()[key] = value


    client.load_world(town)

    try:
        # Initialize the client, get the world and set the weather
        traffic_manager, world, settings, synchronous_master = start_client(client)
        set_weather(world, sun_altitude_angle, sun_azimuth_angle)
        
        # Load the JSON data from a file
        with open(json_file_path, 'r') as f:
            evals = json.load(f)

        # For each agent name (e.g., 'if_if', 'simlingo_simlingo')
        for agent_name, agent_scenarios in evals.items():
            
            # The inner loop iterates through each scenario for the current agent
            for scenario_name, scenario_data in agent_scenarios.items():
                # Extract the variables for the current scenario
                sp_npcs, sp_peds, pedestrian_name = (scenario_data[k] for k in ("sp_npcs", "sp_peds", "pedestrian_name"))
                print_scenario_info(agent_name, scenario_name, sp_npcs, sp_peds, pedestrian_name)
                
                # Spawning the pedestrian
                bpLibrary = world.get_blueprint_library()
                pedestrian = None
                if sp_peds:
                    pedestrian = spawn_pedestrian(world, bpLibrary, pedestrian_name, ped_x, ped_y, ped_z, ped_pitch, ped_yaw, ped_roll)

                # Spawning the npc vehicles
                vehicle_spawn_points = world.get_map().get_spawn_points()
                npc_list = []
                if sp_npcs:
                    npc_list = spawn_npcs(world, bpLibrary, vehicle_spawn_points, npc_spawn_points, traffic_manager)

                # Setting up the route and spawning the ego vehicle
                start_loc , start_num = find_closest_spawn_point(world, carla.Location(x=start_x, y=start_y, z=start_z), vehicle_spawn_points)
                end_loc , end_num = find_closest_spawn_point(world, carla.Location(x=end_x, y=end_y, z=end_z), vehicle_spawn_points)
                vehicle = world.spawn_actor(bpLibrary.filter('model3')[0], start_loc) # Spawning the ego vehicle
                world.tick()

                # Set the spectator according to the vehicle's transform
                spectator = world.get_spectator()
                spectator.set_transform(put_spectator(vehicle.get_transform()))
                world.tick()

                # Set up PCLA
                make_route(client, start_num, end_num, vehicle_spawn_points, PCLA)
                route = "route.xml"
                pcla = PCLA.PCLA(agent_name, vehicle, route, client)

                dynamic = True
                # Run the vehicle until it reaches the destination
                while is_far_from(vehicle.get_location(), end_loc, max_distance=2.0):
                    if dynamic:
                        move_pedestrian(pedestrian, vehicle, calc_distance, ped_distance, target_ped_x, target_ped_y, target_ped_z, vehicle.get_velocity())
                    ego_action = pcla.get_action()
                    vehicle.apply_control(ego_action)
                    world.tick()
                
                # Clean up the actors and PCLA instance
                clean_up(npc_list, pedestrian, pcla)

    finally:
        # Restore the original settings
        settings.synchronous_mode = False
        world.apply_settings(settings)

        # Clean up in case of an error
        clean_up(npc_list, pedestrian, pcla)

if __name__ == '__main__':

    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        print('Done.')

