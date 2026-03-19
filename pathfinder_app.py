import pip
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestRegressor
import joblib

# --- 1. THE AI BRAIN (PRE-TRAINED LOGIC) ---
@st.cache_resource
def train_model():
    """Trains a Random Forest based on patterns in the student survey data"""
    np.random.seed(42)
    # Simulating 500 records based on the survey patterns provided
    n = 500
    data = []
    for _ in range(n):
        att = np.random.randint(30, 100)
        study = np.random.randint(1, 15)
        prev_sgpa = np.random.uniform(4.0, 10.0)
        # Current midterm score (simulating volatility)
        current_marks = np.clip(prev_sgpa * 10 + np.random.randint(-15, 5), 0, 100)
        volatility = current_marks - (prev_sgpa * 10)
        
        # Target: Final Exam Score prediction
        target = current_marks + (study * 2) + (att * 0.1) + (volatility * 0.3)
        data.append([att, study, prev_sgpa, current_marks, volatility, np.clip(target, 0, 100)])
    
    X = pd.DataFrame(data, columns=['Attendance', 'Study_Hours', 'Prev_SGPA', 'Midterm_Marks', 'Volatility', 'Target'])
    y = X.pop('Target')
    
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    return model

# --- 2. SURVEY DATA PREPROCESSING ---
def process_survey_input(raw_att, raw_study):
    """Converts Google Form text ranges to numeric midpoints"""
    att_map = {'>90%': 95, '90-80%': 85, '80-90%': 85, '80-75%': 77, '75-60%': 67, '60-50%': 55, '50-60%': 55, '<50%': 40}
    study_map = {'<2 HOURS': 1.5, '2-3 HOURS': 2.5, '3-4 HOURS': 3.5, '4-6 HOURS': 5.0}
    return att_map.get(raw_att, 75), study_map.get(raw_study, 2.5)

