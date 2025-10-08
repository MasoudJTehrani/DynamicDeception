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
    with open(yaml_file_path, 'r') as file:
        config = yaml.safe_load(file)

    INPUT_SHAPE = (config['CHANNELS'], config['HEIGHT'], config['WIDTH'])

    #------------------------------------------------------------------------------------------------------
    # Model Setup
    # Check for CUDA availability
    check_cuda()
    # Load YOLO model
    model = Yolo(yolov5.load(os.path.join(current_dir, config['YOLO_MODEL'])))
    detector = pytorch_yolo(model, INPUT_SHAPE)
    # Set the seed for randomness
    set_seeds(42)

    # ------------------------------------------------------------------------------------------------------
    # Load and filter dataset
    training_images_for_generation, dets, validation_dirs, transform, dirs = load_and_predict_dataset(detector, INPUT_SHAPE, config['DATASET_CUTOFF_GENERATE'], config['DATASET_CUTOFF'], os.path.join(current_dir, config['TRAINING_DATASET_DIR']), config['DATASET_URL'])

    # Save or load the person detections to/from pickle file
    preds_orig_person = save_load_person_detections(dets, config['OBJECT_CATEGORY_NAMES'], extract_predictions, load_data, save_data)
    patch_locations = preds_orig_person # Using this, the patches will be applied on the pedestrians locations

    # ------------------------------------------------------------------------------------------------------
    # Patch Generation
    torch.cuda.empty_cache()
    patch, loss, ap = patch_generator(detector, generation_mode, training_images_for_generation, patch_locations, transform, yaml_file_path, current_dir)

    # Save or load patch, loss, and ap to a file using pickle. This file is not pushed in git.
    save_patch(patch, loss, ap, os.path.join(current_dir, "patch_results.pkl"))
    #patch, loss, ap = load_patch(os.path.join(current_dir, "patch_results.pkl"))

    # ------------------------------------------------------------------------------------------------------
    # Loss analysis
    analyze_loss(loss, config['optimizer'], config['learning_rate'], config['disguise_distance_factor'], ap, current_dir)
    
    # ------------------------------------------------------------------------------------------------------
    # Save the generated patch image
    Image.fromarray(patch.transpose(1,2,0).astype(np.uint8)).save(os.path.join(current_dir, "plots/patches/patch.png"))
    print(f"\nThe patch is saved in: \n{os.path.join(current_dir, 'plots/patches/')}")

    # ------------------------------------------------------------------------------------------------------
    # Patch validation
    all_stop_sign_scores_patch, number_of_attacks = validate_patch(detector, yaml_file_path, validation_dirs, dirs, generation_mode, patch, ap, current_dir, transform)

    # ------------------------------------------------------------------------------------------------------
    # Compare patch to the disguise image to see if the patch made a difference
    all_stop_sign_scores_disguise, number_of_attacks = validate_patch(detector, yaml_file_path, validation_dirs, dirs, generation_mode, patch, ap, current_dir, transform, use_patch= False)

    # ------------------------------------------------------------------------------------------------------
    # Visualize the validation
    visualize_validation(all_stop_sign_scores_patch, all_stop_sign_scores_disguise, K=number_of_attacks, current_dir=current_dir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Patch generation script. Use -mode to select generation mode ('single', 'collusion').")
    parser.add_argument('-mode', type=str, default='single', help="Generation mode: 'single' (default) or other supported modes.")
    args = parser.parse_args()
    
    if args.mode not in ['single', 'collusion']:
        raise ValueError("Invalid mode. Please choose 'single' or 'collusion'.")
    
    # Call the main function with the parsed arguments
    main(args.mode)