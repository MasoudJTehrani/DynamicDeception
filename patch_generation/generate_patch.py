from patch_functions import *

def main(generation_mode):
    print(f"Generation mode selected: {generation_mode}")

    #------------------------------------------------------------------------------------------------------
    # Initialization and Configuration

    # Set Environment Variables
    os.environ["TORCH_FORCE_NO_WEIGHTS_ONLY_LOAD"] = "1"

    # Path setup
    current_dir = os.path.dirname(os.path.abspath(__file__))
    yaml_file_path = os.path.join(current_dir,'patch_config.yaml')

    # Load patch configuration from YAML file
    # Read the YAML configuration file for more information
    with open(yaml_file_path, 'r') as file:
        config = yaml.safe_load(file)

    for key, value in config.items():
        globals()[key] = value

    INPUT_SHAPE = (CHANNELS, HEIGHT, WIDTH)
    patch_shape = (patch_channels, patch_height, patch_width)
    
    #------------------------------------------------------------------------------------------------------
    # Initialize components

    # Check for CUDA availability
    check_cuda()

    # Load YOLO model
    model = Yolo(yolov5.load(os.path.join(current_dir, YOLO_MODEL)))
    detector = pytorch_yolo(model, INPUT_SHAPE)

    # Set the seed for randomness
    set_seeds(42)

    # ------------------------------------------------------------------------------------------------------
    # Load and filter dataset
    training_images_for_generation, dets, validation_dirs, transform = load_and_predict_dataset(detector, INPUT_SHAPE, DATASET_CUTOFF_GENERATE, DATASET_CUTOFF, os.path.join(current_dir, TRAINING_DATASET_DIR), DATASET_URL)

    # Save or load the person detections to/from pickle file
    preds_orig_person = save_load_person_detections(dets, OBJECT_CATEGORY_NAMES, extract_predictions, load_data, save_data)
    patch_locations = preds_orig_person # Using this, the patches will be applied on the pedestrians locations

    # ------------------------------------------------------------------------------------------------------
    # Patch Generation
    torch.cuda.empty_cache()
    patch, loss = patch_generator(detector, generation_mode, training_images_for_generation, patch_locations, transform, yaml_file_path, current_dir)




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Patch generation script. Use --mode to select generation mode ('single', 'collusion').")
    parser.add_argument('--mode', type=str, default='single', help="Generation mode: 'single' (default) or other supported modes.")
    args = parser.parse_args()
    
    # Call the main function with the parsed arguments
    main(args.mode)