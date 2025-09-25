def spawn_npcs(world, bpLibrary, vehicle_spawn_points, npc_spawn_points, traffic_manager):
    """
    Function to spawn NPC vehicles in the simulation.
    Args:
        world: Carla world object
        bpLibrary: Carla blueprint library
        vehicle_spawn_points: List of spawn points in the Carla world
        npc_spawn_points: List of indices for spawn points to use for NPCs
        traffic_manager: Carla traffic manager object
    Returns:
        vehicles_list: List of spawned NPC vehicle actors
    """
    blueprints = bpLibrary.filter('vehicle.*')
    vehicles_list = []
    for sp in npc_spawn_points:
        npc = world.try_spawn_actor(blueprints[sp%10], vehicle_spawn_points[sp])
        if npc is not None:
            vehicles_list.append(npc)
            npc.set_autopilot(True, traffic_manager.get_port())
            print('spawned npc vehicle %s' % npc.type_id)
    return vehicles_list
