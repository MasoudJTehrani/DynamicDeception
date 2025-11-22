import time
import os
from .save_run import save_run

def clean_up(current_dir, npc_list, pedestrians, pcla):
    """Cleans up the spawned NPCs, pedestrian, vehicle, and PCLA instance.

    Args:
        sp_npcs (bool): Whether NPCs were spawned.
        npc_list (list): List of spawned NPC actors.
        sp_peds (bool): Whether a pedestrian was spawned.
        pedestrians (carla.Actor): The spawned pedestrians actors.
        vehicle (carla.Actor): The spawned vehicle actor.
        pcla (PCLA): The PCLA instance.

    """
    save_run(current_dir)

    print('...Cleaning up the actors and PCLA instance...')
    if npc_list:
        for npc in npc_list:
            npc.destroy()
    if pedestrians:
        for ped in pedestrians:
            ped.destroy()
    pcla.cleanup()
    time.sleep(0.5)
