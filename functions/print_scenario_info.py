def print_scenario_info(agent_name, scenario_name, sp_npcs, sp_peds, pedestrian_name, description):
    print("-" * 50)
    print(f"--- Processing Agent: {agent_name} ---")
    print(f"  Scenario: {scenario_name}")
    print(f"    Spawn NPCs: {sp_npcs}")
    print(f"    Spawn Peds: {sp_peds}")
    print(f"    Pedestrian Name: '{pedestrian_name}'")
    print(f"    Description: {description}")
    print("-" * 50)