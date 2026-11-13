
"""
MachFlow - Validation Module
Engineering Checks for Diffuser Calculations
"""

import math


def validate_subsonic_result(result):
    checks = {}

    checks["Inlet Mach is subsonic"] = (
        0 < result["inlet_mach"] < 1
    )

    checks["Exit Mach is subsonic"] = (
        0 < result["exit_mach"] < 1
    )

    checks["Exit Mach is lower than inlet Mach"] = (
        result["exit_mach"] < result["inlet_mach"]
    )

    checks["Diffuser area ratio is greater than 1"] = (
        result["area_ratio"] > 1
    )

    checks["Ideal total pressure recovery is valid"] = (
        math.isclose(
            result["ideal_total_pressure_recovery"],
            1.0,
            rel_tol=1e-8
        )
    )

    return checks


def validate_supersonic_result(result):
    checks = {}

    checks["Inlet Mach is supersonic"] = (
        result["inlet_mach"] > 1
    )

    checks["Mach after shock is subsonic"] = (
        0 < result["mach_after_shock"] < 1
    )

    checks["Exit Mach is subsonic"] = (
        0 < result["exit_mach"] < 1
    )

    checks["Shock pressure ratio is greater than 1"] = (
        result["shock_pressure_ratio"] > 1
    )

    checks["Total pressure recovery is between 0 and 1"] = (
        0 < result["total_pressure_recovery"] <= 1
    )

    checks["Exit pressure ratio is positive"] = (
        result["exit_to_inlet_static_pressure_ratio"] > 0
    )

    return checks


def print_validation(title, checks):
    print(f"\n{title}")
    print("-" * 45)

    for description, passed in checks.items():
        status = "PASS" if passed else "FAIL"
        print(f"[{status}] {description}")

    total = len(checks)
    passed_count = sum(checks.values())

    print("-" * 45)
    print(f"Validation Score: {passed_count}/{total}")

    return passed_count == total


if __name__ == "__main__":

    from diffuser import (
        analyze_subsonic_diffuser,
        analyze_supersonic_diffuser
    )

    print("\n===================================")
    print("      MACHFLOW VALIDATION")
    print("===================================")

    subsonic = analyze_subsonic_diffuser(0.5, 1.5)
    supersonic = analyze_supersonic_diffuser(2.0, 1.5)

    subsonic_valid = print_validation(
        "1. SUBSONIC DIFFUSER CHECKS",
        validate_subsonic_result(subsonic)
    )

    supersonic_valid = print_validation(
        "2. SUPERSONIC DIFFUSER CHECKS",
        validate_supersonic_result(supersonic)
    )

    print("\n===================================")

    if subsonic_valid and supersonic_valid:
        print("ALL VALIDATION CHECKS PASSED")
    else:
        print("SOME VALIDATION CHECKS FAILED")

    print("===================================")
