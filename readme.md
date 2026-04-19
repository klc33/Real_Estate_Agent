# 🏠 AI Real Estate Agent

**LLM Prompt Chaining + Supervised ML + Containerized Deployment**

An AI-powered real estate agent that extracts property features from natural language, predicts sale prices using a trained machine learning model, and explains the valuation in plain English — all served from a Docker container.

---

## 📋 **What This Project Does**

A user describes a property in plain English:  
*"How much would a 3-bedroom ranch with a big garage in a good neighborhood cost?"*

The system:
1. **🧠 Extracts** structured features using an LLM (Groq)
2. **📊 Predicts** the price using a trained Gradient Boosting model
3. **💬 Explains** the result with market context and feature analysis

Everything runs in a single Docker container with FastAPI (backend) and Streamlit (frontend), deployed on Railway.

---

## 🏗️ **Architecture Overview**
┌─────────────────────────────────────────────────────────────────┐
│ USER QUERY │
│ "3-bedroom ranch with large garage" │
└─────────────────────────────────────────────────────────────────┘
↓
┌─────────────────────────────────────────────────────────────────┐
│ STAGE 1: Feature Extraction │
│ (Groq LLM) │
│ Output: {BedroomAbvGr: 3, HouseStyle: "Ranch", GarageCars: 2} │
└─────────────────────────────────────────────────────────────────┘
↓
┌─────────────────────────────────────────────────────────────────┐
│ ML MODEL PREDICTION │
│ (HistGradientBoostingRegressor) │
│ Trained on Ames Housing Dataset │
└─────────────────────────────────────────────────────────────────┘
↓
┌─────────────────────────────────────────────────────────────────┐
│ STAGE 2: Explanation │
│ (Groq LLM) │
│ Output: "This home is valued at $285,000, which is above the │
│ market median due to the 3 bedrooms and ranch style." │
└─────────────────────────────────────────────────────────────────┘
↓
┌─────────────────────────────────────────────────────────────────┐
│ FASTAPI + STREAMLIT │
│ (Single Docker Container) │
│ Deployed on Railway │
└─────────────────────────────────────────────────────────────────┘



---

## 📋 **Prerequisites**

Before running this project, ensure you have:

- **Python 3.11+** ([Download](https://www.python.org/downloads/))
- **Docker Desktop** ([Download](https://www.docker.com/products/docker-desktop/))
- **Git** ([Download](https://git-scm.com/downloads))
- **Groq API Key** ([Get one here](https://console.groq.com/keys))

---

## 🚀 **Setup Steps**

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/real-estate-agent.git
cd real-estate-agent

# Copy the example environment file
cp .env.example .env

# Edit .env and add your Groq API key
# GROQ_API_KEY=gsk_your_actual_key_here



# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Activate (Mac/Linux)
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt


# The model file should already be in ml/best_model.pkl
# If missing, train it:
python ml/train_models.py


# Build and run with Docker
docker build -t realestate-agent .
docker run -p 8000:8000 -p 8501:8501 -e GROQ_API_KEY=your_key_here realestate-agent

API: http://localhost:8000

UI: http://localhost:8501

# Terminal 1: Run FastAPI
uvicorn app.main:app --reload --port 8000

# Terminal 2: Run Streamlit
streamlit run streamlit_app/app.py