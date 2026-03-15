import numpy as np
import matplotlib.pyplot as plt

np.set_printoptions(precision=3, suppress=True)

print("--- Question 4: Matrix and Polynomial Operations ---")

print("\n--- Part 1: Matrix Manipulation ---")

A = np.array([[8, -3],
              [12, 5],
              [5, 9]])

B = np.array([[11, 10],
              [-6, 15]])

print("Matrix A (3x2):\n", A)
print("\nMatrix B (2x2):\n", B)

AB = A @ B
print("\nProduct (A @ B):\n", AB)

LHS = AB.T
print("\nLHS (AB)ᵀ:\n", LHS)

RHS = B.T @ A.T
print("\nRHS (Bᵀ @ Aᵀ):\n", RHS)

is_equal = np.allclose(LHS, RHS)
print(f"\nProperty (AB)ᵀ = Bᵀ Aᵀ is: {is_equal}")

print("\n--- Part 2: Polynomial Operations ---")

p = [5, -4, 0, 0, 3, -2]
print(f"\np(x) coefficients: {p}")

q = [1, 0, -4, 3]
print(f"q(x) coefficients: {q}")

product_pq = np.convolve(p, q)
print("\nProduct p(x)q(x) coefficients:\n", product_pq)

quotient, remainder = np.polydiv(p, q)
print("\nDivision p(x) / q(x):")
print("  Quotient coefficients: ", quotient)
print("  Remainder coefficients: ", remainder)

roots_p = np.roots(p)
print("\nRoots of p(x) (both real and complex):\n", roots_p)

print("\nGenerating and saving plots...")

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))
fig.suptitle('Polynomial Plots', fontsize=16)

x_p = np.arange(0, 16, 3)
y_p = np.polyval(p, x_p)
ax1.plot(x_p, y_p, 'bo-', label='p(x) = 5x^5 - 4x^4 + 3x - 2')
ax1.set_title('Plot of p(x) at discrete points (x = 0, 3, ..., 15)')
ax1.set_xlabel('x')
ax1.set_ylabel('p(x)')
ax1.set_xlim(0, 15)
ax1.set_xticks(np.arange(0, 16, 3))
ax1.legend()
ax1.grid(True)

step = 0.02
num_points = int(round(15.0 / step)) + 1
x_q = np.linspace(0.0, 15.0, num_points)
y_q = np.polyval(q, x_q)
ax2.plot(x_q, y_q, 'r-', label='q(x) = x^3 - 4x + 3')
ax2.set_title('Plot of q(x) for x ∈ [0, 15] (step = 0.02)')
ax2.set_xlabel('x')
ax2.set_ylabel('q(x)')
ax2.set_xlim(0, 15)
ax2.set_xticks(np.arange(0, 16, 1))
ax2.legend()
ax2.grid(True)

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plot_file = 'polynomial_plots_tick15.png'
fig.savefig(plot_file)
print(f"Plots saved successfully as '{plot_file}'")

plt.show()

print("\n--- Script Finished ---")
