import streamlit as st

# Define the primary activities and support activities
primary_activities = [
    "Inbound Logistics",
    "Operations",
    "Outbound Logistics",
    "Marketing and Sales",
    "Service"
]

support_activities = [
    "Procurement",
    "Technology Development",
    "Human Resource Management",
    "Firm Infrastructure"
]

# Create a dictionary to store the decisions and their impacts
decisions = {
    "Inbound Logistics": 0,
    "Operations": 0,
    "Outbound Logistics": 0,
    "Marketing and Sales": 0,
    "Service": 0,
    "Procurement": 0,
    "Technology Development": 0,
    "Human Resource Management": 0,
    "Firm Infrastructure": 0
}

# Render the sidebar for decision inputs
def render_sidebar():
    st.sidebar.subheader("Value Chain Decisions")
    for activity in primary_activities:
        decision = st.sidebar.slider(
            f"{activity} Decision",
            min_value=-10,
            max_value=10,
            value=0,
            step=1
        )
        decisions[activity] = decision

    for activity in support_activities:
        decision = st.sidebar.slider(
            f"{activity} Decision",
            min_value=-10,
            max_value=10,
            value=0,
            step=1
        )
        decisions[activity] = decision

# Calculate the overall impact based on the decisions
def calculate_impact():
    primary_impact = sum(decisions[activity] for activity in primary_activities)
    support_impact = sum(decisions[activity] for activity in support_activities)
    total_impact = primary_impact + support_impact
    return total_impact

# Render the main content
def render_content():
    st.title("Michael Porter's Value Chain Model Simulator")
    st.write("Use the sliders in the sidebar to make decisions and see their impact on the value chain.")

    render_sidebar()

    total_impact = calculate_impact()

    st.subheader("Decisions and Impact")
    st.write("Primary Activities")
    for activity in primary_activities:
        st.write(f"- {activity}: {decisions[activity]}")
    st.write("Support Activities")
    for activity in support_activities:
        st.write(f"- {activity}: {decisions[activity]}")
    st.write(f"Total Impact: {total_impact}")

# Run the app
if __name__ == "__main__":
    render_content()
