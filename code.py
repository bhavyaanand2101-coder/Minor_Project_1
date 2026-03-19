import streamlit as st
import pandas as pd
import time
# --- PAGE CONFIG ---
st.set_page_config(page_title="PathFinder AI Demo", page_icon="🚀", layout="wide")
# --- CUSTOM CSS FOR DESIGN ---
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; background-color: #4CAF50; color: white; }
    .risk-card { padding: 20px; border-radius: 15px; text-align: center; color: white; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)
# --- SIDEBAR: INPUTS ---
st.sidebar.header("📊 Student Input Data")
st.sidebar.write("Adjust parameters to see AI prediction change in real-time.")
name = st.sidebar.text_input("Student Name", "Alex Johnson")
attendance = st.sidebar.slider("Attendance (%)", 0, 100, 75)
study_hours = st.sidebar.slider("Weekly Study Hours", 0, 20, 5)
midterm_score = st.sidebar.slider("Mid-term Score (out of 100)", 0, 100, 45)
prev_failures = st.sidebar.selectbox("Previous Course Failures", [0, 1, 2, 3,4])
# --- LOGIC: SIMULATED ML MODEL ---
# This simulates how a Random Forest model would calculate probability
risk_score = (100 - attendance) * 0.4 + (20 - study_hours) * 2 + (100 - midterm_score) * 0.3 + (prev_failures * 10)
risk_score = min(max(risk_score, 0), 100) # Keep between 0-100
# --- MAIN INTERFACE ---
st.title("🚀 PathFinder: Early Warning & Recovery System")
st.markdown(f"### Analyzing Performance for: **{name}**")
st.divider()
col1, col2 = st.columns([1, 2])
with col1:
    st.subheader("⚠️ Risk Assessment")
    # Traffic Light Logic
    if risk_score > 70:
        st.error("### STATUS: CRITICAL (RED)")
        st.markdown("<div class='risk-card' style='background-color: #e74c3c;'>High Probability of Failure</div>", unsafe_allow_html=True)
        status = "Red"
    elif risk_score > 40:
        st.warning("### STATUS: AT-RISK (YELLOW)")
        st.markdown("<div class='risk-card' style='background-color: #f39c12;'>Needs Intervention</div>", unsafe_allow_html=True)
        status = "Yellow"
    else:
        st.success("### STATUS: ON-TRACK (GREEN)")
        st.markdown("<div class='risk-card' style='background-color: #27ae60;'>Safe Zone</div>", unsafe_allow_html=True)
        status = "Green"
    st.metric(label="Calculated Risk Score", value=f"{int(risk_score)}%")
with col2:
    st.subheader("📍 The Comeback Roadmap")
    if status == "Green":
        st.write("✨ Student is performing well. Recommended Action: Maintain current habits and explore advanced elective topics.")
    else:
        st.info("AI-Generated Recovery Steps:")
        # ROADMAP GENERATION LOGIC
        if attendance < 75:
            st.write("👉 **Step 1: Attendance Recovery:** Attendance is your biggest 'Success Killer'. Must attend next 10 classes to stabilize.")
        if study_hours < 10:
            st.write(f"👉 **Step 2: Study Volume:** To move to Green, increase study time from {study_hours}hrs to **12hrs/week**.")
        if midterm_score < 50:
            st.write(f"👉 **Step 3: Academic Gap:** Target a minimum of 65% in the final exam. Schedule a session with a Peer Tutor.")
st.divider()
# --- INNOVATION: THE WHAT-IF SIMULATOR ---
st.subheader("🔄 'What-If' Success Simulator")
st.write("Move the sliders to see how Alex can change his future.")
sim_study = st.select_slider("Simulate Extra Study Hours per week", options=[0, 2, 4, 6, 8, 10])
# Recalculate based on simulation
new_risk = max(risk_score - (sim_study * 5), 5)
if sim_study > 0:
    st.write(f"📈 **Simulation Result:** If {name} studies {sim_study} extra hours, the risk score drops from **{int(risk_score)}%** to **{int(new_risk)}%**!")
    if new_risk < 40:
        st.balloons()
        st.success("This student would move into the GREEN (Safe) zone!")
# --- FOOTER ---
st.sidebar.markdown("---")
st.sidebar.write("Developed by: Team PathFinder")
st.sidebar.write("System: Random Forest Classifier v1.0")