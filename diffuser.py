
"""
MachFlow - Diffuser Module
Subsonic and Supersonic Diffuser Analysis
"""

from calculations import (
    subsonic_diffuser,
    normal_shock,
    area_mach,
    solve_mach,
    isentropic_pressure
)


def analyze_subsonic_diffuser(mach_inlet, area_ratio, gamma=1.4):
    """Analyze an ideal subsonic diffuser."""
    return subsonic_diffuser(
        mach_inlet,
        area_ratio,
        gamma
    )


def analyze_supersonic_diffuser(mach_inlet, area_ratio, gamma=1.4):
    """
    Idealized supersonic diffuser:
    1. Normal shock at constant area
    2. Subsonic diffusion after the shock
    """

    if mach_inlet <= 1:
        raise ValueError("Supersonic inlet Mach must be greater than 1")

    if area_ratio <= 1:
        raise ValueError("Exit-to-inlet area ratio must be greater than 1")

    # Step 1: Normal shock at diffuser inlet
    shock = normal_shock(mach_inlet, gamma)

    mach_after_shock = shock["mach2"]

    # Step 2: Area-Mach relation after the shock
    inlet_area_astar = area_mach(mach_after_shock, gamma)

    exit_area_astar = area_ratio * inlet_area_astar

    # Step 3: Calculate exit Mach number
    mach_exit = solve_mach(
        exit_area_astar,
        branch="subsonic",
        gamma=gamma
    )

    # Step 4: Static pressure calculation
    p1_p01 = isentropic_pressure(mach_inlet, gamma)

    # Normal shock pressure ratio
    p2_p1 = shock["pressure_ratio"]

    # Isentropic pressure ratio after the shock
    p3_p02 = isentropic_pressure(mach_exit, gamma)

    # Total pressure after shock relative to inlet total pressure
    p02_p01 = shock["total_pressure_recovery"]

    p3_p01 = p3_p02 * p02_p01

    return {
        "inlet_mach": mach_inlet,
        "mach_after_shock": mach_after_shock,
        "exit_mach": mach_exit,
        "area_ratio": area_ratio,
        "shock_pressure_ratio": p2_p1,
        "total_pressure_recovery": p02_p01,
        "inlet_static_pressure_over_total": p1_p01,
        "exit_static_pressure_over_inlet_total": p3_p01,
        "exit_to_inlet_static_pressure_ratio": p3_p01 / p1_p01,
        "flow_type": "Supersonic diffuser with inlet normal shock"
    }


if __name__ == "__main__":

    print("\n===================================")
    print("       MACHFLOW DIFFUSER MODULE")
    print("===================================")

    print("\n1. SUBSONIC DIFFUSER")

    subsonic = analyze_subsonic_diffuser(
        mach_inlet=0.5,
        area_ratio=1.5
    )

    for key, value in subsonic.items():
        print(f"{key}: {value:.6f}")

    print("\n2. SUPERSONIC DIFFUSER")

    supersonic = analyze_supersonic_diffuser(
        mach_inlet=2.0,
        area_ratio=1.5
    )

    for key, value in supersonic.items():
        if isinstance(value, float):
            print(f"{key}: {value:.6f}")
        else:
            print(f"{key}: {value}")

    print("\n===================================")
    print("      DIFFUSER ANALYSIS DONE")
    print("===================================")
