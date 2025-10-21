
def rename_results_file(current_dir, patch_mode, scenario, scenario_name):
    import os
    # Rename the results file based on the patch mode and scenario
    results_dir = os.path.join(current_dir, 'results')
    old_file_path = os.path.join(results_dir, 'language_result.txt')
    new_file_name = f'language_result_{patch_mode}_{scenario}_{scenario_name}.txt'
    new_file_path = os.path.join(results_dir, new_file_name)

    if os.path.exists(old_file_path):
        os.rename(old_file_path, new_file_path)
        print(f'Results file renamed to: {new_file_name}')
    else:
        print('Results file does not exist.')