import os
import warnings
import random
import numpy as np
from tqdm import tqdm
from PIL import Image
from torchvision.transforms import transforms
from .download_dataset import download_dataset
from sklearn.model_selection import train_test_split

def load_and_transform_image(dir, transform):
        im = Image.open(dir)
        return transform(im).numpy()

def batch_predict(dirs, batch_size, transform, detector):
    all_predictions = []
    for i in tqdm(range(0, len(dirs), batch_size), desc="Loading, transforming and predicting Batches"):
        batch_dirs = dirs[i:i + batch_size]
        batch_images = np.array([load_and_transform_image(dir, transform) for dir in batch_dirs])*255
        batch_dets = detector.predict(batch_images)
        all_predictions.extend(batch_dets)
    return all_predictions

def load_and_filter_dataset(detector, INPUT_SHAPE, DATASET_CUTOFF_GENERATE, DATASET_CUTOFF, TRAINING_DATASET_DIR, DATASET_dir):
    
    # Download the dataset if it does not exist
    download_dataset(DATASET_dir, TRAINING_DATASET_DIR)

    """
    Ignore all future warnings
    Reason:
    Adversarial-Patch-ART\.venv\Lib\site-packages\yolov5\models\common.py:682: FutureWarning: 
    `torch.cuda.amp.autocast(args...)` is deprecated. Please use `torch.amp.autocast('cuda', args...)` instead.
    with amp.autocast(autocast):
    """
    warnings.simplefilter(action='ignore', category=FutureWarning)

    dirs = []
    # Iterate over all files and directories in the given path
    for root, _dirs_, files in os.walk(TRAINING_DATASET_DIR):
        for file in files:
            file_path = os.path.join(root, file)
            dirs+=[file_path]

    print("Size of Dataset:", len(dirs))

    if not DATASET_CUTOFF:
        DATASET_CUTOFF = len(dirs)

    # Calculate padding, assumes all images in the training set have the same resolution
    train_img_height = Image.open(dirs[0]).height
    padding_top = (INPUT_SHAPE[1] - train_img_height) // 2
    padding_bottom = INPUT_SHAPE[1] - train_img_height - padding_top

    transform = transforms.Compose([
            #transforms.Resize(INPUT_SHAPE[1], interpolation=transforms.InterpolationMode.BICUBIC),
            #transforms.CenterCrop(INPUT_SHAPE[1]),
            transforms.Pad((0, padding_top, 0, padding_bottom)),
            transforms.ToTensor(),
            transforms.Lambda(lambda x: x[:3])  # Keep only the first 3 channels (RGB)
        ])

    # Randomly sample DATASET_CUTOFF images if the dataset is larger than the cutoff
    sampled_dirs = random.sample(dirs, DATASET_CUTOFF if DATASET_CUTOFF > 0 and DATASET_CUTOFF <= len(dirs) else len(dirs))

    # Use train_test_split to split the data
    train_dirs, validation_dirs = train_test_split(
        sampled_dirs, test_size=0.2, random_state=42
    )

    training_images_for_generation = train_dirs

    if DATASET_CUTOFF_GENERATE:
        training_images_for_generation = training_images_for_generation[:DATASET_CUTOFF_GENERATE]

    print("Dataset size after cutoff for patch training:", len(training_images_for_generation))

    batch_size = 1
    dets = batch_predict(training_images_for_generation, batch_size, transform, detector) # get the moels predictions on the benign training images

    torch.cuda.empty_cache()

    return training_images_for_generation, dets
