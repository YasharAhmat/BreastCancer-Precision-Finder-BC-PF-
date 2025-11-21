import streamlit as st
import pandas as pd
from utils.api_client import match_patient_to_trials

st.set_page_config(page_title="Breast Cancer Trial Matcher", page_icon="🧬")
st.title("Breast Cancer Clinical Trial Matcher")

# Patient input form
with st.sidebar.form(key="patient_form"):
    st.header("Patient Information")

    age = st.number_input("Age", min_value=18, max_value=120, value=45, step=1)
    location = st.text_input("Location", "Atlanta, GA")
    gender = st.selectbox("Gender", ["Female", "Male", "Other"], index=0)

    st.subheader("Breast Cancer Subtype")
    subtype = st.selectbox(
        "Subtype",
        ["Triple-Negative", "Luminal A/B", "HER2-Enriched", "All"],
        index=0,
        help="Select the patient's breast cancer subtype"
    )

    submit_btn = st.form_submit_button("Find Matching Trials")

# On submit
if submit_btn:
    patient_data = {
        "age": age,
        "location": location,
        "gender": gender,
        "subtype": subtype
    }

    with st.spinner("Finding matching trials..."):
        result = match_patient_to_trials(patient_data)

    if result.get("error"):
        st.error(f"Error: {result.get('message', 'Unknown error')}")
    elif result.get("count", 0) == 0:
        st.warning("No matching trials found. Try adjusting the criteria.")
    else:
        st.success(f"Found {result['count']} matching trial(s)!")

        # Display matches
        for match in result["matches"]:
            trial = match["trial"]
            confidence = match["confidence"]
            reasons = match["reasons"]
            recommendation = match.get("recommendation", "")

            with st.expander(f"**{trial['title']}** - {confidence} confidence"):
                st.markdown(f"**NCT ID:** {trial['nct_id']}")
                st.markdown(f"**Phase:** {trial.get('phase', 'N/A')}")
                st.markdown(f"**Status:** {trial.get('status', 'N/A')}")
                st.markdown(f"**Recommendation:** {recommendation}")

                st.markdown("---")
                st.markdown("**Match Reasons:**")
                for reason in reasons:
                    st.markdown(f"- {reason}")

                if trial.get('description'):
                    st.markdown("---")
                    st.markdown("**Description:**")
                    st.write(trial['description'])

                if trial.get('locations'):
                    st.markdown("---")
                    st.markdown("**Locations:**")
                    for loc in trial['locations'][:5]:  # Show first 5 locations
                        st.markdown(
                            f"- {loc.get('facility', 'Unknown')}, {loc.get('city', '')}, {loc.get('state', '')}")
                    if len(trial['locations']) > 5:
                        st.markdown(f"*...and {len(trial['locations']) - 5} more locations*")
else:
    st.info("👈 Enter patient information in the sidebar to find matching clinical trials.")
