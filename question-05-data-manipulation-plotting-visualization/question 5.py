import numpy as np
import matplotlib.pyplot as plt

print("--- Question 5: Data Manipulation, Plotting, and Visualization ---")

print("\n--- Part 1: Matrix Manipulation ---")

M = np.array([[2, 3, 4],
              [5, 6, 7],
              [8, 9, 10]])

print("Original Matrix M:\n", M)

V = M[:, 2]
print("\nVector V (Third Column):\n", V)

W = M[0, :]
print("\nVector W (First Row):\n", W)

col_max = np.max(M, axis=0)
col_min = np.min(M, axis=0)
print(f"\nMaximum of each column: {col_max}")
print(f"Minimum of each column: {col_min}")

row_max = np.max(M, axis=1)
row_min = np.min(M, axis=1)
print(f"\nMaximum of each row: {row_max}")
print(f"Minimum of each row: {row_min}")

print("\n--- Part 2: Generating and Saving Plots ---")

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 12))
fig.suptitle('Function Plots', fontsize=16)

x_linear = np.linspace(0, 120, 100)
y_linear = x_linear

ax1.plot(x_linear, y_linear, 'g-')
ax1.set_title('Plot 1: Linear Function (y = x)')
ax1.set_xlabel('X Axis')
ax1.set_ylabel('Y Axis')
ax1.axis([0, 120, 0, 120])
ax1.grid(True)

x_complex = np.linspace(0, 4 * np.pi, 200)
y_real = np.sin(x_complex)
y_imag = np.cos(2 * x_complex)

ax2.plot(x_complex, y_real, 'b-', label='Real Part: sin(x)')
ax2.plot(x_complex, y_imag, 'r--', label='Imaginary Part: cos(2x)')
ax2.set_title('Plot 2: f(x) = sin(x) + i*cos(2x)')
ax2.set_xlabel('x (radians)')
ax2.set_ylabel('Function Value')
ax2.legend()
ax2.grid(True)
ax2.axis('tight')

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plot_file = 'data_visualization_plots.png'
fig.savefig(plot_file)
print(f"Plots saved successfully as '{plot_file}'")

plt.show()

print("\n--- Script Finished ---")
