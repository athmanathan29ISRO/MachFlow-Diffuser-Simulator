
"""
MachFlow - Diffuser Simulator
Main Engineering Calculation Engine

Author: MachFlow Development Team
Purpose: Compressible flow calculations
"""

import math
from scipy.optimize import brentq

# ------------------------------------------
# CONSTANTS
# ------------------------------------------

GAMMA_DEFAULT = 1.4


# ------------------------------------------
# 1. ISENTROPIC PRESSURE RELATION
# ------------------------------------------

def isentropic_pressure(mach, gamma=GAMMA_DEFAULT):

    if mach < 0:
        raise ValueError("Mach number cannot be negative")

    if gamma <= 1:
        raise ValueError("Gamma must be greater than 1")

    pressure_ratio = (
        1 + ((gamma - 1) / 2) * mach**2
    ) ** (-gamma / (gamma - 1))

    return pressure_ratio


# ------------------------------------------
# 2. AREA-MACH NUMBER RELATION
# ------------------------------------------

def area_mach(mach, gamma=GAMMA_DEFAULT):

    if mach <= 0:
        raise ValueError("Mach number must be positive")

    if gamma <= 1:
        raise ValueError("Gamma must be greater than 1")

    term = (2 / (gamma + 1)) * (
        1 + ((gamma - 1) / 2) * mach**2
    )

    exponent = (gamma + 1) / (2 * (gamma - 1))

    area_ratio = (1 / mach) * term**exponent

    return area_ratio


# ------------------------------------------
# 3. SOLVE MACH NUMBER FROM AREA RATIO
# ------------------------------------------

def solve_mach(area_ratio, branch="subsonic",
               gamma=GAMMA_DEFAULT):

    if area_ratio < 1:
        raise ValueError("Area ratio must be >= 1")

    if gamma <= 1:
        raise ValueError("Gamma must be greater than 1")

    if area_ratio == 1:
        return 1.0

    def equation(mach):
        return area_mach(mach, gamma) - area_ratio

    if branch == "subsonic":

        return brentq(
            equation,
            1e-10,
            1 - 1e-10
        )

    elif branch == "supersonic":

        upper = 2.0

        while equation(upper) < 0:
            upper *= 2

        return brentq(
            equation,
            1 + 1e-10,
            upper
        )

    else:
        raise ValueError(
            "Branch must be subsonic or supersonic"
        )


# ------------------------------------------
# 4. NORMAL SHOCK CALCULATIONS
# ------------------------------------------

def normal_shock(mach1, gamma=GAMMA_DEFAULT):

    if mach1 <= 1:
        raise ValueError(
            "Normal shock requires upstream Mach > 1"
        )

    if gamma <= 1:
        raise ValueError("Gamma must be greater than 1")

    mach2_squared = (
        1 + ((gamma - 1) / 2) * mach1**2
    ) / (
        gamma * mach1**2 - ((gamma - 1) / 2)
    )

    mach2 = math.sqrt(mach2_squared)

    pressure_ratio = (
        1 + (2 * gamma / (gamma + 1))
        * (mach1**2 - 1)
    )

    density_ratio = (
        ((gamma + 1) * mach1**2)
        /
        ((gamma - 1) * mach1**2 + 2)
    )

    temperature_ratio = (
        pressure_ratio / density_ratio
    )

    total_pressure_recovery = (
        pressure_ratio
        *
        (
            (1 + ((gamma - 1) / 2) * mach2**2)
            /
            (1 + ((gamma - 1) / 2) * mach1**2)
        ) ** (gamma / (gamma - 1))
    )

    return {
        "mach1": mach1,
        "mach2": mach2,
        "pressure_ratio": pressure_ratio,
        "density_ratio": density_ratio,
        "temperature_ratio": temperature_ratio,
        "total_pressure_recovery": total_pressure_recovery
    }


# ------------------------------------------
# 5. SUBSONIC DIFFUSER
# ------------------------------------------

def subsonic_diffuser(
    mach_inlet,
    area_exit_to_inlet,
    gamma=GAMMA_DEFAULT
):

    if not 0 < mach_inlet < 1:
        raise ValueError(
            "Subsonic inlet Mach must be between 0 and 1"
        )

    if area_exit_to_inlet <= 1:
        raise ValueError(
            "Diffuser exit area must exceed inlet area"
        )

    # Inlet area relative to sonic throat area
    inlet_area_ratio = area_mach(mach_inlet, gamma)

    # Exit area relative to sonic throat area
    exit_area_ratio = (
        area_exit_to_inlet * inlet_area_ratio
    )

    # Calculate exit Mach
    mach_exit = solve_mach(
        exit_area_ratio,
        branch="subsonic",
        gamma=gamma
    )

    # Static-to-total pressure ratios
    pressure_inlet = isentropic_pressure(
        mach_inlet, gamma
    )

    pressure_exit = isentropic_pressure(
        mach_exit, gamma
    )

    return {
        "inlet_mach": mach_inlet,
        "exit_mach": mach_exit,
        "area_ratio": area_exit_to_inlet,
        "inlet_area_over_astar": inlet_area_ratio,
        "exit_area_over_astar": exit_area_ratio,
        "pressure_inlet_over_total": pressure_inlet,
        "pressure_exit_over_total": pressure_exit,
        "static_pressure_ratio": pressure_exit / pressure_inlet,
        "ideal_total_pressure_recovery": 1.0
    }


# ------------------------------------------
# 6. BASIC TESTING
# ------------------------------------------

if __name__ == "__main__":

    print("\n===================================")
    print("       MACHFLOW SIMULATOR")
    print("  ENGINEERING CALCULATION ENGINE")
    print("===================================")

    print("\n1. ISENTROPIC PRESSURE")

    print(
        "P/P0 =",
        round(isentropic_pressure(0.5), 6)
    )

    print("\n2. AREA-MACH RELATION")

    print(
        "A/A* =",
        round(area_mach(0.5), 6)
    )

    print("\n3. SUBSONIC DIFFUSER")

    diffuser = subsonic_diffuser(0.5, 1.5)

    for key, value in diffuser.items():
        print(f"{key}: {value:.6f}")

    print("\n4. NORMAL SHOCK")

    shock = normal_shock(3.0)

    for key, value in shock.items():
        print(f"{key}: {value:.6f}")

    print("\n===================================")
    print("       CALCULATIONS COMPLETED")
    print("===================================")
