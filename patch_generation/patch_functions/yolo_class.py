import torch
from yolov5.utils.loss import ComputeLoss
from art.estimators.object_detection.pytorch_yolo import PyTorchYolo

class Yolo(torch.nn.Module):
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.model.hyp = {'box': 0.05,
                        'obj': 1.0,
                        'cls': 0.5,
                        'anchor_t': 4.0,
                        'cls_pw': 1.0,
                        'obj_pw': 1.0,
                        'fl_gamma': 0.0
                        }
        self.compute_loss = ComputeLoss(self.model.model.model)

    def forward(self, x, targets=None):
        if self.training:
            #print("self.training is true")
            outputs = self.model.model.model(x)
            loss, loss_items = self.compute_loss(outputs, targets)
            loss_components_dict = {"loss_total": loss}
            loss_components_dict['loss_box'] = loss_items[0]
            loss_components_dict['loss_obj'] = loss_items[1]
            loss_components_dict['loss_cls'] = loss_items[2]
            return loss_components_dict
        else:
            outputs = self.model(x)
            return outputs

def pytorch_yolo(model, INPUT_SHAPE):
    # creates the detector model
    return PyTorchYolo(model=model,
                    device_type='gpu',
                    input_shape=INPUT_SHAPE,
                    clip_values=(0, 255),
                    attack_losses=("loss_total", "loss_cls",
                                    "loss_box",
                                    "loss_obj"))