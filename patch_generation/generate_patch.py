from patch_functions import *
import pickle

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
    training_images_for_generation, dets, validation_dirs, transform, dirs = load_and_predict_dataset(detector, INPUT_SHAPE, DATASET_CUTOFF_GENERATE, DATASET_CUTOFF, os.path.join(current_dir, TRAINING_DATASET_DIR), DATASET_URL)

    # Save or load the person detections to/from pickle file
    #spreds_orig_person = save_load_person_detections(dets, OBJECT_CATEGORY_NAMES, extract_predictions, load_data, save_data)
    #patch_locations = preds_orig_person # Using this, the patches will be applied on the pedestrians locations

    # ------------------------------------------------------------------------------------------------------
    # Patch Generation
    torch.cuda.empty_cache()
    #patch, loss, ap = patch_generator(detector, generation_mode, training_images_for_generation, patch_locations, transform, yaml_file_path, current_dir)

    # Save patch, loss, and ap to a file using pickle
    save_path = os.path.join(current_dir, "patch_results.pkl")
    #with open(save_path, "wb") as f:
        #pickle.dump({"patch": patch, "loss": loss, "ap": ap}, f)

    # To load later:
    with open(save_path, "rb") as f:
        data = pickle.load(f)
    patch = data["patch"]
    loss = data["loss"]
    ap = data["ap"]

    # ------------------------------------------------------------------------------------------------------
    # Loss analysis
    analyze_loss(loss, optimizer, learning_rate, disguise_distance_factor, ap, current_dir)
    
    # ------------------------------------------------------------------------------------------------------
    # Save the generated patch
    Image.fromarray(patch.transpose(1,2,0).astype(np.uint8)).save(os.path.join(current_dir, "plots/patches/patch.png"))
    print(f"\nThe patch is saved in: \n{os.path.join(current_dir, 'plots/patches/')}")

    # ------------------------------------------------------------------------------------------------------
    # Patch validation
    torch.cuda.empty_cache()
    set_seeds(42)
    validate_patch(detector, yaml_file_path, validation_dirs, dirs, generation_mode, patch, ap, current_dir, transform)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Patch generation script. Use --mode to select generation mode ('single', 'collusion').")
    parser.add_argument('--mode', type=str, default='single', help="Generation mode: 'single' (default) or other supported modes.")
    args = parser.parse_args()
    
    # Call the main function with the parsed arguments
    main(args.mode)