from .validation_functions import *
from .extract_predictions import extract_predictions
from .plot_image_with_boxes import plot_image_with_boxes
from .set_seeds import set_seeds
import torch
import yaml
import random
import os

def validate_patch(detector, yaml_file_path, validation_dirs, dirs, generation_mode, patch, ap, current_dir, transform, use_patch= True):
    
    torch.cuda.empty_cache()
    set_seeds(42)
    detector.model.eval()

    # Load patch configuration from YAML file
    with open(yaml_file_path, 'r') as file:
        config = yaml.safe_load(file)

    # Validate the disguise instead of the patch if use_patch is False
    if not use_patch:
        print("\nValidating the disguise image instead of the patch.")
        if generation_mode == "single":
            patch=np.array(Image.open(config['SINGLE_DISGUISE_PATH'])) # load external patch
        else:
            patch=np.array(Image.open(config['COLLUSION_DISGUISE_PATH'])) # load external patch
        patch = patch.transpose(2,0,1) # This will make the AdversarialPatch use the disguise image
    
    # Turning config['colordict'] values from lists to tuples, {'stop sign': (255, 0, 0), 'banana': (0, 0, 255), ...}
    if 'colordict' in config and config['colordict'] is not None:
        # Iterate through the dictionary and convert each list value to a tuple
        for key, value_list in config['colordict'].items():
            config['colordict'][key] = tuple(value_list)

    if config['SCALE'] is not None:
        config['SCALE'] = config['scale_max'] - (config['scale_max'] - config['scale_min']) / 2 # take the middle of the scale range

    cut_dirs = validation_dirs[:config['DATASET_CUTOFF'] if config['DATASET_CUTOFF'] > 0 and config['DATASET_CUTOFF'] <= len(dirs) else len(dirs)]
    show_indices = set(random.sample(range(len(cut_dirs) + 1), config['PLOT_N_SAMPLES']))

    #set_seeds()
    dets_orig = batch_predict(cut_dirs, config['batch_size'], detector, transform)
    preds_orig_person = [extract_predictions(dets, config['OBJECT_CATEGORY_NAMES'], conf_thresh=config['plot_threshold'], n_boxes=config['n_boxes'], classes=["person"]) for dets in dets_orig]

    number_of_attacks = 0
    successful_attacks = 0
    successful_attacks_l = 0
    successful_attacks_r = 0
    

    all_stop_sign_scores_patch = []

    for j in tqdm(range(len(cut_dirs)), desc="val steps"):
        training_images = get_images(cut_dirs[j:j+1], transform)

        if generation_mode == 'collusion':
            if config['TRY_HALF_PATCH']:
                patched_images_l, target_boxes_l = ap.apply_patch(training_images[:], scale=config['SCALE'], patch_external=patch, split=True, split_keep_both=False, half_to_keep="left", return_patch_outlines=True, patch_locations=preds_orig_person[j:j+1])
                dets_l = batch_predict_raw(patched_images_l, detector = detector)

                patched_images_r, target_boxes_r = ap.apply_patch(training_images[:], scale=config['SCALE'], patch_external=patch, split=True, split_keep_both=False, half_to_keep="right", return_patch_outlines=True, patch_locations=preds_orig_person[j:j+1])
                dets_r = batch_predict_raw(patched_images_r, detector = detector)

            patched_images, target_boxes = ap.apply_patch(training_images[:], scale=config['SCALE'], patch_external=patch, split=True, split_keep_both=True, return_patch_outlines=True, patch_locations=preds_orig_person[j:j+1])
        else:
            patched_images, target_boxes = ap.apply_patch(training_images[:], scale=config['SCALE'], patch_external=patch, split=False, split_keep_both=True, return_patch_outlines=True, patch_locations=preds_orig_person[j:j+1])

        dets = batch_predict_raw(patched_images, detector = detector)

        # Analyze predictions for each image in the batch
        for i in range(len(dets)):
            number_of_attacks += 1
            if i < config['SKIP']:
                continue
            preds_orig = extract_predictions(dets_orig[i], config['OBJECT_CATEGORY_NAMES'], conf_thresh=config['plot_threshold'], n_boxes=config['n_boxes'], classes=config['classes'])

            preds = extract_predictions(dets[i], config['OBJECT_CATEGORY_NAMES'], conf_thresh=config['plot_threshold'], n_boxes=config['n_boxes'], classes=config['classes'])
            preds_stop_sign = extract_predictions(dets[i], config['OBJECT_CATEGORY_NAMES'], conf_thresh=config['success_threshold'], n_boxes=config['n_boxes'], classes=["stop sign"])

            overlapping_stop_sign_preds = overlapping(preds_stop_sign, target_boxes[i])

            if generation_mode == 'collusion' and config['TRY_HALF_PATCH']:
                preds_l = extract_predictions(dets_l[i], config['OBJECT_CATEGORY_NAMES'], conf_thresh=config['plot_threshold'], n_boxes=config['n_boxes'], classes=config['classes'])
                preds_r = extract_predictions(dets_r[i], config['OBJECT_CATEGORY_NAMES'], conf_thresh=config['plot_threshold'], n_boxes=config['n_boxes'], classes=config['classes'])
                preds_stop_sign_l = extract_predictions(dets_l[i], config['OBJECT_CATEGORY_NAMES'], conf_thresh=config['success_threshold'], n_boxes=config['n_boxes'], classes=["stop sign"])
                preds_stop_sign_r = extract_predictions(dets_r[i], config['OBJECT_CATEGORY_NAMES'], conf_thresh=config['success_threshold'], n_boxes=config['n_boxes'], classes=["stop sign"])
                overlapping_stop_sign_preds_l = overlapping(preds_stop_sign_l, target_boxes[i])
                overlapping_stop_sign_preds_r = overlapping(preds_stop_sign_r, target_boxes[i])
                if overlapping_stop_sign_preds_l[0]:
                    successful_attacks_l += 1
                if overlapping_stop_sign_preds_r[0]:
                    successful_attacks_r += 1


            preds_stop_sign = overlapping_stop_sign_preds
            if config['ONLY_OVERLAPPING']:
                preds = preds_stop_sign

            if preds_stop_sign[2]:
                all_stop_sign_scores_patch.append(preds_stop_sign[2][0]) # index 2 is all scores, 0 taking the first

            if preds_stop_sign[0]:
                successful_attacks += 1

            # Remove "and use_patch" to also save the validation images for the disguise. You also need to change the title
            if (config['SAVE_IMAGES'] or j in show_indices) and use_patch:
                plot_image_with_boxes(index = number_of_attacks, img=patched_images[i].transpose(1,2,0).copy(), boxes=preds[1], pred_cls=preds[0], target_boxes=target_boxes[i],
                                    title=f"Predictions on image with both halves patch", scores=preds[2], colordict=config['colordict'], current_dir=current_dir)

            # Remove "and use_patch" to also save the validation images for the disguise. You also need to change the title
            if generation_mode == 'collusion' and config['TRY_HALF_PATCH'] and (config['SAVE_IMAGES'] or j in show_indices) and use_patch:
                plot_image_with_boxes(index = number_of_attacks, img=patched_images_l[i].transpose(1,2,0).copy(), boxes=preds_l[1], pred_cls=preds_l[0], target_boxes=target_boxes_l[i],
                                        title="Predictions on image with left half of patch", scores=preds_l[2], colordict=config['colordict'], current_dir=current_dir)
                plot_image_with_boxes(index = number_of_attacks, img=patched_images_r[i].transpose(1,2,0).copy(), boxes=preds_r[1], pred_cls=preds_r[0], target_boxes=target_boxes_r[i],
                                        title="Predictions on image with right half of patch", scores=preds_r[2], colordict=config['colordict'], current_dir=current_dir)

    print(f'Images are saved to \n{os.path.join(current_dir, "plots", "validation")}')

    if use_patch:
        print("\nValidation Results (Using Patch):")
    else:
        print("\nValidation Results (Using Disguise):")
        
    if generation_mode == "collusion" and config['TRY_HALF_PATCH']:
        print(f"Validation Results (Collusion Mode with Half Patch):")
        print(f"Total Attacks: {number_of_attacks}")
        print(f"Successful Attacks (Both Halves): {successful_attacks}")
        print(f"Successful Attacks (Left Half): {successful_attacks_l}")
        print(f"Successful Attacks (Right Half): {successful_attacks_r}")
        print(f"Success Rate (Both Halves): {successful_attacks / number_of_attacks:.2%}")
        print(f"Success Rate (Left Half): {successful_attacks_l / number_of_attacks:.2%}")
        print(f"Success Rate (Right Half): {successful_attacks_r / number_of_attacks:.2%}")
    else:
        print(f"Validation Results (Single Patch Mode):")
        print(f"Total Attacks: {number_of_attacks}")
        print(f"Successful Attacks: {successful_attacks}")
        print(f"Success Rate: {successful_attacks / number_of_attacks:.2%}")

    if all_stop_sign_scores_patch:
        avg_score = sum(all_stop_sign_scores_patch) / len(all_stop_sign_scores_patch)
        print(f"Average Stop Sign Score (Patched): {avg_score:.4f}")

    return all_stop_sign_scores_patch, number_of_attacks