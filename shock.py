
"""
MachFlow - Shock Calculation Module

Normal Shock and Oblique Shock Analysis
"""

import math
from scipy.optimize import brentq, minimize_scalar

from calculations import normal_shock


# ------------------------------------------
# 1. MACH ANGLE
# ------------------------------------------

def mach_angle(mach1):

    if mach1 <= 1:
        raise ValueError("Mach number must be greater than 1")

    return math.degrees(math.asin(1 / mach1))


# ------------------------------------------
# 2. THETA-BETA-M RELATION
# ------------------------------------------

def theta_beta_m(beta, mach1, gamma=1.4):

    numerator = 2 / math.tan(beta) * (
        mach1**2 * math.sin(beta)**2 - 1
    )

    denominator = (
        mach1**2 * (gamma + math.cos(2 * beta)) + 2
    )

    return math.atan(numerator / denominator)


# ------------------------------------------
# 3. MAXIMUM DEFLECTION ANGLE
# ------------------------------------------

def maximum_deflection(mach1, gamma=1.4):

    if mach1 <= 1 or gamma <= 1:
        raise ValueError("Invalid Mach number or gamma")

    beta_min = math.asin(1 / mach1) + 1e-8
    beta_max = math.pi / 2 - 1e-8

    result = minimize_scalar(
        lambda beta: -theta_beta_m(beta, mach1, gamma),
        bounds=(beta_min, beta_max),
        method="bounded"
    )

    return math.degrees(-result.fun)


# ------------------------------------------
# 4. OBLIQUE SHOCK CALCULATION
# ------------------------------------------

def oblique_shock(mach1, theta_deg, gamma=1.4,
                  branch="weak"):

    if mach1 <= 1:
        raise ValueError("Upstream Mach must be greater than 1")

    if gamma <= 1:
        raise ValueError("Gamma must be greater than 1")

    if theta_deg <= 0:
        raise ValueError("Deflection angle must be positive")

    if branch not in ("weak", "strong"):
        raise ValueError("Branch must be weak or strong")

    theta = math.radians(theta_deg)

    beta_min = math.asin(1 / mach1) + 1e-8
    beta_max = math.pi / 2 - 1e-8

    max_theta = maximum_deflection(mach1, gamma)

    if theta_deg >= max_theta:
        raise ValueError(
            f"No attached oblique shock. "
            f"Maximum deflection is approximately "
            f"{max_theta:.4f} degrees."
        )

    peak = minimize_scalar(
        lambda beta: -theta_beta_m(beta, mach1, gamma),
        bounds=(beta_min, beta_max),
        method="bounded"
    )

    beta_peak = peak.x

    equation = lambda beta: (
        theta_beta_m(beta, mach1, gamma) - theta
    )

    if branch == "weak":
        beta = brentq(
            equation, beta_min, beta_peak
        )
    else:
        beta = brentq(
            equation, beta_peak, beta_max
        )

    # Normal component of upstream Mach
    mach_normal_1 = mach1 * math.sin(beta)

    # Apply normal shock equations
    normal = normal_shock(mach_normal_1, gamma)

    mach_normal_2 = normal["mach2"]

    # Downstream Mach number
    mach2 = mach_normal_2 / math.sin(beta - theta)

    return {
        "mach1": mach1,
        "mach2": mach2,
        "deflection_angle_deg": theta_deg,
        "shock_angle_deg": math.degrees(beta),
        "mach_angle_deg": mach_angle(mach1),
        "normal_mach1": mach_normal_1,
        "normal_mach2": mach_normal_2,
        "pressure_ratio": normal["pressure_ratio"],
        "density_ratio": normal["density_ratio"],
        "temperature_ratio": normal["temperature_ratio"],
        "total_pressure_recovery":
            normal["total_pressure_recovery"],
        "shock_branch": branch,
        "maximum_deflection_deg": max_theta
    }


# ------------------------------------------
# 5. TESTING
# ------------------------------------------

if __name__ == "__main__":

    print("\n================================")
    print("       MACHFLOW SHOCK MODULE")
    print("================================")

    mach = 2.0
    theta = 10.0

    print("\n1. Mach Angle")

    print(f"Mach Angle: {mach_angle(mach):.4f} degrees")

    print("\n2. Maximum Deflection")

    print(
        f"Maximum Deflection: "
        f"{maximum_deflection(mach):.4f} degrees"
    )

    print("\n3. Weak Oblique Shock")

    result = oblique_shock(
        mach1=2.0,
        theta_deg=10.0,
        branch="weak"
    )

    for key, value in result.items():

        if isinstance(value, float):
            print(f"{key}: {value:.6f}")
        else:
            print(f"{key}: {value}")

    print("\n================================")
    print("      SHOCK CALCULATIONS DONE")
    print("================================")
