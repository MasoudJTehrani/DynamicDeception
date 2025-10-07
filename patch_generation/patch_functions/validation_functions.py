from PIL import Image
import numpy as np
from tqdm import tqdm

def load_and_transform_image(url, transform):
    im = Image.open(url)
    return transform(im).numpy()

def batch_predict(urls, batch_size, detector, transform):
    all_predictions = []
    for i in tqdm(range(0, len(urls), batch_size), desc="predict"):
        batch_urls = urls[i:i + batch_size]
        batch_images = np.array([load_and_transform_image(url, transform) for url in batch_urls])*255
        batch_dets = detector.predict(batch_images)
        all_predictions.extend(batch_dets)
    return all_predictions

def get_images(urls, transform):
    images = np.array([load_and_transform_image(url, transform) for url in urls])*255
    return images

def batch_predict_raw(imgs, detector, batch_size=1):
    all_predictions = []
    for i in range(0, len(imgs), batch_size):
        batch_imgs = imgs[i:i + batch_size]
        batch_dets = detector.predict(batch_imgs)
        all_predictions.extend(batch_dets)
    return all_predictions

def rectangles_overlap(box1, box2):
    """
    Check if two rectangles overlap.
    Args:
        box1: tuple of (x1, y1, x2, y2) or ((x1, y1), (x2, y2))
        box2: tuple of (x1, y1, x2, y2)
    """
    # Handle different input formats
    if len(box1) == 2 and isinstance(box1[0], tuple):
        # Format: ((x1, y1), (x2, y2))
        x1_1, y1_1 = box1[0]
        x2_1, y2_1 = box1[1]
    else:
        # Format: (x1, y1, x2, y2)
        x1_1, y1_1, x2_1, y2_1 = box1

    x1_2, y1_2, x2_2, y2_2 = box2

    if x2_1 <= x1_2 or x2_2 <= x1_1 or y2_1 <= y1_2 or y2_2 <= y1_1:
        return False
    return True

def overlapping(preds, target):
    """
    Filter predictions to keep only those that overlap with the target box
    That way we remove any detections of real stop signs or false positives that are not caused by a patch
    """

    labels, boxes, scores = preds

    filtered_labels = []
    filtered_boxes = []
    filtered_scores = []

    # Check each prediction box against all target boxes
    for j, pred_box in enumerate(boxes):
        if rectangles_overlap(pred_box, target):
            filtered_labels.append(labels[j])
            filtered_boxes.append(pred_box)
            filtered_scores.append(scores[j])

    return (filtered_labels, filtered_boxes, filtered_scores)