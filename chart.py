import re
import matplotlib.pyplot as plt

# The text data containing the training history
log_data = """
--------------------------------------------------------------------------------
Epoch 0001 | Train Loss: 0.2239 | Val Loss: 0.2090 | Perfect Match Accuracy: 0.00% | Learning Rate: 0.001000
  -->  New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0002 | Train Loss: 0.2014 | Val Loss: 0.1893 | Perfect Match Accuracy: 0.00% | Learning Rate: 0.001000
Epoch 0003 | Train Loss: 0.1935 | Val Loss: 0.1905 | Perfect Match Accuracy: 0.00% | Learning Rate: 0.001000
Epoch 0004 | Train Loss: 0.1917 | Val Loss: 0.1914 | Perfect Match Accuracy: 0.00% | Learning Rate: 0.001000
Epoch 0005 | Train Loss: 0.1953 | Val Loss: 0.1899 | Perfect Match Accuracy: 0.00% | Learning Rate: 0.001000
Epoch 0006 | Train Loss: 0.1934 | Val Loss: 0.1930 | Perfect Match Accuracy: 0.00% | Learning Rate: 0.001000
Epoch 0007 | Train Loss: 0.1944 | Val Loss: 0.1893 | Perfect Match Accuracy: 0.00% | Learning Rate: 0.001000
"""

def parse_and_plot(text):
    epochs = []
    train_losses = []
    val_losses = []
    accuracies = []

    # Regex pattern to capture numbers dynamically
    pattern = re.compile(
        r"Epoch\s+(\d+)\s*\|\s*Train Loss:\s*([\d.]+)\s*\|\s*Val Loss:\s*([\d.]+)\s*\|\s*Perfect Match Accuracy:\s*([\d.]+)%"
    )

    # Process line by line iteratively
    for line in text.strip().split("\n"):
        match = pattern.search(line)
        if match:
            epoch = int(match.group(1))
            train_loss = float(match.group(2))
            val_loss = float(match.group(3))
            accuracy = float(match.group(4))

            epochs.append(epoch)
            train_losses.append(train_loss)
            val_losses.append(val_loss)
            accuracies.append(accuracy)

    # Building the Dual-Y-Axis Chart
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Left Y-Axis: Losses
    color_train = '#1f77b4'
    color_val = '#ff7f0e'
    ax1.set_xlabel('Epoch', fontweight='bold')
    ax1.set_ylabel('Loss', color='black', fontweight='bold')
    line1 = ax1.plot(epochs, train_losses, color=color_train, marker='o', label='Train Loss', linewidth=2)
    line2 = ax1.plot(epochs, val_losses, color=color_val, marker='s', label='Val Loss', linewidth=2)
    ax1.tick_params(axis='y', labelcolor='black')
    ax1.grid(True, linestyle='--', alpha=0.6)

    # Right Y-Axis: Accuracy (Since percentages are on a completely different scale than loss numbers)
    ax2 = ax1.twinx()  
    color_acc = '#2ca02c'
    ax2.set_ylabel('Perfect Match Accuracy (%)', color=color_acc, fontweight='bold')
    line3 = ax2.plot(epochs, accuracies, color=color_acc, marker='^', linestyle='--', label='Accuracy (%)', linewidth=2)
    ax2.tick_params(axis='y', labelcolor=color_acc)

    # Combine legends from both axes
    lines = line1 + line2 + line3
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='upper right')

    plt.title('Modulo Net VQ Training Performance History', fontsize=14, fontweight='bold', pad=15)
    fig.tight_layout()
    
    # Show the plot
    plt.show()

if __name__ == "__main__":
    parse_and_plot(log_data)