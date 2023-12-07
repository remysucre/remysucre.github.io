import matplotlib.pyplot as plt
import numpy as np

# Define the range for x and y
x = np.linspace(0, 2, 400)
y = np.linspace(0, 2, 400)

# Create meshgrid for x and y
X, Y = np.meshgrid(x, y)

# Define the constraints
constraint1 = X + Y <= 2
constraint2 = Y <= 1.5
constraint3 = X <= 1.5

# Combine the constraints
feasible_region = constraint1 & constraint2 & constraint3

# Plotting
plt.figure(figsize=(8, 6))
plt.imshow(feasible_region, extent=(0, 2, 0, 2), origin='lower', cmap='Blues', alpha=0.3)

# Adding the constraints as lines
plt.plot(x, 2 - x, label=r'$x + y \leq 2$')  # x + y <= 2
plt.axhline(y=1.5, label=r'$y \leq 1.5$')  # y <= 1.5
plt.axvline(x=1.5, label=r'$x \leq 1.5$')  # x <= 1.5

plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.xticks([])
plt.yticks([])

# Labels and legend
# plt.xlabel('x')
# plt.ylabel('y')
# plt.legend()
# plt.grid(True)
# plt.show()
plt.tight_layout()
plt.savefig('lin-con.png')
