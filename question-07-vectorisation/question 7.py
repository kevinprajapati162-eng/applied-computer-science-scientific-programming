import numpy as np

print("--- Question 7: Vectorisation ---")

A_loop = np.zeros(1000)
B_loop = np.zeros(1000)
C_loop = np.empty(1000, dtype=object)
sum_val = 0

for i in range(1000):
    A_loop[i] = i + 1

for i in range(1000):
    sum_val = sum_val + A_loop[i]
    B_loop[i] = sum_val
    if B_loop[i] % 2 == 0:
        C_loop[i] = "Even"
    else:
        C_loop[i] = "Odd"

print("\n--- Non-Vectorized Results (Loop) ---")
print("A (first 10):", A_loop[:10])
print("B (first 10):", B_loop[:10])
print("C (first 10):", C_loop[:10])

print("\n--- Vectorized Results (NumPy) ---")

A_vec = np.arange(1, 1001)
B_vec = np.cumsum(A_vec)
condition = (B_vec % 2 == 0)
C_vec = np.where(condition, "Even", "Odd")

print("A (first 10):", A_vec[:10])
print("B (first 10):", B_vec[:10])
print("C (first 10):", C_vec[:10])

print("\nC (last 10):", C_vec[-10:])

print("\nVerification:")
print("A arrays are equal:", np.array_equal(A_loop, A_vec))
print("B arrays are equal:", np.array_equal(B_loop, B_vec))
print("C arrays are equal:", np.array_equal(C_loop, C_vec))
print("\n--- Script Finished ---")
