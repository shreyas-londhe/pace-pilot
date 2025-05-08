import streamlit as st


def calculate_run_pace(t_run_min, p_target_min_per_km, p_walk_min_per_km, t_walk_min):
    """
    Calculates the required pace for running segments in a run-walk-run strategy.

    Args:
        t_run_min (float): Duration of the running segment in minutes.
        p_target_min_per_km (float): Desired overall average pace in minutes per km.
        p_walk_min_per_km (float): Pace of the walking segments in minutes per km.
        t_walk_min (float): Duration of the walking segment in minutes.

    Returns:
        float: Required pace for running segments in minutes per km.
               Returns None if calculation is not possible (e.g., denominator issues).
    """
    try:
        numerator = t_run_min * p_target_min_per_km * p_walk_min_per_km
        denominator = (p_walk_min_per_km * (t_run_min + t_walk_min)) - (
            p_target_min_per_km * t_walk_min
        )

        if denominator <= 0:
            return None

        p_run_min_per_km = numerator / denominator
        return p_run_min_per_km
    except ZeroDivisionError:
        return None


def format_pace(decimal_minutes):
    """Converts decimal minutes to M'SS" format."""
    if decimal_minutes is None or decimal_minutes < 0:
        return "N/A"
    minutes = int(decimal_minutes)
    # Use round for better accuracy with seconds, especially after division
    seconds = int(round((decimal_minutes - minutes) * 60))
    if seconds == 60:  # Handle edge case where rounding pushes seconds to 60
        minutes += 1
        seconds = 0
    return f"{minutes}'{seconds:02d}\""  # Added closing quote for seconds


# --- Streamlit App ---
st.set_page_config(page_title="Pace Pilot", layout="wide")

st.title("🏃‍♂️💨 Pace Pilot")
st.markdown(
    """
    This tool helps you calculate the **running pace** needed during your run segments 
    to achieve an overall **target average pace** when using a run-walk-run strategy.
"""
)
st.markdown("---")

st.sidebar.header("About")
st.sidebar.info(
    """
    This calculator uses the following formula:
    `P_run = (T_run * P_target * P_walk) / ((P_walk * (T_run + T_walk)) - (P_target * T_walk))`

    Enter your desired run/walk durations and your target paces (in minutes and seconds per km) 
    to find the necessary pace for your running intervals.
"""
)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Your Run-Walk Strategy")

    st.markdown("**Running Segment Duration (T_run):**")
    run_dur_col1, run_dur_col2 = st.columns(2)
    with run_dur_col1:
        t_run_minutes = st.number_input(
            "Minutes",
            min_value=0,
            value=4,
            step=1,
            key="t_run_min",
            format="%d",
            help="Minutes for each running segment.",
        )
    with run_dur_col2:
        t_run_seconds = st.number_input(
            "Seconds",
            min_value=0,
            max_value=59,
            value=0,
            step=1,
            key="t_run_sec",
            format="%d",
            help="Seconds for each running segment (0-59).",
        )
    t_run_min_input = float(t_run_minutes) + (float(t_run_seconds) / 60.0)

    st.markdown("**Walking Segment Duration (T_walk):**")
    walk_dur_col1, walk_dur_col2 = st.columns(2)
    with walk_dur_col1:
        t_walk_minutes = st.number_input(
            "Minutes",
            min_value=0,
            value=1,
            step=1,
            key="t_walk_min",
            format="%d",
            help="Minutes for each walking break.",
        )
    with walk_dur_col2:
        t_walk_seconds = st.number_input(
            "Seconds",
            min_value=0,
            max_value=59,
            value=0,
            step=1,
            key="t_walk_sec",
            format="%d",
            help="Seconds for each walking break (0-59).",
        )
    t_walk_min_input = float(t_walk_minutes) + (float(t_walk_seconds) / 60.0)

