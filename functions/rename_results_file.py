
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
    df['mean_std'] = df.iloc[:, 1:].apply(lambda row: f"{row.mean():.1f}+-{row.std():.1f}", axis=1)

    # Save the modified dataframe
    df.to_csv(new_file_path, index=False)
    print(f'Results file renamed to: {new_file_name}')
