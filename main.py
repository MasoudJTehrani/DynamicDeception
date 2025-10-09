# import all the functions in the functions directory
from functions import *

# Add the directory containing PCLA.py to the Python path

# -------------------------- Change this to your PCLA directory --------------------------
sys.path.append(os.path.dirname(os.path.abspath("/home/vortex/PCLA")))
# -------------------------- Change this to your PCLA directory --------------------------


from PCLA import PCLA

def main(patch_mode='single', scenario='dynamic'):

    print(f"Patch mode: {patch_mode}, Evaluation mode: {scenario}")

    # Path to the configuration files
    current_dir = os.path.dirname(os.path.abspath(__file__))
    yaml_file_path = os.path.join(current_dir, f'scenarios/{scenario}_{patch_mode}_scenario.yaml')
    json_file_path = os.path.join(current_dir, f'scenarios/{patch_mode}_evaluation.json')

    # Connect to the CARLA server
    client = carla.Client('localhost', 2000)
    client.set_timeout(10.0)

    # Load scenario configuration from YAML file
    with open(yaml_file_path, 'r') as file:
        config = yaml.safe_load(file)


    client.load_world(config['town'])

    try:
        # Initialize the client, get the world and set the weather
        traffic_manager, world, settings, synchronous_master = start_client(client)
        set_weather(world, config['sun_altitude_angle'], config['sun_azimuth_angle'])
        
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
                    pedestrian = spawn_pedestrian(world, bpLibrary, pedestrian_name, config['ped_x'], config['ped_y'], config['ped_z'], config['ped_pitch'], config['ped_yaw'], config['ped_roll'])

                # Spawning the npc vehicles
                vehicle_spawn_points = world.get_map().get_spawn_points()
                npc_list = []
                if sp_npcs:
                    npc_list = spawn_npcs(world, bpLibrary, vehicle_spawn_points, config['npc_spawn_points'], traffic_manager)

                # Setting up the route and spawning the ego vehicle
                start_loc , start_num = find_closest_spawn_point(world, carla.Location(x=config['start_x'], y=config['start_y'], z=config['start_z']), vehicle_spawn_points)
                end_loc , end_num = find_closest_spawn_point(world, carla.Location(x=config['end_x'], y=config['end_y'], z=config['end_z']), vehicle_spawn_points)
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

                begin_time = time.time()
                # Run the vehicle until it reaches the destination or a certain time is passed
                while is_far_from(vehicle.get_location(), end_loc, max_distance=2.0) and ((time.time() - begin_time) < config['time_allowed']) :
                    if scenario == 'dynamic' and sp_peds: # Change this later
                        move_pedestrian(pedestrian, vehicle, calc_distance, config['ped_distance'], config['target_ped_x'], config['target_ped_y'], config['target_ped_z'], vehicle.get_velocity())
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

    parser = argparse.ArgumentParser(description='Run DynamicDeception scenarios.')
    parser.add_argument('-patch', '--patch',
                        choices=['single', 'collusion'],
                        default='single',
                        help='The patch mode which says which type of patch should be used for evaluation (default: single)')
    parser.add_argument('-scenario', '--scenario',
                        choices=['dynamic', 'static'],
                        default='dynamic',
                        help='The scenario mode which can be dynamic or static to show whether to move the pedestrian or not (default: dynamic)')

    args = parser.parse_args()

    try:
        main(patch_mode=args.patch, eval_mode=args.scenario)
    except KeyboardInterrupt:
        pass
    finally:
        print('Done.')
