# This Streamlit application simulates business decisions that contribute to value through either 1. Cost 2. Quality 3. Speed or 4. Flexibility. In the system add all the primary and secondary activities. 
import streamlit as st

def display_linkages(decision, metric):
    st.write("### Primary Activities")
    st.write("- Inbound Logistics")
    st.write("- Operations")
    st.write("- Outbound Logistics")
    st.write("- Marketing and Sales")
    st.write("- Service")

    st.write("### Support Activities")
    st.write("- Firm Infrastructure")
    st.write("- Human Resource Management")
    st.write("- Technology Development")
    st.write("- Procurement")

    st.write("### Linkages")
    if decision == "Inbound Logistics":
        st.write("- Horizontal Linkages: Operations, Outbound Logistics")
        st.write("- Vertical Linkages: Procurement, Marketing and Sales, Service")
        st.write("- Task Interdependence: Operations, Procurement")
        st.write("- Cross-functional Linkages: Marketing and Sales, Service")
        st.write("- Shared Resources: Operations, Procurement, Marketing and Sales, Service")
    elif decision == "Operations":
        st.write("- Horizontal Linkages: Inbound Logistics, Outbound Logistics")
        st.write("- Vertical Linkages: Procurement, Marketing and Sales, Service")
        st.write("- Task Interdependence: Inbound Logistics, Outbound Logistics, Procurement")
        st.write("- Cross-functional Linkages: Marketing and Sales, Service")
        st.write("- Shared Resources: Inbound Logistics, Outbound Logistics, Procurement, Marketing and Sales, Service")
    elif decision == "Outbound Logistics":
        st.write("- Horizontal Linkages: Inbound Logistics, Operations")
        st.write("- Vertical Linkages: Procurement, Marketing and Sales, Service")
        st.write("- Task Interdependence: Inbound Logistics, Operations, Procurement")
        st.write("- Cross-functional Linkages: Marketing and Sales, Service")
        st.write("- Shared Resources: Inbound Logistics, Operations, Procurement, Marketing and Sales, Service")
    elif decision == "Marketing and Sales":
        st.write("- Horizontal Linkages: Operations, Outbound Logistics")
        st.write("- Vertical Linkages: Inbound Logistics, Procurement, Service")
        st.write("- Task Interdependence: Operations, Outbound Logistics, Service")
        st.write("- Cross-functional Linkages: Inbound Logistics, Procurement, Service")
        st.write("- Shared Resources: Operations, Outbound Logistics, Inbound Logistics, Procurement, Service")
    elif decision == "Service":
        st.write("- Horizontal Linkages: Operations, Outbound Logistics")
        st.write("- Vertical Linkages: Inbound Logistics, Procurement, Marketing and Sales")
        st.write("- Task Interdependence: Operations, Outbound Logistics, Marketing and Sales")
        st.write("- Cross-functional Linkages: Inbound Logistics, Procurement, Marketing and Sales")
        st.write("- Shared Resources: Operations, Outbound Logistics, Inbound Logistics, Procurement, Marketing and Sales")

def main():
    st.title("Business Decisions Simulator")

    decisions = [
        "Inbound Logistics",
        "Operations",
        "Outbound Logistics",
        "Marketing and Sales",
        "Service"
    ]
    metrics = [
        "Cost",
        "Quality",
        "Speed",
        "Flexibility"
    ]

    decision = st.selectbox("Select a business decision:", decisions)
    metric = st.selectbox("Select the metric of concern:", metrics)

    display_linkages(decision, metric)

if __name__ == "__main__":
    main()
