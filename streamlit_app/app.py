import os
import requests
import streamlit as st
import pandas as pd
import json
from typing import Dict, Any

# Page config
st.set_page_config(
    page_title="AI Real Estate Agent",
    page_icon="🏠",
    layout="wide"
)

# API configuration
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .price-box {
        background: #f0f8ff;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #2a5298;
        margin: 10px 0;
    }
    .missing-warning {
        background: #fff3cd;
        padding: 10px;
        border-radius: 5px;
        border-left: 5px solid #ffc107;
    }
    .explanation-box {
        background: #f8f9fa;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #dee2e6;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🏠 AI Real Estate Agent</h1>
    <p>Describe a property in plain English — I'll extract details, predict the price, and explain why</p>
</div>
""", unsafe_allow_html=True)

# Sidebar with examples
with st.sidebar:
    st.header("📝 Example Queries")
    st.markdown("Try these examples:")
    
    examples = {
        "Basic Home": "3 bedroom ranch with large garage in nice neighborhood",
        "Detailed Home": "Beautiful 4-bedroom 2-story built in 2010 with 2500 sq ft, high quality finishes, in Northridge",
        "Fixer Upper": "Small 2 bedroom house from 1950, needs work, 1200 sq ft, average quality",
        "Luxury Home": "Luxury 5 bedroom home with 3500 sq ft, top quality finishes, built 2015, 3 car garage"
    }
    
    for label, query in examples.items():
        if st.button(label, key=label):
            st.session_state.query = query
    
    st.divider()
    st.markdown("### ℹ️ About")
    st.markdown("""
    This AI agent uses:
    - **LLM** to extract features from text
    - **ML Model** trained on Ames housing data
    - **LLM** to explain the prediction
    
    More details = Better predictions!
    """)


# Main input area
st.markdown("### Describe the Property")
default_query = st.session_state.get("query", "")
text = st.text_area(
    "Enter property description:",
    value=default_query,
    height=100,
    placeholder="e.g., '3 bedroom ranch with large garage in nice neighborhood'",
    label_visibility="collapsed"
)

# Prediction button
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    predict_button = st.button("🔮 Predict Price", type="primary", use_container_width=True)


def display_features(features: Dict[str, Any]):
    """Display extracted features in a nice format"""
    clean_features = {k: v for k, v in features.items() 
                     if k != "completeness" and v is not None}
    
    if not clean_features:
        st.warning("No features could be extracted from the description.")
        return
    
    # Create columns for better display
    cols = st.columns(3)
    for i, (key, value) in enumerate(clean_features.items()):
        col_idx = i % 3
        with cols[col_idx]:
            if isinstance(value, (int, float)):
                if "Area" in key or "Price" in key:
                    formatted_value = f"{value:,.0f}"
                else:
                    formatted_value = str(value)
            else:
                formatted_value = str(value)
            
            st.metric(
                label=key,
                value=formatted_value,
                delta=None
            )


def display_missing_fields(missing: list, completeness: Dict[str, Any]):
    """Display warning about missing fields"""
    if missing:
        extracted = completeness.get("extracted_count", 0)
        total = completeness.get("total_features", 11)
        confidence = completeness.get("confidence", "low")
        
        if confidence == "low":
            st.warning(f"⚠️ Only {extracted}/{total} features found. "
                      f"Prediction may be less accurate. Missing: {', '.join(missing)}")
        elif confidence == "medium":
            st.info(f"ℹ️ Found {extracted}/{total} features. "
                   f"Adding more details would improve accuracy.")


# Make prediction when button is clicked
if predict_button:
    if not text.strip():
        st.warning("⚠️ Please enter a property description")
    else:
        with st.spinner("Analyzing property..."):
            try:
                # Call the API
                response = requests.post(
                    f"{API_URL}/predict",
                    json={"text": text},
                    timeout=60
                )
                
                if response.status_code != 200:
                    st.error(f"❌ Backend error (Status {response.status_code})")
                    st.text(response.text)
                    st.stop()
                
                data = response.json()
                
                # Display results in tabs
                tab1, tab2, tab3 = st.tabs(["💰 Prediction", "📊 Features", "🔍 Details"])
                
                with tab1:
                    st.markdown("### Predicted Price")
                    
                    price = data.get("price", 0)
                    if price > 0:
                        st.markdown(f"""
                        <div class="price-box">
                            <h2 style="color: #1e3c72; margin: 0;">${price:,.0f}</h2>
                            <p style="color: #666; margin: 5px 0 0 0;">Estimated market value</p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.warning("Unable to generate price prediction with the information provided.")
                    
                    st.markdown("### 💡 Explanation")
                    st.markdown(f"""
                    <div class="explanation-box">
                        {data.get('explanation', 'No explanation available.')}
                    </div>
                    """, unsafe_allow_html=True)
                
                with tab2:
                    st.markdown("### Extracted Features")
                    features = data.get("features", {})
                    display_features(features)
                    
                    missing = data.get("missing_fields", [])
                    completeness = data.get("completeness", {})
                    if missing:
                        display_missing_fields(missing, completeness)
                
                with tab3:
                    st.markdown("### Raw Response Data")
                    st.json(data)
                    
            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to the backend API. Make sure it's running at " + API_URL)
            except requests.exceptions.Timeout:
                st.error("❌ Request timed out. Please try again.")
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")


# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
    <p>AI Real Estate Agent | Built with FastAPI, Scikit-learn, and Groq LLM</p>
</div>
""", unsafe_allow_html=True)