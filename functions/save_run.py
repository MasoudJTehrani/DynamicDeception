import os

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
        
        # Read existing CSV and append values
        if os.path.exists(csv_path):
            with open(csv_path, 'r') as f:
                csv_lines = f.readlines()
            
            updated_lines = []
            for line in csv_lines:
                line = line.rstrip('\n')
                if 'pedestrians:' in line.lower() and pedestrians_count:
                    line += ',' + pedestrians_count
                elif 'stop signs:' in line.lower() and stop_signs_count:
                    line += ',' + stop_signs_count
                updated_lines.append(line)
            
            with open(csv_path, 'w') as f:
                f.write('\n'.join(updated_lines) + '\n')