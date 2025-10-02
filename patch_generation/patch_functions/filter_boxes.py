def filter_boxes(predictions, conf_thresh):
    """
    Filters the predictions obtained from a model by their confidence
    predictions: The predictions from a model
    conf_thresh: Min. score for predictions to be included (float)
    Returns a tuple of (classes, boxes, scores) of the detections
    """

    dictionary = {}

    boxes_list = []
    scores_list = []
    labels_list = []

    for i in range(len(predictions[0]["boxes"])):
        score = predictions[0]["scores"][i]
        if score >= conf_thresh:
            boxes_list.append(predictions[0]["boxes"][i])
            scores_list.append(predictions[0]["scores"][[i]])
            labels_list.append(predictions[0]["labels"][[i]])

    #dictionary["boxes"] = np.vstack(boxes_list)
    if boxes_list:  # Check if boxes_list is not empty
        dictionary["boxes"] = np.vstack(boxes_list)
        dictionary["scores"] = np.hstack(scores_list)
        dictionary["labels"] = np.hstack(labels_list)
    else:
        dictionary["boxes"] = np.empty((0,))  # Assign an empty array if boxes_list is empty
        dictionary["scores"] = np.empty((0,))
        dictionary["labels"] = np.empty((0,))

    y = [dictionary]

    return y
