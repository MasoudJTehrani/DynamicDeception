import time
def clean_up(npc_list, pedestrian, pcla):
    """Cleans up the spawned NPCs, pedestrian, vehicle, and PCLA instance.

    Args:
        sp_npcs (bool): Whether NPCs were spawned.
        npc_list (list): List of spawned NPC actors.
        sp_peds (bool): Whether a pedestrian was spawned.
        pedestrian (carla.Actor): The spawned pedestrian actor.
        vehicle (carla.Actor): The spawned vehicle actor.
        pcla (PCLA): The PCLA instance.

    """
    print('...Cleaning up the actors and PCLA instance...')
    if npc_list:
        for npc in npc_list:
            npc.destroy()
    if pedestrian:
        pedestrian.destroy()
    pcla.cleanup()
    time.sleep(0.5)
