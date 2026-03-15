import numpy as np
import matplotlib.pyplot as plt

print("--- Question 6: Advanced Plotting and Code Efficiency ---")

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 12))
fig.suptitle('Advanced Plotting', fontsize=16)

print("Generating Plot 1 (Polynomial)...")

p = [4, 3, -120, 3, -8, 110]

x_p = np.arange(-7, 7.02, 0.02)

y_p = np.polyval(p, x_p)

ax1.plot(x_p, y_p, 'b-', label='p(x) = 4x⁵ + 3x⁴ - 120x³ + ...')
ax1.set_title('Section 1: Plot of Polynomial p(x)')
ax1.set_xlabel('x')
ax1.set_ylabel('p(x)')
ax1.legend()
ax1.grid(True)
ax1.set_xlim([-7, 7])

print("Generating Plot 2 (Hyperbolic Function)...")

x_h = np.arange(-5, 5.02, 0.02)

y_sinh = np.sinh(x_h)

ax2.plot(x_h, y_sinh, 'r-', label='y = sinh(x)')

ax2.set_title('Section 2: Plot of a Hyperbolic Function')
ax2.set_xlabel('x')
ax2.set_ylabel('Function Value')
ax2.legend()
ax2.grid(True)
ax2.set_xlim([-5, 5])

plt.tight_layout(rect=[0, 0.03, 1, 0.95])

plot_file = 'advanced_plotting.png'
fig.savefig(plot_file)
print(f"Plots saved successfully as '{plot_file}'")

plt.show()

print("\n--- Script Finished ---")
