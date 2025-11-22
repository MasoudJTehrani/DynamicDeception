import os
import pandas as pd

def save_run(current_dir):
    """Saves the run results by appending pedestrian and stop sign counts to CSV.
    Args:
        current_dir (str): The current directory where results are stored.
    """

    # Read the language_result.txt file and extract numbers
    txt_path = os.path.join(current_dir, 'results/language_result.txt')
    csv_path = os.path.join(current_dir, 'results/language_result.csv')
    
    if os.path.exists(txt_path):
        with open(txt_path, 'r') as f:
            lines = f.readlines()
        
        # Extract numbers from txt file
        pedestrians_count = None
        stop_signs_count = None
        
        for line in lines:
            if 'pedestrians:' in line.lower():
                pedestrians_count = line.split(':')[-1].strip()
            elif 'stop signs:' in line.lower():
                stop_signs_count = line.split(':')[-1].strip()
        
        # Read existing CSV and append values using pandas
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            
            # Add 'num' column with the extracted counts
            new_col = pd.DataFrame({
                'num': [pedestrians_count, stop_signs_count]
            })
            df = pd.concat([df, new_col], axis=1)
            
            df.to_csv(csv_path, index=False)