with col2:
    st.subheader("Your Pacing Goals")

    st.markdown("**Overall Target Average Pace (P_target):**")
    pace_col1, pace_col2 = st.columns(2)
    with pace_col1:
        p_target_minutes = st.number_input(
            "Minutes",
            min_value=0,
            value=7,
            step=1,
            key="p_target_min",
            format="%d",
            help="Target minutes per km for the overall average pace.",
        )
    with pace_col2:
        p_target_seconds = st.number_input(
            "Seconds",
            min_value=0,
            max_value=59,
            value=30,
            step=1,
            key="p_target_sec",
            format="%d",
            help="Target seconds per km for the overall average pace (0-59).",
        )

    # Convert to decimal minutes for calculation
    # Ensure inputs are treated as floats for division
    p_target_min_per_km_input = float(p_target_minutes) + (
        float(p_target_seconds) / 60.0
    )

    st.markdown("**Your Brisk Walking Pace (P_walk):**")
    walk_pace_col1, walk_pace_col2 = st.columns(2)
    with walk_pace_col1:
        p_walk_minutes = st.number_input(
            "Minutes",
            min_value=0,
            value=10,
            step=1,
            key="p_walk_min",
            format="%d",
            help="The minutes part of your typical brisk walking pace per km.",
        )
    with walk_pace_col2:
        p_walk_seconds = st.number_input(
            "Seconds",
            min_value=0,
            max_value=59,
            value=0,
            step=1,
            key="p_walk_sec",
            format="%d",
            help="The seconds part of your typical brisk walking pace per km (0-59).",
        )

    # Convert to decimal minutes for calculation
    p_walk_min_per_km_input = float(p_walk_minutes) + (float(p_walk_seconds) / 60.0)


st.markdown("---")

if st.button("Calculate Required Run Pace", type="primary", use_container_width=True):
    # Check that combined durations are positive
    if t_run_min_input <= 0:
        st.error("Running segment duration must be positive.")
    elif t_walk_min_input <= 0:
        st.error("Walking segment duration must be positive.")
    elif p_walk_min_per_km_input <= 0:
        st.error("Walking pace must be a positive value (cannot be 0'00\" or less).")
    elif p_target_min_per_km_input <= 0:
        st.error(
            "Target average pace must be a positive value (cannot be 0'00\" or less)."
        )
    else:
        show_warning = False
        if p_walk_min_per_km_input < p_target_min_per_km_input:
            st.warning(
                "Heads up! Your walking pace (P_walk) is faster than your overall target pace (P_target). "
                "This means you could hit your target by mostly walking, or even just walking!"
            )
            show_warning = True

        required_p_run_min_per_km = calculate_run_pace(
            t_run_min_input,
            p_target_min_per_km_input,
            p_walk_min_per_km_input,
            t_walk_min_input,
        )

        if required_p_run_min_per_km is not None and required_p_run_min_per_km > 0:
            formatted_run_pace = format_pace(required_p_run_min_per_km)
            formatted_target_pace = format_pace(p_target_min_per_km_input)

            st.success(
                f"To achieve an overall average pace of **{formatted_target_pace}/km**..."
            )
            st.metric(
                label="You need to run your running segments at approximately:",
                value=f"{formatted_run_pace}/km",
            )

            total_cycle_duration_min = t_run_min_input + t_walk_min_input
            distance_per_cycle_km = float("inf")
            if p_target_min_per_km_input > 0:
                distance_per_cycle_km = (
                    total_cycle_duration_min / p_target_min_per_km_input
                )

            run_distance_in_cycle_km = float("inf")
            if required_p_run_min_per_km > 0:
                run_distance_in_cycle_km = t_run_min_input / required_p_run_min_per_km

            walk_distance_in_cycle_km = float("inf")
            if p_walk_min_per_km_input > 0:
                walk_distance_in_cycle_km = t_walk_min_input / p_walk_min_per_km_input

            st.markdown(
                f"""
            #### Breakdown per {total_cycle_duration_min:.1f}-minute cycle:
            - **Target distance per cycle:** {distance_per_cycle_km:.3f} km
            - **Distance covered running:** {run_distance_in_cycle_km:.3f} km (in {t_run_min_input:.1f} min)
            - **Distance covered walking:** {walk_distance_in_cycle_km:.3f} km (in {t_walk_min_input:.1f} min)
            """
            )
        elif (
            required_p_run_min_per_km is not None
            and required_p_run_min_per_km <= p_walk_min_per_km_input
            and not show_warning  # Avoid redundant messaging if already warned
        ):
            formatted_calc_run_pace = format_pace(required_p_run_min_per_km)
            formatted_walk_pace = format_pace(p_walk_min_per_km_input)
            formatted_target_pace = format_pace(p_target_min_per_km_input)
            st.info(
                f"The calculated running pace ({formatted_calc_run_pace}/km) is slower than or equal to your walking pace "
                f"({formatted_walk_pace}/km). This usually means your target pace ({formatted_target_pace}/km) "
                "is very achievable with your current walk ratio and pace. You might not need to 'run' faster than your walk!"
            )
        else:
            st.error(
                "Could not calculate a valid running pace. "
                "This often means the **target average pace is too fast** for the chosen run/walk durations and your walking pace. "
                "Consider a slower target pace, shorter walk breaks, longer run segments, or a faster walking pace. Also ensure all inputs are sensible."
            )

st.markdown("---")
st.caption(
    "Remember to always listen to your body and adjust as needed. Happy running!"
)
