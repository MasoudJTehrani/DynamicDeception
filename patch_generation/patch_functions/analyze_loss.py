import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import os

def analyze_loss(loss, optimizer, learning_rate, disguise_distance_factor, ap, current_dir):
    plt.style.use('ggplot')
    matplotlib.use('Agg')  # Use the 'Agg' backend for headless mode

    loss_history = []
    for epoch in loss:
        loss_history.append(sum(epoch))
    loss_history = np.array(loss_history)

    # Loss per epoch
    plt.plot(loss_history * (-1 if optimizer=="pgd" else 1))
    plt.xlabel("Training Epochs")
    plt.ylabel("Loss (box + class + score)")
    plt.title(f"Loss during Training with LR {learning_rate}")
    plt.savefig(os.path.join(current_dir, 'plots/loss/loss_per_epoch.png'), dpi=300, bbox_inches='tight')
    plt.clf()

    # Loss per batch with moving average
    flat_loss = [batch_loss for epoch in loss for batch_loss in epoch] # flatten the loss history (it contains loss per patch in a list per epoch)
    flat_loss = np.array(flat_loss) * (-1 if optimizer=="pgd" else 1)

    # Define the size of the sliding window
    k = 10
    # Calculate the moving average
    moving_averages = np.convolve(flat_loss, np.ones(k)/k, mode='valid')
    # Indices for the moving average to align with the input list
    average_indices = range(k - 1, len(flat_loss))

    try:
        plt.plot(flat_loss, linewidth=0.5, color=("red"), label="Loss per batch")
        plt.plot(average_indices, moving_averages, linestyle='--', color='blue', linewidth=5, label=f'Moving Average (k={k})')


        plt.xlabel("Training Batches")  # Label the implicit x-axis
        plt.ylabel("Loss (box + class + score + disguise)")
        plt.legend()
        plt.title(f"Loss per batch during training with LR {learning_rate}")
        plt.savefig(os.path.join(current_dir, 'plots/loss/loss_per_batch.png'), dpi=300, bbox_inches='tight')
        plt.clf()

    except Exception as e:
        print("failed to plot avg:", e)

    # Loss by component and per batch
    try:
        # Calculate the sum of both losses
        total_losses = [d + c for d, c in zip((i * disguise_distance_factor for i in ap.detailed_loss_history["disguise"]), ap.detailed_loss_history["classification"])]

        # Create steps for x-axis
        steps = list(range(1, len(total_losses) + 1))

        plt.figure(figsize=(10, 6))

        # Plot the three lines
        plt.plot(steps, [i * disguise_distance_factor for i in  ap.detailed_loss_history["disguise"]], 'b-', linewidth=2, label='Disguise Loss')
        plt.plot(steps, ap.detailed_loss_history["classification"], 'g-', linewidth=2, label='Classification Loss')
        plt.plot(steps, total_losses, 'r-', linewidth=2.5, label='Total Loss')

        plt.xlabel('Training Step')
        plt.ylabel('Loss Value')
        plt.title('Loss History Comparison')

        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(current_dir, 'plots/loss/loss_history.png'), dpi=300, bbox_inches='tight')
        plt.clf()

    except Exception as e:
        print(e)
    
    print(f"\nLoss plots are saved in: \n{os.path.join(current_dir, 'plots/loss/')}")