import numpy as np
import matplotlib.pyplot as plt

# First Graph: Cost per Unit vs Unit Manufactured (Volume)
fig, ax = plt.subplots(1, 2, figsize=(14, 6))

# Data for first graph
volume = np.linspace(1, 100, 500)
conv_cost = 100 / volume + 10  # Higher initial cost, decreases with volume
add_cost = np.ones_like(volume) * 20  # Constant cost per unit

# Plotting first graph
ax[0].plot(volume, conv_cost, label="Conventional Manufacturing", color='blue')
ax[0].plot(volume, add_cost, label="Additive Manufacturing", color='green', linestyle='--')
ax[0].axvline(x=30, color='yellow', linestyle=':', label='Breakeven Point')  # Approximate breakeven point
ax[0].set_title("Cost per Unit vs Volume")
ax[0].set_xlabel("Units Manufactured (Volume)")
ax[0].set_ylabel("Cost per Unit")
ax[0].legend()
ax[0].grid(True)

# Second Graph: Cost per Piece vs Geometric Complexity
complexity = np.linspace(1, 100, 500)
conv_cost_complexity = 0.1 * complexity ** 2  # Quadratic increase in cost
add_cost_complexity = np.ones_like(complexity) * 50  # Constant cost for Additive Manufacturing

# Plotting second graph
ax[1].plot(complexity, conv_cost_complexity, label="Conventional Manufacturing", color='blue')
ax[1].plot(complexity, add_cost_complexity, label="Additive Manufacturing", color='green', linestyle='--')
ax[1].axvline(x=50, color='red', linestyle=':', label='Complexity Break-even')  # Approximate complexity break-even
ax[1].set_title("Manufacturing Cost vs Geometric Complexity")
ax[1].set_xlabel("Geometric Complexity")
ax[1].set_ylabel("Manufacturing Cost per Piece")
ax[1].legend()
ax[1].grid(True)

# Show plots
plt.tight_layout()
plt.show()
