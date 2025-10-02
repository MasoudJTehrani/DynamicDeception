from patch_functions import *

os.environ["TORCH_FORCE_NO_WEIGHTS_ONLY_LOAD"] = "1"
current_dir = os.path.dirname(os.path.abspath(__file__))
yaml_file_path = os.path.join(current_dir,'patch_config.yaml')

check_cuda()

# Load patch configuration from YAML file
with open(yaml_file_path, 'r') as file:
    config = yaml.safe_load(file)

for key, value in config.items():
    globals()[key] = value

INPUT_SHAPE = (CHANNELS, HEIGHT, WIDTH)

# Load YOLO model
model = Yolo(yolov5.load(YOLO_MODEL))
detector = pytorch_yolo(model, INPUT_SHAPE)

# Set the seed for randomness
set_seeds(42)

# ------------------------------------------------------------------------------------------------------
# Load and filter dataset
training_images_for_generation, dets = load_and_filter_dataset(detector, INPUT_SHAPE, DATASET_CUTOFF_GENERATE, DATASET_CUTOFF, TRAINING_DATASET_DIR, DATASET_URL)

# NOTE: This is a temporary workaround for https://github.com/Trusted-AI/adversarial-robustness-toolbox/issues/2601
def create_detector_model():
    model2 = yolov5.load(YOLO_MODEL)
    model2 = Yolo(model2)
    detector2 = PyTorchYolo(model=model2,
                    device_type='gpu',
                    input_shape=INPUT_SHAPE,
                    clip_values=(0, 255),
                    attack_losses=("loss_total", "loss_cls",
                                    "loss_box",
                                    "loss_obj"))
    return detector2