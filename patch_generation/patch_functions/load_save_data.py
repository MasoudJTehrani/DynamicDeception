# Function to load data
def load_data(file_path):
    with open(file_path, 'rb') as f:
        return pickle.load(f)

# Function to save data
def save_data(file_path, data):
    with open(file_path, 'wb') as f:
        pickle.dump(data, f)