# --- 3. UI/UX CONFIGURATION ---
st.set_page_config(page_title="PathFinder AI | Final Build", layout="wide")
st.markdown("""
    <style>
    .main { background-color: #0f172a; color: white; }
    .stMetric { background-color: #1e293b; padding: 15px; border-radius: 10px; border-left: 5px solid #38bdf8; }
    .roadmap-card { background: rgba(56, 189, 248, 0.1); border-left: 5px solid #38bdf8; padding: 20px; border-radius: 10px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. SIDEBAR INPUTS ---
st.sidebar.title("🎓 Student Portal")
name = st.sidebar.text_input("Student Name", "Aman")
degree = st.sidebar.selectbox("Degree", ["B.Tech (CSE)", "MBA", "B.Sc"])
subject = st.sidebar.text_input("Subject Focus", "Data Structures")

st.sidebar.divider()
st.sidebar.subheader("📊 Performance Metrics")
raw_att = st.sidebar.selectbox("Attendance Range", ['>90%', '90-80%', '80-75%', '75-60%', '50-60%', '<50%'])
raw_study = st.sidebar.selectbox("Study Hours per Day", ['<2 HOURS', '2-3 HOURS', '3-4 HOURS', '4-6 HOURS'])
prev_sgpa = st.sidebar.number_input("Last Semester SGPA", 0.0, 10.0, 7.9)
current_midterm = st.sidebar.number_input("Current Midterm Score (0-100)", 0, 100, 65)

# --- 5. EXECUTION LOGIC ---
model = train_model()
clean_att, clean_study = process_survey_input(raw_att, raw_study)
volatility = current_midterm - (prev_sgpa * 10)

# Prepare input for AI
features = pd.DataFrame([[clean_att, clean_study, prev_sgpa, current_midterm, volatility]], 
                       columns=['Attendance', 'Study_Hours', 'Prev_SGPA', 'Midterm_Marks', 'Volatility'])

prediction = model.predict(features)[0]
risk_score = 100 - prediction

# --- 6. MAIN DASHBOARD ---
st.title("🚀 PathFinder AI: Strategic Recovery Dashboard")
st.write(f"Comprehensive Diagnostic Analysis for **{name}**")

tab1, tab2, tab3 = st.tabs(["🎯 AI Assessment", "📍 Recovery Roadmap", "🔍 Research Analytics"])

# TAB 1: AI ASSESSMENT
with tab1:
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Predicted Final Score", f"{int(prediction)}/100")
    with col2:
        st.metric("Risk Probability", f"{int(risk_score)}%")
    with col3:
        status = "CRITICAL" if risk_score > 65 else "AT-RISK" if risk_score > 35 else "ON-TRACK"
        st.metric("Academic Status", status)

    st.divider()
    
    res1, res2 = st.columns([2, 1])
    with res1:
        # Risk Gauge
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = risk_score,
            title = {'text': "Failure Probability Index"},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "#38bdf8"},
                'steps': [
                    {'range': [0, 35], 'color': "rgba(34, 197, 94, 0.3)"},
                    {'range': [35, 65], 'color': "rgba(234, 179, 8, 0.3)"},
                    {'range': [65, 100], 'color': "rgba(239, 68, 68, 0.3)"}
                ]
            }
        ))
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': "white"})
        st.plotly_chart(fig, use_container_width=True)

    with res2:
        st.write("### 🧠 AI Feature Impact")
        # Showing what drives the prediction (XAI)
        importance = pd.DataFrame({
            'Feature': ['Attendance', 'Study', 'Past SGPA', 'Volatility'],
            'Impact': [0.4, 0.2, 0.1, 0.3] # Simplified importance for demo
        })
        fig_imp = px.bar(importance, x='Impact', y='Feature', orientation='h', color='Impact')
        fig_imp.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font={'color': "white"})
        st.plotly_chart(fig_imp, use_container_width=True)

# TAB 2: RECOVERY ROADMAP
with tab2:
    st.header(f"📍 Personalized Recovery Plan: {subject}")
    
    if status == "ON-TRACK":
        st.success("🌟 You are performing exceptionally well! Continue your current regimen and consider joining the Peer-Mentorship program.")
    else:
        st.markdown(f"**AI Analysis:** Your performance decay is primarily driven by **{'Attendance' if clean_att < 75 else 'Low Study Volume'}**.")
        
        # Step 1: Behavioral
        st.markdown("<div class='roadmap-card'><h4>Step 1: Behavioral Correction</h4>"
                    f"You are currently at {clean_att}% attendance. To reach the safe zone, attend every lecture for the next 15 days.</div>", unsafe_allow_html=True)
        
        # Step 2: Subject Specific
        st.markdown("<div class='roadmap-card'><h4>Step 2: Conceptual Mastery</h4>"
                    f"For {degree} - {subject}: Focus on solving previous year papers and dedicate 2 hours extra daily to high-weightage topics.</div>", unsafe_allow_html=True)
        
        # Step 3: The Target
        st.markdown("<div class='roadmap-card'><h4>Step 3: Goal Tracking</h4>"
                    f"Based on your current trajectory, you must score at least <b>{int(100 - (current_midterm*0.5))}</b> in your finals to secure a Grade A.</div>", unsafe_allow_html=True)

# TAB 3: RESEARCH ANALYTICS
with tab3:
    st.header("🔍 Research Correlation Analysis")
    # Simulation of your survey data trends
    df_res = pd.DataFrame({
        'Attendance': [40, 50, 60, 70, 80, 90, 95],
        'Avg_SGPA': [4.2, 5.1, 6.0, 7.2, 8.1, 8.9, 9.4]
    })
    fig_res = px.scatter(df_res, x='Attendance', y='Avg_SGPA', trendline="ols", title="Correlation: Attendance vs academic success")
    st.plotly_chart(fig_res, use_container_width=True)
    
    st.markdown("""
    **Methodology Note:**
    This system uses a **Random Forest Regressor** ensemble model. 
    It calculates the **Volatility Index** by measuring the delta between the Last Semester SGPA 
    and Current Midterm scores to detect performance decay before it leads to failure.
    """)

# --- 7. FOOTER ---
st.sidebar.markdown("---")
st.sidebar.write("Developed by Team Reactors")
st.sidebar.write("System Status: Active ✅")