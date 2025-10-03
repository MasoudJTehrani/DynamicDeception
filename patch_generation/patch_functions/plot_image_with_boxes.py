import os
import cv2
def plot_image_with_boxes(img, boxes, pred_cls, title, scores, color=(0,255,0), colordict={}, target_boxes=None):
    """
    Visualizes an image with the detected object boxes

    img: Image to plot
    boxes: Prediction boxes (from extract_predictions)
    pred_cls: Class (from extract_predictions)
    title: The plot title (str)
    scores: Score (from extract_predictions)
    color: Default color value for the boxes (tuple)
    colordict: Dictionary with box colors for some classes (dict) like {"car":(255,0,0)}
    """
    text_size = 1
    text_th = 3
    rect_th = 4

    for i in range(len(boxes)):
        if target_boxes is not None:
            #print("target_boxes[i])", target_boxes)
            cv2.rectangle(img, (int(target_boxes[0]), int(target_boxes[1])), (int(target_boxes[2]), int(target_boxes[3])),
                        color=(255,255,0), thickness=rect_th//2)

        cv2.rectangle(img, (int(boxes[i][0][0]), int(boxes[i][0][1])), (int(boxes[i][1][0]), int(boxes[i][1][1])),
                      color=colordict.get(pred_cls[i], color), thickness=rect_th)
        # Write the prediction class
        cv2.putText(img, pred_cls[i]+" "+f"{scores[i]:.2f}", (int(boxes[i][0][0]), int(boxes[i][0][1])), cv2.FONT_HERSHEY_SIMPLEX, text_size,
                    colordict.get(pred_cls[i], color), thickness=text_th)


    # Ensure "plots" folder exists
    current_dir = os.path.dirname(os.path.abspath(__file__))
    plots_dir = os.path.join(current_dir, 'plots')
    if not os.path.exists(plots_dir):
        os.makedirs(plots_dir)

    # Save the image to the "plots" folder
    save_path = os.path.join(plots_dir, f"{title}.png")
    cv2.imwrite(save_path, img)
