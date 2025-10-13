# import all the functions in the functions directory
from functions import *

# Add the directory containing PCLA.py to the Python path

# -------------------------- Change this to your PCLA directory --------------------------
sys.path.append(os.path.dirname(os.path.abspath("/home/vortex/PCLA")))
# -------------------------- Change this to your PCLA directory --------------------------


from PCLA import PCLA

def main(patch_mode='single', scenario='dynamic'):

    print(f"Patch mode: {patch_mode}\nScenario mode: {scenario}")

    # Path to the configuration files
    current_dir = os.path.dirname(os.path.abspath(__file__))
    config_file_path = os.path.join(current_dir, f'scenarios/{patch_mode}_{scenario}_scenario.yaml')
    general_config_path = os.path.join(current_dir, 'scenarios/general_scenario.yaml')
    json_file_path = os.path.join(current_dir, f'scenarios/{patch_mode}_evaluation.json')

    # Connect to the CARLA server
    client = carla.Client('localhost', 2000)
    client.set_timeout(10.0)

    # Load scenario configuration from YAML file
    with open(config_file_path, 'r') as file:
        config = yaml.safe_load(file)
        
    # Load general configuration from YAML file and add to config dictionary
    with open(general_config_path, 'r') as file:
        general_config = yaml.safe_load(file)
    config.update(general_config)

    client.load_world(config['town'])

    # Keep references so final cleanup can stop/join the thread if needed
    stop_event = None
    enter_thread = None

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
                sp_npcs, sp_peds, pedestrian_names = (scenario_data[k] for k in ("sp_npcs", "sp_peds", "pedestrian_names"))
                print_scenario_info(agent_name, scenario_name, sp_npcs, sp_peds, pedestrian_names)
                
                # Spawning the pedestrian
                bpLibrary = world.get_blueprint_library()
                pedestrians = None
                if sp_peds:
                    pedestrians = spawn_pedestrian(world, bpLibrary, pedestrian_names, config['ped_x'], config['ped_y'], config['ped_z'], config['ped_pitch'], config['ped_yaw'], config['ped_roll'], config['sec_ped_distance'])

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

                # Allow user to abort the run by pressing Enter
                # Use select to avoid a permanently blocking input() so we can stop the thread cleanly.
                stop_event = threading.Event()
                enter_thread = threading.Thread(target=wait_for_enter, args=(stop_event,), daemon=True)
                enter_thread.start()

                # Run the vehicle until it reaches the destination, time runs out, or user presses Enter
                begin_time = time.time()
                while is_far_from(vehicle.get_location(), end_loc) \
                      and ((time.time() - begin_time) < config['time_allowed']) \
                      and (not stop_event.is_set()):
                    if scenario == 'dynamic' and sp_peds:
                        move_pedestrian(pedestrians, vehicle, calc_distance, config['ped_distance'], config['target_ped_x'], config['target_ped_y'], config['target_ped_z'], vehicle.get_velocity())
                    ego_action = pcla.get_action()
                    vehicle.apply_control(ego_action)
                    world.tick()

                if stop_event.is_set():
                    print("--------Scenario aborted early by user (Enter pressed)--------")
                else:
                    # signal the thread to exit (if it's still waiting) and join it
                    stop_event.set()
                    if enter_thread is not None and enter_thread.is_alive():
                        enter_thread.join(timeout=1.0)

                # Clean up the actors and PCLA instance
                clean_up(npc_list, pedestrians, pcla)

    finally:
        # Ensure the enter thread is stopped/joined before final exit
        try:
            if stop_event is not None:
                stop_event.set()
            if enter_thread is not None and enter_thread.is_alive():
                enter_thread.join(timeout=1.0)
        except Exception:
            pass

        # Restore the original settings
        settings.synchronous_mode = False
        world.apply_settings(settings)

        # Clean up in case of an error
        clean_up(npc_list, pedestrians, pcla)

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
        main(patch_mode=args.patch, scenario=args.scenario)
    except KeyboardInterrupt:
        pass
    finally:
        print('Done.')
