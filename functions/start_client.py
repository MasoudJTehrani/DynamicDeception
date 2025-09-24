import carla

def start_client(client, asynch=False):
    """
    Initializes the CARLA client, world, traffic manager, and settings.
    Args:
        client (carla.Client): The CARLA client instance.
        asynch (bool): Flag to determine if the simulation should run in asynchronous mode.
    Returns:
        tuple: A tuple containing the traffic manager, world, settings, and a boolean indicating if
               this instance is the synchronous master.
    """
    world = client.get_world()
    traffic_manager = client.get_trafficmanager(8000)
    settings = world.get_settings()
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
    return traffic_manager, world, settings, synchronous_master
