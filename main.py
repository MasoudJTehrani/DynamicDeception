import carla
import time
import os
import sys
import yaml
# import all the functions in the functions directory
from functions import *


# Add the directory containing PCLA.py to the Python path
sys.path.append(os.path.dirname(os.path.abspath("/home/vortex/PCLA")))
current_dir = os.path.dirname(os.path.abspath(__file__))
yaml_file_path = os.path.join(current_dir, 'scenarios', 'static_single_scenario.yaml')

from PCLA import PCLA

def main():

    client = carla.Client('localhost', 2000)
    client.set_timeout(10.0)

    # Load scenario configuration from YAML file
    with open(yaml_file_path, 'r') as file:
        config = yaml.safe_load(file)
    
    for key, value in config.items():
        globals()[key] = value

    ped_spawn_point = carla.Transform(
        carla.Location(x=x, y=y, z=z),
        carla.Rotation(pitch=pitch, yaw=yaw, roll=roll)
    )

    client.load_world(town)

    #pedestrian_bp = bpLibrary.filter('walker.pedestrian.0062')[0]
    sp_npcs = False
    sp_peds = True
    agent = "if_if"

    try:
        traffic_manager, world, settings, synchronous_master = start_client(client)
        set_weather(world)
        
        # Finding actors
        bpLibrary = world.get_blueprint_library()
        pedestrian_bp = bpLibrary.filter('walker.pedestrian.0062')[0]
        ## Finding vehicle
        vehicleBP = bpLibrary.filter('model3')[0]
        vehicle_spawn_points = world.get_map().get_spawn_points()

        # Spawning npc vehicles
        
        vehicles_list = spawn_npcs(sp_npcs, world, bpLibrary, vehicle_spawn_points, traffic_manager)
        

        # Spawn a pedestrian
        pedestrian = spawn_pedestrian(sp_peds, world, bpLibrary)

        # Setting up the route and spawning the ego vehicle
        make_route(client, start_loc, end_loc, vehicle_spawn_points, PCLA)
        vehicle = world.spawn_actor(vehicleBP, vehicle_spawn_points[start_loc]) # Spawning the ego vehicle
        world.tick()

        # Set up PCLA
        route = "route.xml"
        pcla = PCLA.PCLA(agent, vehicle, route, client)
        
        # Set the spectator according the vehicle's transform
        spectator = world.get_spectator()
        spectator.set_transform(put_spectator(vehicle.get_transform()))
        world.tick()

        print('Spawned the vehicle with model =', agent,', press Ctrl+C to exit.\n')
        while True:
            ego_action = pcla.get_action()
            vehicle.apply_control(ego_action)
            world.tick()
    
    finally:
        settings.synchronous_mode = False
        world.apply_settings(settings)

        # Destroy vehicles, pedestrian and PCLA
        print('\nCleaning up the vehicles')
        if spawn_npcs:
            for npc in vehicles_list:
                npc.destroy()
        if spawn_pedestrian:
            pedestrian.destroy()
        if vehicle:
            vehicle.destroy()
        pcla.cleanup()
        time.sleep(0.5)

if __name__ == '__main__':

    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        print('Done.')

