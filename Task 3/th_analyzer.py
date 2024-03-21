import matplotlib.pyplot as plt

# Your data
thresholds = [0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0]
predicted_edges = [627763, 491716, 337201, 248003, 164195, 108355, 59715, 29746, 13016, 5281, 1728, 613, 205, 48, 6, 0, 0, 0, 0, 0, 0]
accuracy = [0.13715367105101767, 0.12934295406291438, 0.12722382199341045, 30.17907209377686, 54.3245542814561, 70.8017279407809, 83.63667095592244, 91.51193185659238, 0.13060848186846957, 0.1893580761219466, 0.11574074074074073, 0.48939641109298526, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# Plotting
fig, ax1 = plt.subplots()

ax1.set_xlabel('Threshold')
ax1.set_ylabel('Predicted Edges', color='tab:blue')
ax1.plot(thresholds, predicted_edges, marker='o', linestyle='-', color='tab:blue')
ax1.tick_params(axis='y', labelcolor='tab:blue')

ax2 = ax1.twinx()
ax2.set_ylabel('Accuracy', color='tab:red')
ax2.plot(thresholds, accuracy, marker='x', linestyle=':', color='tab:red')
ax2.tick_params(axis='y', labelcolor='tab:red')

plt.title('Threshold vs Predicted Edges and Accuracy for FutureGraph')
plt.grid(True)
plt.savefig("node2vec_threshold.png")
plt.show()
