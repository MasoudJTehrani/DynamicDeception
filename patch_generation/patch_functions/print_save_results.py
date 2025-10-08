import os

def print_save_results(successful_attacks, number_of_attacks, all_stop_sign_scores_patch,
                       current_dir, generation_mode, config, successful_attacks_l=0, successful_attacks_r=0, use_patch=True):  
    lines = []
    if use_patch:
        header = "Validation Results (Using Patch):"
    else:
        header = "Validation Results (Using Disguise):"
    lines.append(header)
    print("\n" + header)

    if generation_mode == "collusion" and config.get('TRY_HALF_PATCH', False):
        lines.append("Validation Results (Collusion Mode with Half Patch):")
        lines.append(f"Total Attacks: {number_of_attacks}")
        lines.append(f"Successful Attacks (Both Halves): {successful_attacks}")
        lines.append(f"Successful Attacks (Left Half): {successful_attacks_l}")
        lines.append(f"Successful Attacks (Right Half): {successful_attacks_r}")

        total = number_of_attacks if number_of_attacks > 0 else 1
        rate_both = successful_attacks / total
        rate_left = successful_attacks_l / total
        rate_right = successful_attacks_r / total

        lines.append(f"Success Rate (Both Halves): {rate_both:.2%}")
        lines.append(f"Success Rate (Left Half): {rate_left:.2%}")
        lines.append(f"Success Rate (Right Half): {rate_right:.2%}")

        print("\n".join(lines[-7:]))
    else:
        lines.append("Validation Results (Single Patch Mode):")
        lines.append(f"Total Attacks: {number_of_attacks}")
        lines.append(f"Successful Attacks: {successful_attacks}")

        total = number_of_attacks if number_of_attacks > 0 else 1
        rate = successful_attacks / total
        lines.append(f"Success Rate: {rate:.2%}")

        print("\n".join(lines[-4:]))

    if all_stop_sign_scores_patch:
        avg_score = sum(all_stop_sign_scores_patch) / len(all_stop_sign_scores_patch)
        avg_line = f"Average Stop Sign Score (Patched): {avg_score:.4f}"
        lines.append(avg_line)
        print(avg_line)

    # Ensure current_dir exists and save results to file
    os.makedirs(current_dir, exist_ok=True)
    results_path = os.path.join(current_dir, f"validation_results_{generation_mode}.txt")
    try:
        with open(results_path, 'w') as f:
            f.write("\n".join(lines) + "\n")
        print(f"Validation results saved to {results_path}")
    except Exception as e:
        print(f"Failed to save validation results to {results_path}: {e}")
