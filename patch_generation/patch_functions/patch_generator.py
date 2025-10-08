import numpy as np
import os
import yaml
import yolov5
from PIL import Image
import torch
from art.attacks.evasion import AdversarialPatchPyTorch
from .yolo_class import Yolo, pytorch_yolo

def patch_generator(detector, generation_mode, training_images_for_generation, 
                    patch_locations, transform, yaml_file_path, current_dir):
    
    torch.cuda.empty_cache()
    # Load patch configuration from YAML file
    with open(yaml_file_path, 'r') as file:
        config = yaml.safe_load(file)

    INPUT_SHAPE = (config['CHANNELS'], config['HEIGHT'], config['WIDTH'])
    patch_shape = (config['patch_channels'], config['patch_height'], config['patch_width'])

    if generation_mode == 'single':
        split = False
        disguise = np.array(Image.open(os.path.join(current_dir, config['SINGLE_DISGUISE_PATH'])).resize(patch_shape[1:]))
    else:
        split = True
        disguise = np.array(Image.open(os.path.join(current_dir, config['COLLUSION_DISGUISE_PATH'])).resize(patch_shape[1:]))
    disguise = disguise.transpose(2,0,1)

    if not config['GENERATE']:
        max_epochs = 1
        max_steps = 1
    else:
        max_epochs = config['max_epochs']
        max_steps = config['max_steps']

    # This is the target detection, e.g. what we want the detections by the model to look like. Mostly a class with score 1 at the patch location
    # NOTE: Currently, this will get overwritten in the generation as we place the patches on the pedestrians, except for the target class (label)
    synthetic_y = {
        'boxes': np.array([[0,0,0,0]], dtype=np.float32), # TODO the box would be based on patch_location and patch_shape
        'scores': np.array([    1], dtype=np.float32),
        'labels': np.array([config['OBJECT_CATEGORY_NAMES'].index("stop sign")])
    }

    pretrained_patch = None
    if not config['GENERATE'] and generation_mode == 'single':
        pretrained_patch = np.array(Image.open(config['PRETRAINED_SINGLE_PATH']).resize(patch_shape[1:]))
        pretrained_patch = pretrained_patch.transpose(2,0,1)
    elif not config['GENERATE'] and generation_mode == 'collusion':
        pretrained_patch = np.array(Image.open(config['PRETRAINED_COLLUSION_PATH']).resize(patch_shape[1:]))
        pretrained_patch = pretrained_patch.transpose(2,0,1)

    ap = AdversarialPatchPyTorch(
        estimator=detector,
        summary_writer=False,
        patch_type=config['patch_type'],
        targeted=config['targeted'],
        verbose=True,
        rotation_max=config['rotation_max'],
        scale_min=config['scale_min'],
        scale_max=config['scale_max'],
        distortion_scale_max=config['distortion_scale_max'],
        contrast_min=config['contrast_min'],
        contrast_max=config['contrast_max'],
        optimizer=config['optimizer'],
        scheduler=config['scheduler'],
        learning_rate=config['learning_rate'],
        max_epochs=max_epochs,
        max_steps=max_steps,
        batch_size=config['batch_size'],
        patch_shape=patch_shape,
        pretrained_patch=pretrained_patch,
        disguise=disguise,
        disguise_distance_factor=config['disguise_distance_factor'],
        split=split,
        gap_size=config['gap_size'],
        fixed_gap=config['fixed_gap'],
    )

    # This is a temporary workaround for https://github.com/Trusted-AI/adversarial-robustness-toolbox/issues/2601
    def create_detector_model():
        model = Yolo(yolov5.load(os.path.join(current_dir, config['YOLO_MODEL'])))
        return pytorch_yolo(model, INPUT_SHAPE)

    if config['GENERATE']:
        patch, patch_mask, loss = ap.generate(
            x=training_images_for_generation,
            y=[synthetic_y]*len(training_images_for_generation),
            patch_locations=patch_locations,
            fixed_location_random_scaling=config['fixed_location_random_scaling'],
            transform=transform,
            detector_creator=create_detector_model,
            decay_rate=config['decay_rate'],
            decay_step=config['decay_step']
        )
    else:
        patch, patch_mask, loss = ap.generate(
            x=training_images_for_generation,
            y=[synthetic_y]*len(training_images_for_generation),
            transform=transform,
        )
        if generation_mode == 'single':
            patch = np.array(Image.open(os.path.join(current_dir, config['PRETRAINED_SINGLE_PATH'])))
        else:
            patch = np.array(Image.open(os.path.join(current_dir, config['PRETRAINED_COLLUSION_PATH'])))
        patch = patch.transpose(2,0,1)

    return patch, loss, ap