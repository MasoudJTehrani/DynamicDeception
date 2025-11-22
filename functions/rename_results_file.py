
import os
import pandas as pd

def rename_results_file(current_dir, patch_mode, scenario, scenario_name):

    results_dir = os.path.join(current_dir, 'results')
    old_file_path = os.path.join(results_dir, 'language_result.csv')
    new_file_name = f'language_result_{patch_mode}_{scenario}_{scenario_name}.csv'
    new_file_path = os.path.join(results_dir, new_file_name)

    # Read the CSV file
    df = pd.read_csv(old_file_path)

    # Calculate mean and std for each row and add as new column
    mean_std_values = []
    for i in range(len(df)):
        mean_std_values.append(f"{df.iloc[i, 1:].mean():.2f}+-{df.iloc[i, 1:].std():.2f}")

    df['mean+-std'] = mean_std_values
    # Save the modified dataframe with header
    df.to_csv(new_file_path, index=False, header=True)
    print(f'Results file renamed to: {new_file_name}')
