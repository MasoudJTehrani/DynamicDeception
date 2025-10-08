import pickle

def save_patch(patch, loss, ap, save_path):
    with open(save_path, "wb") as f:
        pickle.dump({"patch": patch, "loss": loss, "ap": ap}, f)
    

def load_patch(load_path):
    with open(load_path, "rb") as f:
        data = pickle.load(f)
    return data["patch"], data["loss"], data["ap"]
