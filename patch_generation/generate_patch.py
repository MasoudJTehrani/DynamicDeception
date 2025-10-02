from patch_functions import *

def main(generation_mode):
    print(f"Generation mode selected: {generation_mode}")
    # Set Environment Variables
    os.environ["TORCH_FORCE_NO_WEIGHTS_ONLY_LOAD"] = "1"

    # Path setup
    current_dir = os.path.dirname(os.path.abspath(__file__))
    yaml_file_path = os.path.join(current_dir,'patch_config.yaml')

    # Load patch configuration from YAML file
    with open(yaml_file_path, 'r') as file:
        config = yaml.safe_load(file)

    INPUT_SHAPE = (config['CHANNELS'], config['HEIGHT'], config['WIDTH'])

    # If you want the patch generation to start from pretrained patches, set GENERATE to False
    if not config['GENERATE']:
        SINGLE_DISGUISE_PATH = config['PRETRAINED_SINGLE_PATH']
        COLLUSION_DISGUISE_PATH = config['PRETRAINED_COLLUSION_PATH']
    else:
        SINGLE_DISGUISE_PATH = config['SINGLE_DISGUISE_PATH']
        COLLUSION_DISGUISE_PATH = config['COLLUSION_DISGUISE_PATH']

    # Check for CUDA availability
    check_cuda()

    # Load YOLO model
    model = Yolo(yolov5.load(config['YOLO_MODEL']))
    detector = pytorch_yolo(model, INPUT_SHAPE)

    # Set the seed for randomness
    set_seeds(42)

    # Load and filter dataset
    training_images_for_generation, dets, validation_dirs = load_and_predict_dataset(detector, INPUT_SHAPE, config['DATASET_CUTOFF_GENERATE'], config['DATASET_CUTOFF'], config['TRAINING_DATASET_DIR'], config['DATASET_URL'])

    # Save or load the person detections to/from pickle file
    save_load_person_detections(dets, config['OBJECT_CATEGORY_NAMES'], extract_predictions, load_data, save_data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Patch generation script. Use --mode to select generation mode ('single', 'collusion').")
    parser.add_argument('--mode', type=str, default='single', help="Generation mode: 'single' (default) or other supported modes.")
    args = parser.parse_args()
    
    # Call the main function with the parsed arguments
    main(args.mode)