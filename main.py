
"""
MachFlow - Diffuser Simulator
Main Streamlit Application
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from report_generator import generate_pdf_report

from diffuser import (
    analyze_subsonic_diffuser,
    analyze_supersonic_diffuser
)

from validation import (
    validate_subsonic_result,
    validate_supersonic_result
)


# --------------------------------
# PAGE CONFIGURATION
# --------------------------------

st.set_page_config(
    page_title="MachFlow - Diffuser Simulator",
    page_icon="✈️",
    layout="wide"
)

st.title("✈️ MachFlow - Diffuser Simulator")

st.markdown(
    "### Engineering Analysis of Subsonic and Supersonic Diffusers"
)

st.write(
    "MachFlow calculates ideal diffuser flow properties "
    "using isentropic flow relations and normal shock equations."
)

st.divider()


# --------------------------------
# SIDEBAR INPUTS
# --------------------------------

st.sidebar.header("Simulation Parameters")

flow_type = st.sidebar.selectbox(
    "Select Diffuser Type",
    ["Subsonic Diffuser", "Supersonic Diffuser"]
)

gamma = st.sidebar.number_input(
    "Specific Heat Ratio (γ)",
    min_value=1.01,
    max_value=2.0,
    value=1.4,
    step=0.01
)

if flow_type == "Subsonic Diffuser":

    mach_inlet = st.sidebar.number_input(
        "Inlet Mach Number",
        min_value=0.01,
        max_value=0.99,
        value=0.5,
        step=0.05
    )

else:

    mach_inlet = st.sidebar.number_input(
        "Inlet Mach Number",
        min_value=1.01,
        max_value=5.0,
        value=2.0,
        step=0.1
    )

area_ratio = st.sidebar.number_input(
    "Exit Area / Inlet Area",
    min_value=1.01,
    max_value=10.0,
    value=1.5,
    step=0.1
)

calculate = st.sidebar.button(
    "Calculate Diffuser",
    type="primary",
    use_container_width=True
)


# --------------------------------
# CALCULATION
# --------------------------------

if calculate:

    try:

        if flow_type == "Subsonic Diffuser":

            result = analyze_subsonic_diffuser(
                mach_inlet,
                area_ratio,
                gamma
            )

            checks = validate_subsonic_result(result)

        else:

            result = analyze_supersonic_diffuser(
                mach_inlet,
                area_ratio,
                gamma
            )

            checks = validate_supersonic_result(result)

        st.session_state["result"] = result
        st.session_state["checks"] = checks
        st.session_state["flow_type"] = flow_type
        st.session_state["inputs"] = {
    "inlet_mach": mach_inlet,
    "area_ratio": area_ratio,
    "gamma": gamma
}

    except Exception as error:

        st.error(f"Calculation Error: {error}")


# --------------------------------
# DISPLAY RESULTS
# --------------------------------

if "result" in st.session_state:

    result = st.session_state["result"]
    checks = st.session_state["checks"]
    selected_type = st.session_state["flow_type"]

    st.subheader("Simulation Results")

    if selected_type == "Subsonic Diffuser":

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Inlet Mach Number",
            f'{result["inlet_mach"]:.4f}'
        )

        col2.metric(
            "Exit Mach Number",
            f'{result["exit_mach"]:.4f}'
        )

        col3.metric(
            "Static Pressure Ratio",
            f'{result["static_pressure_ratio"]:.4f}'
        )

    else:

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Inlet Mach Number",
            f'{result["inlet_mach"]:.4f}'
        )

        col2.metric(
            "Mach After Shock",
            f'{result["mach_after_shock"]:.4f}'
        )

        col3.metric(
            "Exit Mach Number",
            f'{result["exit_mach"]:.4f}'
        )

    st.divider()

    # --------------------------------
    # DETAILED RESULTS TABLE
    # --------------------------------

    st.subheader("Detailed Engineering Results")

    result_table = pd.DataFrame(
        [
            {"Parameter": key, "Calculated Value": value}
            for key, value in result.items()
        ]
    )

    st.dataframe(
        result_table,
        use_container_width=True,
        hide_index=True
    )

    # --------------------------------
    # MACH NUMBER GRAPH
    # --------------------------------

    st.subheader("Mach Number Distribution")

    if selected_type == "Subsonic Diffuser":

        positions = ["Inlet", "Exit"]
        mach_values = [
            result["inlet_mach"],
            result["exit_mach"]
        ]

    else:

        positions = [
            "Inlet",
            "After Normal Shock",
            "Exit"
        ]

        mach_values = [
            result["inlet_mach"],
            result["mach_after_shock"],
            result["exit_mach"]
        ]

    fig, ax = plt.subplots(figsize=(9, 4))

    ax.plot(
        positions,
        mach_values,
        marker="o",
        linewidth=2
    )

    ax.axhline(
        y=1.0,
        linestyle="--",
        label="Mach 1"
    )

    ax.set_title("Mach Number at Key Diffuser Stations")
    ax.set_xlabel("Flow Station")
    ax.set_ylabel("Mach Number")
    ax.grid(True)
    ax.legend()

    st.pyplot(fig)
    plt.close(fig)

    st.caption(
        "This plot connects calculated station values for comparison. "
        "It is not a spatially resolved flow-field solution."
    )

    # --------------------------------
    # VALIDATION
    # --------------------------------

    st.subheader("Engineering Validation")

    passed = 0

    for description, status in checks.items():

        if status:
            st.success(f"PASS - {description}")
            passed += 1

        else:
            st.error(f"FAIL - {description}")

    st.write(
        f"Validation Score: {passed}/{len(checks)}"
    )

    if passed == len(checks):
        st.success("All validation checks passed.")

    st.divider()

    st.info(
        "Note: This version uses idealized one-dimensional "
        "compressible-flow models. Real diffuser performance "
        "also depends on friction, boundary-layer growth, "
        "flow separation and shock interactions."
    )

else:

    st.info(
        "Select the diffuser type and enter the simulation "
        "parameters in the sidebar. Click Calculate Diffuser "
        "to begin."
    )

    st.subheader("MachFlow Modules")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Subsonic Diffuser**")
        st.write("Calculates ideal subsonic flow deceleration.")

    with col2:
        st.markdown("**Supersonic Diffuser**")
        st.write("Models an inlet normal shock followed by subsonic diffusion.")
    # --------------------------------
# PDF REPORT GENERATION
# --------------------------------

if "result" in st.session_state:

    st.divider()

    st.subheader("PDF Report Generation")

    pdf_data = generate_pdf_report(
        st.session_state["result"],
        st.session_state["checks"],
        st.session_state["flow_type"],
        st.session_state["inputs"]
    )

    st.download_button(
    label="Download Simulation Report (PDF)",
    data=pdf_data,
    file_name="MachFlow_Simulation_Report.pdf",
    mime="application/pdf",
    use_container_width=True,
    key="machflow_pdf_download"
)
    

   