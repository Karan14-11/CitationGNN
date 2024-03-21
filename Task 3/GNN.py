import matplotlib.pyplot as plt

# Threshold values
thresholds = [-0.5, -0.45, -0.4, -0.35, -0.3, -0.25, -0.2, -0.15, -0.1, -0.05, 0.0, 0.05]

# Corresponding accuracy values
accuracies = [89.70, 89.50, 89.33, 97.12, 96.59, 96.11, 95.66, 94.81, 94.12, 93.59, 92.86, 92.46]

# Plotting
plt.plot(thresholds, accuracies, marker='o', linestyle='-', color='b')
plt.title('Threshold vs. Accuracy')
plt.xlabel('Threshold')
plt.ylabel('Accuracy (%)')
plt.grid(True)
# plt.show()
plt.savefig("GNN.png", format = "png")
