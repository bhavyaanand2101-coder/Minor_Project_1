from flask import Flask, render_template, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)
model = joblib.load('pathfinder_model.pkl')

# Knowledge Base for Roadmaps
ROADMAPS = {
    "B.Tech": {
        "Data Structures": ["Solve 2 LeetCode problems daily", "Practice Tree Traversals", "Review Lab Codes"],
        "Calculus": ["Solve 5 Integration sums daily", "Watch Calculus visuals", "Attend Tutorials"]
    },
    "MBA": {
        "Finance": ["Financial Modeling in Excel", "Analyze Balance Sheets", "Case Study on Ratios"],
        "Marketing": ["Mock Digital Campaign", "Consumer Behavior Analysis", "Read Financial News"]
    }
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    
    # Extract values
    att = int(data['attendance'])
    study = int(data['study'])
    g1 = int(data['g1'])
    g2 = int(data['g2'])
    degree = data['degree']
    subject = data['subject']
    
    # ML Prediction
    volatility = g2 - g1
    input_df = pd.DataFrame([[att, study, g2, volatility]], 
                            columns=['Attendance', 'Study_Hours', 'G2', 'Volatility'])
    prediction = model.predict(input_df)[0]
    risk = 100 - prediction
    
    # Get Roadmap
    specific_steps = ROADMAPS.get(degree, {}).get(subject, ["Maintain core focus."])
    
    return jsonify({
        "prediction": round(prediction, 1),
        "risk": round(risk, 1),
        "roadmap": specific_steps,
        "status": "RED" if risk > 60 else "YELLOW" if risk > 35 else "GREEN"
    })

if __name__ == '__main__':
    app.run(debug=True)