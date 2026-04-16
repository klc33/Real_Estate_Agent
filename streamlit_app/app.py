import os
import requests
import streamlit as st
import json
from typing import Dict, Any

# Page config
st.set_page_config(
    page_title="AI Real Estate Agent",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Fixed CSS with proper contrast and readable text
st.markdown("""
<style>
.body{
    color:black;
}
    /* Global Styles */
    .stApp {
        background: #f5f7fa;
    }
    
    /* Main container padding */
    .main > div {
        padding: 2rem 3rem;
    }
    
    /* Header Styles */
    .main-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    .main-header h1 {
        color: #ffffff;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
    }
    
    .main-header p {
        color: #e0e7ff;
        font-size: 1.1rem;
        margin-top: 0.5rem;
    }
    
    /* Price Display Card */
    .price-card {
        background: #ffffff;
        padding: 2rem;
        border-radius: 12px;
        margin: 20px 0;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
        border-left: 5px solid #2a5298;
    }
    
    .price-label {
        color: #6b7280;
        font-size: 0.9rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.5rem;
    }
    
    .price-value {
        color: #1e3c72;
        font-size: 3.5rem;
        font-weight: 700;
        margin: 0;
        line-height: 1.2;
    }
    
    .price-subtitle {
        color: #6b7280;
        font-size: 0.95rem;
        margin-top: 0.5rem;
    }
    
    /* Explanation Card */
    .explanation-card {
        background: #ffffff;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 20px 0;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
        border: 1px solid #e5e7eb;
    }
    
    .explanation-header {
        display: flex;
        align-items: center;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #e5e7eb;
    }
    
    .explanation-header h3 {
        color: #1f2937;
        font-size: 1.3rem;
        font-weight: 600;
        margin: 0;
    }
    
    .explanation-icon {
        font-size: 1.5rem;
        margin-right: 10px;
    }
    
    .explanation-text {
        color: #374151;
        font-size: 1.05rem;
        line-height: 1.7;
        background: #f9fafb;
        padding: 1.2rem;
        border-radius: 8px;
        border-left: 4px solid #2a5298;
    }
    
    /* Features Grid */
    .feature-card {
        background: #ffffff;
        padding: 1rem 1.2rem;
        border-radius: 10px;
        margin-bottom: 0.8rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        border: 1px solid #e5e7eb;
        transition: all 0.2s;
    }
    
    .feature-card:hover {
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        border-color: #2a5298;
    }
    
    .feature-label {
        color: #6b7280;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.3rem;
    }
    
    .feature-value {
        color: #1f2937;
        font-size: 1.2rem;
        font-weight: 600;
    }
    
    /* Warning Banner */
    .warning-banner {
        background: #fef3c7;
        border: 1px solid #fbbf24;
        border-left: 5px solid #f59e0b;
        padding: 1rem 1.2rem;
        border-radius: 8px;
        margin: 20px 0;
    }
    
    .warning-banner h4 {
        color: #92400e;
        margin: 0 0 0.5rem 0;
        font-size: 1.1rem;
        font-weight: 600;
    }
    
    .warning-banner p {
        color: #78350f;
        margin: 0;
        font-size: 0.95rem;
    }
    
    /* Info Banner */
    .info-banner {
        background: #dbeafe;
        border: 1px solid #93c5fd;
        border-left: 5px solid #3b82f6;
        padding: 1rem 1.2rem;
        border-radius: 8px;
        margin: 20px 0;
    }
    
    .info-banner h4 {
        color: #1e3a8a;
        margin: 0 0 0.5rem 0;
        font-size: 1.1rem;
        font-weight: 600;
    }
    
    .info-banner p {
        color: #1e40af;
        margin: 0;
        font-size: 0.95rem;
    }
    
    /* Completeness Bar */
    .completeness-container {
        margin: 20px 0;
    }
    
    .completeness-header {
        display: flex;
        justify-content: space-between;
        margin-bottom: 8px;
        color: #374151;
        font-weight: 500;
    }
    
    .completeness-bar {
        background: #e5e7eb;
        height: 8px;
        border-radius: 4px;
        overflow: hidden;
    }
    
    .completeness-fill {
        height: 100%;
        border-radius: 4px;
        transition: width 0.3s ease;
    }
    
    .completeness-fill.high {
        background: #10b981;
    }
    
    .completeness-fill.medium {
        background: #f59e0b;
    }
    
    .completeness-fill.low {
        background: #ef4444;
    }
    
    .completeness-footer {
        color: #6b7280;
        font-size: 0.9rem;
        margin-top: 8px;
    }
    
    /* Input Area */
    .stTextArea textarea {
        border: 2px solid #d1d5db;
        border-radius: 10px;
        padding: 1rem;
        font-size: 1rem;
        background: #ffffff;
        color: #1f2937;
    }
    
    .stTextArea textarea:focus {
        border-color: #2a5298;
        box-shadow: 0 0 0 3px rgba(42, 82, 152, 0.1);
    }
    
    /* Button */
    .stButton button {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: #ffffff;
        border: none;
        padding: 0.7rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        border-radius: 8px;
        transition: all 0.2s;
        width: 100%;
    }
    
    .stButton button:hover {
        background: linear-gradient(135deg, #2a5298 0%, #1e3c72 100%);
        box-shadow: 0 4px 12px rgba(30, 60, 114, 0.3);
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid #e5e7eb;
    }
    
    [data-testid="stSidebar"] h3 {
        color: #1f2937;
    }
    
    [data-testid="stSidebar"] p {
        color: #4b5563;
    }
    
    /* Sidebar buttons */
    [data-testid="stSidebar"] .stButton button {
        background: #f3f4f6;
        color: #1f2937;
        border: 1px solid #d1d5db;
        box-shadow: none;
    }
    
    [data-testid="stSidebar"] .stButton button:hover {
        background: #e5e7eb;
        border-color: #9ca3af;
        box-shadow: none;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: #f3f4f6;
        padding: 0.5rem;
        border-radius: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        color: #4b5563;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background: #ffffff;
        color: #1e3c72;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    /* Section headers */
    h3 {
        color: #1f2937 !important;
        font-weight: 600 !important;
        margin-bottom: 1rem !important;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        color: #6b7280;
        margin-top: 3rem;
        border-top: 1px solid #e5e7eb;
    }
    
    /* Success and warning messages */
    .stSuccess {
        background: #d1fae5;
        color: #065f46;
    }
    
    .stWarning {
        background: #fef3c7;
        color: #92400e;
    }
    
    .stError {
        background: #fee2e2;
        color: #991b1b;
    }
    
    .stInfo {
        background: #dbeafe;
        color: black;
    }
    
    /* JSON viewer */
    .stJson {
        background: #f9fafb;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 1rem;
    }
    
    /* Spinner */
    .stSpinner {
        color: black;
    }
</style>
""", unsafe_allow_html=True)

# API configuration
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

# Initialize session state
if 'query' not in st.session_state:
    st.session_state.query = ""

# Header
st.markdown("""
<div class="main-header">
    <h1>🏠 AI Real Estate Agent</h1>
    <p>Describe a property in plain English — I'll extract details, predict the price, and explain why</p>
</div>
""", unsafe_allow_html=True)

# Sidebar with examples
with st.sidebar:
    st.markdown("### 📝 Try These Examples")
    st.markdown("---")
    
    examples = {
        "🏡 Basic Home": "3 bedroom ranch with large garage in nice neighborhood",
        "🏰 Detailed Home": "Beautiful 4-bedroom 2-story built in 2010 with 2500 sq ft, high quality finishes, in Northridge",
        "🔧 Fixer Upper": "Small 2 bedroom house from 1950, needs complete renovation, poor condition, 1200 sq ft",
        "💎 Luxury Home": "Stunning luxury 5 bedroom estate, 4000 sq ft, built 2015, top quality, 3 car garage, best neighborhood"
    }
    
    for label, query in examples.items():
        if st.button(label, key=label, use_container_width=True):
            st.session_state.query = query
    
    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.markdown("""
    This AI agent uses:
    - **LLM** to extract features
    - **ML Model** trained on Ames housing data
    - **LLM** to explain predictions
    
    **More details = Better predictions!**
    """)

# Main input area
st.markdown("### 📝 Describe the Property")
query_text = st.text_area(
    "Enter property description:",
    value=st.session_state.query,
    height=120,
    placeholder="e.g., '3 bedroom ranch with large garage in nice neighborhood'",
    label_visibility="collapsed"
)

# Prediction button
col1, col2, col3 = st.columns([1, 1.5, 1])
with col2:
    predict_button = st.button("🔮 Predict Price", type="primary", use_container_width=True)


def display_price(price):
    """Display price in a clean card"""
    st.markdown(f"""
    <div class="price-card">
        <div class="price-label">Estimated Market Value</div>
        <div class="price-value">${price:,.0f}</div>
        <div class="price-subtitle">Based on extracted features and market data</div>
    </div>
    """, unsafe_allow_html=True)


def display_explanation(explanation, confidence):
    """Display explanation with confidence indicator"""
    confidence_emoji = {"high": "🟢", "medium": "🟡", "low": "🔴"}
    emoji = confidence_emoji.get(confidence, "⚪")
    
    st.markdown(f"""
    <div class="explanation-card">
        <div class="explanation-header">
            <span class="explanation-icon">💡</span>
            <h3>AI Explanation {emoji}</h3>
        </div>
        <div class="explanation-text">
            {explanation}
        </div>
    </div>
    """, unsafe_allow_html=True)


def display_completeness_bar(extracted, total, confidence):
    """Display a visual completeness bar"""
    percentage = (extracted / total) * 100
    
    st.markdown(f"""
    <div class="completeness-container">
        <div class="completeness-header">
            <span>Data Completeness</span>
            <span>{extracted}/{total} features</span>
        </div>
        <div class="completeness-bar">
            <div class="completeness-fill {confidence}" style="width: {percentage}%;"></div>
        </div>
        <div class="completeness-footer">
            {confidence.title()} confidence prediction
        </div>
    </div>
    """, unsafe_allow_html=True)


def display_features_grid(features):
    """Display features in a clean grid"""
    clean_features = {k: v for k, v in features.items() 
                     if k != "completeness" and v is not None}
    
    if not clean_features:
        st.warning("No features could be extracted from the description.")
        return
    
    st.markdown("### 📊 Extracted Features")
    
    cols = st.columns(3)
    
    feature_names = {
        "BedroomAbvGr": "Bedrooms",
        "FullBath": "Bathrooms",
        "GrLivArea": "Living Area",
        "LotArea": "Lot Size",
        "YearBuilt": "Year Built",
        "OverallQual": "Quality Rating",
        "GarageCars": "Garage Capacity",
        "Neighborhood": "Neighborhood",
        "HouseStyle": "House Style",
        "LotFrontage": "Lot Frontage",
        "Street": "Street Type"
    }
    
    for i, (key, value) in enumerate(clean_features.items()):
        col_idx = i % 3
        with cols[col_idx]:
            display_name = feature_names.get(key, key)
            
            if isinstance(value, (int, float)):
                if "Area" in key or key == "LotFrontage":
                    formatted_value = f"{value:,.0f} sq ft"
                elif key == "YearBuilt":
                    formatted_value = f"{int(value)}"
                elif key == "OverallQual":
                    stars = "★" * min(10, int(value)) + "☆" * (10 - min(10, int(value)))
                    formatted_value = f"{int(value)}/10 {stars}"
                elif key == "GarageCars":
                    formatted_value = f"{int(value)} car{'s' if value != 1 else ''}"
                else:
                    formatted_value = str(value)
            else:
                formatted_value = str(value)
            
            st.markdown(f"""
            <div class="feature-card">
                <div class="feature-label">{display_name}</div>
                <div class="feature-value">{formatted_value}</div>
            </div>
            """, unsafe_allow_html=True)


def display_missing_warning(missing, completeness):
    """Display warning about missing fields"""
    if missing:
        extracted = completeness.get("extracted_count", 0)
        total = completeness.get("total_features", 11)
        confidence = completeness.get("confidence", "low")
        
        missing_text = ', '.join(missing[:5])
        if len(missing) > 5:
            missing_text += f' and {len(missing) - 5} more'
        
        if confidence == "low":
            st.markdown(f"""
            <div class="warning-banner">
                <h4>⚠️ Limited Information</h4>
                <p>Only {extracted} out of {total} features found. The prediction may be less accurate.<br>
                <strong>Missing:</strong> {missing_text}</p>
            </div>
            """, unsafe_allow_html=True)
        elif confidence == "medium":
            st.markdown(f"""
            <div class="info-banner">
                <h4>ℹ️ Moderate Information</h4>
                <p>Found {extracted} out of {total} features. Adding more details would improve accuracy.</p>
            </div>
            """, unsafe_allow_html=True)


# Make prediction when button is clicked
if predict_button:
    if not query_text.strip():
        st.warning("⚠️ Please enter a property description")
    else:
        with st.spinner("🔍 Analyzing property..."):
            try:
                response = requests.post(
                    f"{API_URL}/predict",
                    json={"text": query_text},
                    timeout=60
                )
                
                if response.status_code != 200:
                    st.error(f"❌ Backend error (Status {response.status_code})")
                    st.text(response.text)
                    st.stop()
                
                data = response.json()
                
                price = data.get("price", 0)
                explanation = data.get("explanation", "")
                features = data.get("features", {})
                missing = data.get("missing_fields", [])
                completeness = data.get("completeness", {})
                
                confidence = completeness.get("confidence", "low")
                extracted = completeness.get("extracted_count", 0)
                total = completeness.get("total_features", 11)
                
                tab1, tab2, tab3 = st.tabs(["💰 Prediction", "📊 Features", "🔍 Details"])
                
                with tab1:
                    if price > 0:
                        display_price(price)
                        display_completeness_bar(extracted, total, confidence)
                        display_explanation(explanation, confidence)
                    else:
                        st.warning("⚠️ Unable to generate price prediction with the information provided.")
                        display_missing_warning(missing, completeness)
                        if explanation:
                            st.info(explanation)
                
                with tab2:
                    display_features_grid(features)
                    display_missing_warning(missing, completeness)
                    
                    if missing:
                        st.markdown("### 💡 Suggestions")
                        st.markdown("""
                        To improve accuracy, try providing:
                        - Square footage (e.g., "2000 sq ft")
                        - Number of bathrooms (e.g., "2.5 baths")
                        - Quality description (e.g., "high quality", "needs renovation")
                        - Garage details (e.g., "2 car garage")
                        - Year built (e.g., "built in 2010")
                        """)
                
                with tab3:
                    st.markdown("### 📋 Raw Response Data")
                    st.json(data)
                    
                    response_json = json.dumps(data, indent=2)
                    st.download_button(
                        label="📥 Download JSON Response",
                        data=response_json,
                        file_name="prediction_response.json",
                        mime="application/json"
                    )
                    
            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to the backend API.")
                st.info(f"Make sure the API is running at {API_URL}")
            except requests.exceptions.Timeout:
                st.error("❌ Request timed out. Please try again.")
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")

# Footer
st.markdown("""
<div class="footer">
    <p>🏠 AI Real Estate Agent | Built with FastAPI, Scikit-learn, and Groq LLM</p>
</div>
""", unsafe_allow_html=True)