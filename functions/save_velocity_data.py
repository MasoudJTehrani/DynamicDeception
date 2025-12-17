def save_velocity_data(current_dir, patch_mode, scenario, scenario_name, iteration, velocity_data):
    """
    plot the velocity data of the vehicle and save to a CSV file.
    Parameters:
    - current_dir: directory to save the data
    - patch_mode: the patch mode used in the scenario
    - scenario: the scenario type
    - scenario_name: name of the scenario
    - iteration: iteration number
    - velocity_data: list of [x, y, z] velocity vectors
    """
    import os
    import csv
    import math

    # Create the directory if it doesn't exist
    output_dir = os.path.join(current_dir, 'results/velocity_data')
    os.makedirs(output_dir, exist_ok=True)

    # Convert 3D velocity vectors to speed (magnitude)
    speeds = [math.sqrt(v.x**2 + v.y**2 + v.z**2) for v in velocity_data]

    # Define the output file path
    output_file = os.path.join(output_dir, f'velocity_{patch_mode}_{scenario}_{scenario_name}_iter{iteration}.csv')

    # Write the velocity data to the CSV file
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Frame', 'Speed (m/s)'])
        for i, speed in enumerate(speeds):
            writer.writerow([i, speed])
    print(f"Velocity data saved to {output_file}")

    # plot the velocity data
    import matplotlib.pyplot as plt

    times = list(range(len(speeds)))

    plt.figure(figsize=(10, 6))
    plt.plot(times, speeds, label='Speed (m/s)')
    plt.xlabel('Time Step')
    plt.ylabel('Speed (m/s)')
    plt.title(f'Velocity Data for {scenario_name} ({patch_mode} - {scenario}) - Iteration {iteration}')
    plt.legend()
    plt.grid()
    plt.savefig(os.path.join(output_dir, f'velocity_plot_{patch_mode}_{scenario}_{scenario_name}_iter{iteration}.png'))
    plt.close()
    print(f"Velocity plot saved to {output_dir}")
