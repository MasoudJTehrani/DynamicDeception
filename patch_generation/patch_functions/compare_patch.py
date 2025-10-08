import numpy as np
import yaml
from PIL import Image
from .validation_functions import *
from .extract_predictions import extract_predictions
from .plot_image_with_boxes import plot_image_with_boxes

def compare_patch(yaml_file_path, generation_mode, dirs, validation_dirs, detector, transform, ap):

    # Load patch configuration from YAML file
    with open(yaml_file_path, 'r') as file:
        config = yaml.safe_load(file)

    if generation_mode == "single":
        disguise_patch=np.array(Image.open(config['SINGLE_DISGUISE_PATH'])) # load external patch
    else:
        disguise_patch=np.array(Image.open(config['COLLUSION_DISGUISE_PATH'])) # load external patch
    disguise_patch = disguise_patch.transpose(2,0,1)

    cut_dirs = validation_dirs[:config['DATASET_CUTOFF'] if config['DATASET_CUTOFF'] > 0 and config['DATASET_CUTOFF'] <= len(dirs) else len(dirs)]
    show_indices = set(random.sample(range(len(cut_dirs) + 1), config['PLOT_N_SAMPLES']))
    
    dets_orig = batch_predict(cut_dirs, config['batch_size'], detector, transform)
    preds_orig_person = [extract_predictions(dets, config['OBJECT_CATEGORY_NAMES'], conf_thresh=config['plot_threshold'], n_boxes=config['n_boxes'], classes=["person"]) for dets in dets_orig]

    number_of_attacks_disguise = 0
    successful_attacks_disguise = 0

    all_stop_sign_scores_disguise = []

    for j in tqdm(range(len(cut_dirs)), desc="val steps"):
        training_images = get_images(cut_dirs[j:j+1], transform)

        if generation_mode == 'collusion':
            if config['TRY_HALF_PATCH']:
                patched_images_l, target_boxes_l = ap.apply_patch(training_images[:], scale=config['SCALE'], patch_external=disguise_patch, split=config['split'], split_keep_both=False, half_to_keep="left", return_patch_outlines=True, patch_locations=preds_orig_person[j:j+1])
                dets_l = batch_predict_raw(patched_images_l, detector = detector)

                patched_images_r, target_boxes_r = ap.apply_patch(training_images[:], scale=config['SCALE'], patch_external=disguise_patch, split=config['split'], split_keep_both=False, half_to_keep="right", return_patch_outlines=True, patch_locations=preds_orig_person[j:j+1])
                dets_r = batch_predict_raw(patched_images_r, detector = detector)

            patched_images, target_boxes = ap.apply_patch(training_images[:], scale=config['SCALE'], patch_external=disguise_patch, split=config['split'], split_keep_both=True, return_patch_outlines=True, patch_locations=preds_orig_person[j:j+1]) # , locations =
        else:
            patched_images, target_boxes = ap.apply_patch(training_images[:], scale=config['SCALE'], patch_external=disguise_patch, split=config['split'], split_keep_both=True, return_patch_outlines=True, patch_locations=preds_orig_person[j:j+1])

        dets = batch_predict_raw(patched_images, detector = detector)


        for i in range(len(dets)):

            number_of_attacks_disguise += 1
            if i<config['SKIP']:
                continue
            preds_orig = extract_predictions(dets_orig[i], config['OBJECT_CATEGORY_NAMES'], conf_thresh=config['plot_threshold'], n_boxes=config['n_boxes'], classes=config['classes'])

            preds = extract_predictions(dets[i], config['OBJECT_CATEGORY_NAMES'], conf_thresh=config['plot_threshold'], n_boxes=config['n_boxes'], classes=config['classes'])
            preds_stop_sign = extract_predictions(dets[i], config['OBJECT_CATEGORY_NAMES'], conf_thresh=config['success_threshold'], n_boxes=config['n_boxes'], classes=["stop sign"])

            overlapping_stop_sign_preds = overlapping(preds_stop_sign, target_boxes[i])

            preds_stop_sign = overlapping_stop_sign_preds
            preds = preds_stop_sign # TODO TEMP REMOVE

            if preds_stop_sign[2]:
                all_stop_sign_scores_disguise.append(preds_stop_sign[2][0]) # index 2 is all scores, 0 taking the first

            if preds_stop_sign[0]:
                successful_attacks_disguise += 1
            
            if config['SAVE_IMAGES'] or j in show_indices:
                plot_image_with_boxes(index = number_of_attacks, img=patched_images[i].transpose(1,2,0).copy(), boxes=preds[1], pred_cls=preds[0], target_boxes=target_boxes[i],
                                    title=f"Predictions on image with both halves patch", scores=preds[2], colordict=config['colordict'], current_dir=current_dir)

            

