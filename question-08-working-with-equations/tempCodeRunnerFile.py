import math

delta_Hv = 2.453e6
R_air = 461

def saturation_pressure(T):
    return 6.11 * math.exp((delta_Hv / R_air) * (1/273 - 1/T))

print(f"{'Temperature (°F)':>18} | {'Saturation Vapour Pressure P0 (mbar)':>35}")
print("-" * 60)

for F in range(-60, 121, 10):
    T = (F - 32) * 5/9 + 273.15
    P0 = saturation_pressure(T)
    print(f"{F:>18} | {P0:>35.4f}")
