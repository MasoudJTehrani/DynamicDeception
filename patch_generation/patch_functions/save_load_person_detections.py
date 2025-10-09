import os
from tqdm import tqdm
#Save/load the person detection to/from file
def save_load_person_detections(dets, OBJECT_CATEGORY_NAMES, extract_predictions, load_data, save_data, current_dir="."):
    """
    Saves or loads the person detections to/from a pickle file
    dets: The detections from the model
    OBJECT_CATEGORY_NAMES: The object category names used by the model
    extract_predictions: The function to extract the predictions from the model output
    load_data: The function to load data from a pickle file
    save_data: The function to save data to a pickle file 
    Returns the person detections
    """
    preds_orig_person_stored = os.path.join(current_dir, "pickles", "preds_orig_person.pkl")
    # Check if the file exists
    if os.path.exists(preds_orig_person_stored):
        # Load from disk
        preds_orig_person = load_data(preds_orig_person_stored)
        print("preds_orig_person loaded from ", preds_orig_person_stored)
    else:
        # Get data and store to disk for later use
        preds_orig_person = [extract_predictions(d, OBJECT_CATEGORY_NAMES, 0.1, n_boxes=2, classes=["person"]) for d in tqdm(dets, desc="Getting Person Locations of Training Images")]
        save_data(preds_orig_person_stored, preds_orig_person)
        print("Data retrieved and saved to disk:", preds_orig_person_stored)
    return preds_orig_person
