import matplotlib.pyplot as plt
import os

def visualize_validation(red_points, blue_points, K, current_dir):
        #matplotlib.use('Agg')  # Use the 'Agg' backend for headless mode
        
        plt.rcParams.update({
            'font.size': 17,
            'axes.labelsize': 17,
            'axes.titlesize': 17,
            'xtick.labelsize': 17,
            'ytick.labelsize': 17,
            'legend.fontsize': 17
        })
        
        red_points.sort()
        blue_points.sort()
        
        total_red = K  
        total_blue = K
        successful_red = len(red_points)
        successful_blue = len(blue_points)
        
        red_x = []
        red_y = []
        blue_x = []
        blue_y = []
        
        for i, s in enumerate(red_points):
            red_x.append(s)
            red_y.append(successful_red/total_red - (i / total_red))
            
        for i, s in enumerate(blue_points):
            blue_x.append(s)
            blue_y.append(successful_blue/total_blue - (i / total_blue))  
        
        plt.figure(figsize=(8, 6))
        
        plt.plot(red_x, red_y, color="red", label="Adversarial Patch", 
                marker='.', markersize=14,
                linewidth=2.5,
                linestyle='-')
        plt.plot(blue_x, blue_y, color="blue", label="Disguise", 
                marker='.', markersize=14,
                linewidth=2.5,
                linestyle='-')
        
        plt.legend(frameon=True, fancybox=True, framealpha=0.8)
        plt.xlabel('Confidence Score')
        plt.ylabel('Attack Success Rate (ASR)')
        #plt.title('Complementary Cumulative Distribution Function')
        
        # Thicker grid lines
        plt.grid(True, linewidth=1.5, alpha=0.5)
        
        # Make axis lines thicker
        plt.gca().spines['bottom'].set_linewidth(1.5)
        plt.gca().spines['left'].set_linewidth(1.5)
        plt.gca().spines['top'].set_linewidth(1.5)
        plt.gca().spines['right'].set_linewidth(1.5)
        
        # Set y-axis limits
        max_y = max(successful_red/total_red, successful_blue/total_blue)
        plt.ylim(0, max(0.5, max_y + 0.05))
        
        plt.tight_layout()
        
        plt.savefig('./CCDF/ccdf.pdf', format='pdf', dpi=300, bbox_inches='tight')
        plt.show()
        
        # Save the plot as a PNG file to plots/validation directory
        output_dir = os.path.join(current_dir, "plots", "validation")
        plt.savefig(os.path.join(output_dir, 'ccdf.png'), dpi=300, bbox_inches='tight')
        print(f"CCDF plot saved to: \n{os.path.join(output_dir, 'ccdf.png')}")
