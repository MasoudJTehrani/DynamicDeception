import carla
import time
import os
import sys

# Add the directory containing PCLA.py to the Python path
sys.path.append(os.path.dirname(os.path.abspath("/home/vortex/PCLA")))
current_dir = os.path.dirname(os.path.abspath(__file__))

from PCLA import PCLA
#from PCLA import route_maker
#from PCLA import location_to_waypoint
def put_spectator(location):
    # Puts the spectator in the location given to starting point of the vehicle
    loc = carla.Location(x=location.location.x, y=location.location.y, z=location.location.z + 20)
    rot = carla.Rotation(pitch=location.rotation.pitch - 50, yaw=location.rotation.yaw, roll=location.rotation.roll)
    return carla.Transform(loc, rot)

def set_weather(world):
    weather = carla.WeatherParameters(
        sun_altitude_angle=120.0,
        sun_azimuth_angle=30.0)
    world.set_weather(weather)

def main():

    client = carla.Client('localhost', 2000)
    client.set_timeout(10.0)
    #client.load_world("Town07")
    synchronous_master = False
    start_loc = 10
    end_loc = 37

    try:
        world = client.get_world()
        traffic_manager = client.get_trafficmanager(8000)

        set_weather(world)
        settings = world.get_settings()
        asynch = False
        if not asynch:
            traffic_manager.set_synchronous_mode(True)
            if not settings.synchronous_mode:
                synchronous_master = True
                settings.synchronous_mode = True
                settings.fixed_delta_seconds = 0.05
            else:
                synchronous_master = False
        else:
            print("You are currently in asynchronous mode. If this is a traffic simulation, \
                    you could experience some issues. If it's not working correctly, switch to \
                    synchronous mode by using traffic_manager.set_synchronous_mode(True)")
        world.apply_settings(settings)
        
        # Finding actors
        bpLibrary = world.get_blueprint_library()

        ## Finding vehicle
        vehicleBP = bpLibrary.filter('model3')[0]

        vehicle_spawn_points = world.get_map().get_spawn_points()


        # Spawning npc vehicles
        spawn_npcs = False
        spawn_pedestrian = True
        agent = "if_if"

        if spawn_npcs:
            spawn_points = [22, 46, 45, 108, 111]
            blueprints = bpLibrary.filter('vehicle.*')
            vehicles_list = []
            for sp in spawn_points:
                npc = world.try_spawn_actor(blueprints[sp%10], vehicle_spawn_points[sp])
                if npc is not None:
                    vehicles_list.append(npc)
                    npc.set_autopilot(True, traffic_manager.get_port())
                    print('spawned npc vehicle %s' % npc.type_id)

        ### Spawn vehicle
        #transform = carla.Transform(carla.Location(x=74, y=141), carla.Rotation(yaw=0))
        #vehicle = world.spawn_actor(vehicleBP, vehicle_spawn_points[start_loc])
        
        # Retrieve the spectator object
        spectator = world.get_spectator()

        # Spawn a pedestrian
        
        if spawn_pedestrian:
            pedestrian_bp = bpLibrary.filter('walker.pedestrian.0062')[0]
            spawn_point = carla.Transform()
            spawn_point.location = carla.Location(x=5.5, y=55.5, z=1.5)
            spawn_point.rotation = carla.Rotation(pitch=0, yaw=180, roll=0)
            pedestrian = world.try_spawn_actor(pedestrian_bp, spawn_point)
            world.tick()

        #print(vehicle_spawn_points[start_loc])

        client = carla.Client('localhost', 2000)
        world = client.get_world()

        vehicle_spawn_points = world.get_map().get_spawn_points() # Carla spawn points
        startLoc = vehicle_spawn_points[start_loc].location # Start location
        endLoc = vehicle_spawn_points[end_loc].location # End location
        waypoints = PCLA.location_to_waypoint(client, startLoc, endLoc)  # Returns waypoints between two locations
        PCLA.route_maker(waypoints, "route.xml")  # Returns waypoints usable for PCLA
        #wp_loc = waypoints[-30].transform.location
        #wp_rot = waypoints[-30].transform.rotation

        #vehicle = world.spawn_actor(vehicleBP, carla.Transform(carla.Location(x=wp_loc.x, y=wp_loc.y, z=1), carla.Rotation(wp_rot.pitch, yaw=wp_rot.yaw, roll=wp_rot.roll)))
        vehicle = world.spawn_actor(vehicleBP, vehicle_spawn_points[start_loc])

        world.tick()

        
        route = "route.xml"
        pcla = PCLA.PCLA(agent, vehicle, route, client)
        
        # Set the spectator with our transform
        spectator.set_transform(put_spectator(vehicle.get_transform()))
        world.tick()

        print('Spawned the vehicle with model =', agent,', press Ctrl+C to exit.\n')
        while True:
            ego_action = pcla.get_action()
            #print(ego_action)
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

