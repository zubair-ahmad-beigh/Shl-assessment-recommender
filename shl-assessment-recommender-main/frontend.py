import os
import streamlit as st
import requests

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000/recommend")

st.set_page_config(
    page_title="SHL Assessment Recommender",
    page_icon="🎯",
    layout="centered"
)

st.title("🎯 SHL Assessment Recommendation System")
st.markdown(
    "Enter a job description or hiring requirement to get recommended SHL assessments."
)

query = st.text_area(
    "Job Description / Query",
    height=150,
    placeholder="e.g. Java backend developer with good communication skills"
)

top_k = st.slider("Number of recommendations", 3, 10, 6)

if st.button("🔍 Get Recommendations"):
    if not query.strip():
        st.warning("Please enter a job description.")
    else:
        with st.spinner("Fetching recommendations..."):
            response = requests.post(
                API_URL,
                json={"query": query, "top_k": top_k},
                timeout=30
            )

        if response.status_code == 200:
            results = response.json()

            if not results:
                st.info("No recommendations found.")
            else:
                st.success("Recommended Assessments")

                for i, r in enumerate(results, 1):
                    with st.container():
                        st.markdown(f"### {i}. {r['assessment_name']}")
                        st.markdown(f"**Type:** `{r['test_type']}`")
                        st.markdown(
                            f"[🔗 View Assessment]({r['url']})",
                            unsafe_allow_html=True
                        )
                        st.divider()
        else:
            st.error("API error. Make sure FastAPI server is running.")
