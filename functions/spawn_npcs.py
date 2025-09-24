def spawn_npcs(spawn_npcs, world, bpLibrary, vehicle_spawn_points, traffic_manager):
    """
    Function to spawn NPC vehicles in the simulation.
    Args:
        spawn_npcs: Boolean to decide whether to spawn NPC vehicles
        world: Carla world object
        bpLibrary: Carla blueprint library
        vehicle_spawn_points: List of spawn points in the Carla world
        traffic_manager: Carla traffic manager object
    Returns:
        vehicles_list: List of spawned NPC vehicle actors
    """
    if spawn_npcs:
        npc_spawn_points = [22, 46, 45, 108, 111]
        blueprints = bpLibrary.filter('vehicle.*')
        vehicles_list = []
        for sp in npc_spawn_points:
            npc = world.try_spawn_actor(blueprints[sp%10], vehicle_spawn_points[sp])
            if npc is not None:
                vehicles_list.append(npc)
                npc.set_autopilot(True, traffic_manager.get_port())
                print('spawned npc vehicle %s' % npc.type_id)
        return vehicles_list
