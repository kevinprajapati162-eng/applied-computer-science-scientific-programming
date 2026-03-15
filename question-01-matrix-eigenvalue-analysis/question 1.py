import numpy as np
import time

np.set_printoptions(precision=1, suppress=True)

def custom_inverse(M):
    start_time = time.perf_counter()
    if not isinstance(M, np.ndarray) or M.ndim != 2:
        raise ValueError("Input must be a 2D numpy array.")
    n, m = M.shape
    if n != m:
        raise ValueError("Input must be a square matrix.")
    aug = np.hstack([M.astype(float), np.eye(n)])
    try:
        for i in range(n):
            pivot_row = i
            for k in range(i + 1, n):
                if abs(aug[k, i]) > abs(aug[pivot_row, i]):
                    pivot_row = k
            if pivot_row != i:
                aug[[i, pivot_row]] = aug[[pivot_row, i]]
            pivot_val = aug[i, i]
            if abs(pivot_val) < 1e-12:
                raise np.linalg.LinAlgError("Matrix is singular and cannot be inverted.")
            aug[i, :] /= pivot_val
            for j in range(n):
                if i != j:
                    factor = aug[j, i]
                    if factor != 0:
                        aug[j, :] -= factor * aug[i, :]
        M_inv = aug[:, n:]
    except np.linalg.LinAlgError:
        raise
    except Exception as e:
        raise RuntimeError(f"Unexpected error during inversion: {e}")
    finally:
        elapsed = time.perf_counter() - start_time
    return M_inv

def calculate_D_and_eigen(A, B, C):
    for M, name in [(A, 'A'), (B, 'B'), (C, 'C')]:
        if not isinstance(M, np.ndarray) or M.ndim != 2:
            raise ValueError(f"Input {name} must be a 2D numpy array.")
    if not A.shape[0] == A.shape[1] or A.shape != B.shape or A.shape != C.shape:
        raise ValueError("All input matrices must have the same square dimensions.")
    print("(a) Compatibility checks passed successfully.")
    try:
        print("(b) Performing operations: D = (3*A^2*B - 2*B^T*C + I)^3 ...")
        I = np.eye(A.shape[0])
        A_squared = np.linalg.matrix_power(A, 2)
        B_transpose = B.T
        M = 3 * (A_squared @ B) - 2 * (B_transpose @ C) + I
        D = np.linalg.matrix_power(M, 3)
        print("(b) Calculation of D complete.")
        print("(c) Calculating eigenvalues and eigenvectors of D...")
        eigenvalues, eigenvectors = np.linalg.eig(D)
        return D, eigenvalues, eigenvectors
    except np.linalg.LinAlgError as e:
        print(f"A linear algebra error occurred during calculation: {e}")
        return None, None, None
    except Exception as e:
        print(f"Unexpected error during D calculation: {e}")
        return None, None, None

def analyze_D(D, inversion_function):
    try:
        print("(d) Using custom matrix inversion function to find D⁻¹...")
        start = time.perf_counter()
        D_inv = inversion_function(D)
        inversion_time = time.perf_counter() - start
        print(f"(d) Custom inversion complete in {inversion_time:.6f} seconds.")
        print("(e) Computing L2 condition number...")
        norm_D = np.linalg.norm(D, ord=2)
        norm_D_inv = np.linalg.norm(D_inv, ord=2)
        cond_num = norm_D * norm_D_inv
        print("(f) Calculating trace of D⁻¹...")
        trace_D_inv = np.trace(D_inv)
        return cond_num, trace_D_inv, inversion_time
    except np.linalg.LinAlgError as e:
        print(f"(d) Error: Matrix is singular or nearly singular: {e}")
        return np.inf, np.nan, None
    except Exception as e:
        print(f"(d) Unexpected error during analysis: {e}")
        return np.inf, np.nan, None

print("\n--- Demonstration with 4x4 Matrices ---")
np.random.seed(42)
A_ex = np.round(np.random.rand(4, 4), 1)
B_ex = np.round(np.random.rand(4, 4), 1)
C_ex = np.round(np.random.rand(4, 4), 1)
print("Input Matrix A:\n", A_ex)
print("\nInput Matrix B:\n", B_ex)
print("\nInput Matrix C:\n", C_ex)
print("\n--- Running Function 1: calculate_D_and_eigen ---")
D_res, eigvals, eigvecs = calculate_D_and_eigen(A_ex, B_ex, C_ex)
if D_res is not None:
    print("\nResulting Matrix D (from part b):\n", D_res)
    print("\n(c) Eigenvalues of D:\n", eigvals)
    print("\n(c) Eigenvectors of D:\n", eigvecs)
    print("\n--- Running Function 2: analyze_D ---")
    cond_num_res, trace_inv_res, inv_time = analyze_D(D_res, custom_inverse)
    print("\n--- Final Results ---")
    print(f"(e) L2 Condition Number of D: {cond_num_res:.6g}")
    if not np.isnan(trace_inv_res):
        print(f"(f) Trace of D⁻¹: {trace_inv_res:.6g}")
    else:
        print("(f) Trace of D⁻¹: NaN (inverse not available)")
    if inv_time is not None:
        print(f"Inversion time: {inv_time:.6f} seconds")
print("\nTime complexity of custom_inverse: O(n^3) time, O(n^2) space")
print("\n--- (a) Demonstration of Error Handling ---")
print("\nTest 1: (a) Error Handling for Incompatible Dimensions")
try:
    A_bad = np.random.rand(4, 3)
    calculate_D_and_eigen(A_bad, B_ex, C_ex)
except ValueError as e:
    print(f"Caught expected error: {e}")
print("\nTest 2: (a/d) Error Handling for Singular Matrix in custom_inverse")
D_singular = np.array([[1, 2, 3, 4],
                       [5, 6, 7, 8],
                       [9, 10, 11, 12],
                       [13, 14, 15, 16]], dtype=float)
cond_num_sing, trace_inv_sing, inv_time_sing = analyze_D(D_singular, custom_inverse)
print(f"Condition Number (Singular): {cond_num_sing}")
print(f"Trace of Inverse (Singular): {trace_inv_sing}")
