import torch
import torchvision
def extract_predictions(predictions_, OBJECT_CATEGORY_NAMES, conf_thresh=0, n_boxes=5, classes=[], DEBUG=False):
    """
    Filters the predictions obtained from a model by their confidence and classes

    predictions_: The predictions from a model
    conf_thresh: Min. score for predictions to be included (float)
    n_boxes: Max. number of prediction to keep (takes the ones with highest score) (int)
    classes: classes to keep (all if empty) (list)

    Returns a tuple of (classes, boxes, scores) of the detections
    """

    # Filter by confidence threshold
    boxes = predictions_["boxes"]
    scores = predictions_["scores"]
    labels = predictions_["labels"]

    if DEBUG: print(f">>>> filtering {len(scores)} with threshold {conf_thresh}")
    filtered_indices = [i for i, score in enumerate(scores) if score >= conf_thresh]
    if len(filtered_indices) < 1:
        return [], [], []
    boxes = [boxes[i] for i in filtered_indices]
    scores = [scores[i] for i in filtered_indices]
    labels = [labels[i] for i in filtered_indices]

    # Apply Non-Maximum Suppression (NMS)
    boxes_tensor = torch.tensor(boxes)
    scores_tensor = torch.tensor(scores)
    if DEBUG: print(f">>>> running NMS with {len(scores)} scores")
    keep_indices = torchvision.ops.nms(boxes_tensor, scores_tensor, iou_threshold=0.5).tolist()

    #print(predictions_)

    predictions_class = [OBJECT_CATEGORY_NAMES[i] for i in labels]  # For each prediction, get the predicted class
    predictions_boxes = [[(i[0], i[1]), (i[2], i[3])] for i in boxes]  # Get the predicted bounding boxes
    predictions_score = scores  # Get the prediction score

    predictions_class = [predictions_class[i] for i in keep_indices]
    predictions_boxes = [predictions_boxes[i] for i in keep_indices]
    predictions_score = [predictions_score[i] for i in keep_indices]

    predictions_t = sorted(range(len(predictions_score)), key=lambda i: predictions_score[i], reverse=True)  # Sort the prediction indices by their score

    # Put the other lists in the same order, by descending prediction score
    predictions_boxes = [predictions_boxes[i] for i in predictions_t]
    predictions_class = [predictions_class[i] for i in predictions_t]
    predictions_scores = [predictions_score[i] for i in predictions_t]
    if classes:  # only keep the n_boxes best detections of the specified classes, if they are above the confidence threshold
        predictions_boxes_n = [e for e, c, s in zip(predictions_boxes, predictions_class, predictions_scores) if c in classes and s >= conf_thresh][:n_boxes]
        predictions_class_n = [e for e, s in zip(predictions_class, predictions_scores) if e in classes and s >= conf_thresh][:n_boxes]
        predictions_scores_n = [e for e, c in zip(predictions_scores, predictions_class) if c in classes and e >= conf_thresh][:n_boxes]
    else:  # only keep the n_boxes best detections
        predictions_boxes_n = predictions_boxes[:n_boxes]
        predictions_class_n = predictions_class[:n_boxes]
        predictions_scores_n = predictions_scores[:n_boxes]

    if DEBUG: print(f"predictions_class_n {predictions_class_n}")
    if DEBUG: print(f"predictions_boxes_n {predictions_boxes_n}")
    if DEBUG: print(f"predictions_scores_n {predictions_scores_n}")
    return predictions_class_n, predictions_boxes_n, predictions_scores_n
