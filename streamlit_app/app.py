import os
import requests
import streamlit as st

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

st.title("🏠 AI Real Estate Agent")

text = st.text_area("Describe the property")

if st.button("Predict Price"):

    if not text.strip():
        st.warning("Please enter description")
        st.stop()

    try:
        response = requests.post(
            f"{API_URL}/predict",
            json={"text": text},
            timeout=60
        )

        if response.status_code != 200:
            st.error("Backend error")
            st.text(response.text)
            st.stop()

        data = response.json()

        st.subheader("💰 Price")
        st.success(f"${data['price']:,.0f}")

        st.subheader("⚠ Missing")
        st.write(data.get("missing_fields", []))

        st.subheader("📊 Features")
        st.json(data.get("features", {}))

        st.subheader("🧠 Explanation")
        st.write(data.get("explanation", ""))

    except Exception as e:
        st.error(str(e))