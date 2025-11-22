import os

def recreate_files(current_dir):
    """Recreates empty results files for future runs.

    Args:
        current_dir (str): The current directory where results are stored.
    """
    with open(os.path.join(current_dir, 'results/language_result.txt'), 'w') as f:
        f.write('pedestrians: 0\n')
        f.write('stop signs: 0\n')
    
    with open(os.path.join(current_dir, 'results/language_result.csv'), 'w') as f:
        f.write('pedestrians:\n')
        f.write('stop signs:\n')
        