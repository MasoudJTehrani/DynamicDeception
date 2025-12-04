
# DynamicDeception

Replication package for the paper: **_Dynamic Deception: When Pedestrians Team Up to Fool Autonomous Cars_**

---
## Contents

1. [Setup](#-setup)
2. [Pedestrians’ Shirts](#-pedestrians-shirts)
3. [Running the Code](#-running-the-code)
4. [Configurations](#-configurations)
5. [Results](#-results)


## 🚀 Setup

1. **Build CARLA from source**  
   To customize the environment (stop signs and pedestrians), you must build CARLA from source.  
   Follow the official guide:  
   https://carla.readthedocs.io/en/latest/build_carla/

   The CARLA version required for replicating our paper is **0.9.15.2**:  
   https://github.com/carla-simulator/carla/tree/0.9.15.2

2. **Install PCLA**  
   This project depends on the [PCLA](https://github.com/MasoudJTehrani/PCLA) framework.  
   Ensure that:
   - PCLA is cloned on your system  
   - The PCLA Python environment is activated  
   - You can run PCLA agents

3. **Update the PCLA path in `main.py`**  
   In `main.py`, modify line 7 to point to your PCLA directory:
   ```python
   sys.path.append(os.path.dirname(os.path.abspath("/home/vortex/PCLA")))
   ```

4. **Replace the Simlingo agent**

    A customized `agent_simlingo.py` script is included in the `extras/` folder.
    This version prints and saves language prompts as `.txt` files inside the `results/` directory.

	  Replace the default PCLA Simlingo agent by copying this file to :
	  `/path/to/PCLA/pcla_agents/simlingo/agent_simlingo.py`

6. **Modify the stop sign in Town07**

    To replicate our experimental setup, open Town07 in the CARLA UE editor and hide or remove the stop sign at the target intersection used in the paper.

## 👕 Pedestrians’ Shirts
  The pedestrian shirt textures used in our experiments are inside the `images/` folder.
  You may reuse them to replicate the study.
  
  A YouTube tutorial is available showing:
  
  - how to modify pedestrian shirts,
  - how to create new pedestrian models,
  - and how to spawn customized pedestrians in CARLA.

## ▶️ Running the Code

***While the PCLA environment is active***, run an evaluation with:

```Shell
python main.py -patch <option> -scenario <option>
``` 

**`-patch` options:**

-   `single` – evaluate the single pedestrian attack
    
-   `collusion` – evaluate the collusion attack
    

**`-scenario` options:**

-   `static` – pedestrian remains still
    
-   `dynamic` – pedestrian moves with the vehicle

## ⚙️ Configurations

All configuration files are located in the `scenarios/` directory.  
Each file includes explanatory comments.

### `general_scenario.yaml`

This file contains configuration values shared across all scenarios in a given town.

**Important:** NPC spawn points change depending on how Town07 is loaded.

-   **If Town07 is preloaded via the UE editor**, use:
    
    `npc_spawn_points: [22, 46, 45, 108]` 
    
-   **If Town07 is loaded through the Python API**:
    
    `client.load_world("Town07")` 
    
    then you must adjust the NPC spawn points accordingly.
    

> Ego vehicle's spawning point does _not_ need to be changed, as the autonomous vehicle uses coordinate-based spawning (see line ~14 in the YAML file).

### Scenario-based YAML files

Each combination of `-patch` and `-scenario` has its own YAML file with fine-grained controls such as spawn locations, the movements and etc.
    

### `#scenario_evaluation.json`

This file defines:

-   which PCLA agent performs evaluation
-   scenario names
-   whether to spawn npc and pedestrians or not
-   IDs of the pedestrians being evaluated (must match our scenarios for replication)

## 📊 Results

All outputs are stored under the `results/` directory.

You will find **CSV files** containing model-level statistics (per-run and aggregated mean ± std).
The system-level evaluation were done by analysing recorded videos (used to manually count full stops).

## 📂 Project Structure (Overview)

```Bash
├─ images/ # Shirt textures for pedestrians 
├─ extras/ # Custom agent (agent_simlingo.py) 
├─ scenarios/ # YAML configuration files 
├─ results/ # CSV logs 
├─ main.py # Python evaluation file 
└─ README.md
```

## Citation
If you find PCLA useful, please consider giving it a star 🌟, and cite the published paper

```bibtex
Title{Dynamic Deception}
```
