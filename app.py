from flask import Flask, render_template, request, jsonify
import pickle
import os
from url_checker import check_url

app = Flask(__name__)

# Load model and vectorizer safely
model_path = "model.pkl"
vectorizer_path = "vectorizer.pkl"

if not os.path.exists(model_path) or not os.path.exists(vectorizer_path):
    print("Warning: model.pkl or vectorizer.pkl not found. Please run model_train.py first.")
    model = None
    vectorizer = None
else:
    model = pickle.load(open(model_path, "rb"))
    vectorizer = pickle.load(open(vectorizer_path, "rb"))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    # Handle both AJAX (JSON) and standard form POST
    is_ajax = request.is_json
    
    if is_ajax:
        data = request.get_json()
        url = data.get("url", "")
        email = data.get("email", "")
    else:
        url = request.form.get("url", "")
        email = request.form.get("email", "")

    # Default values in case model isn't trained yet
    email_result = "Model not loaded"
    prediction = 0
    phishing_prob = 0.0

    # 1. Run Machine Learning Classifier on Email Body
    if model and vectorizer:
        email_vector = vectorizer.transform([email])
        prediction = model.predict(email_vector)[0]
        
        # Get threat probability for the interactive gauge
        try:
            probabilities = model.predict_proba(email_vector)[0]
            phishing_prob = float(probabilities[1])
        except Exception:
            phishing_prob = 1.0 if prediction == 1 else 0.0

        if prediction == 1:
            email_result = "⚠️ Phishing Email"
        else:
            email_result = "✅ Safe Email"
    else:
        email_result = "❌ Model files missing. Train model first!"

    # 2. Run Heuristic URL Check
    url_result = check_url(url)
    url_suspicious = ("❌" in url_result)
    is_phishing = (prediction == 1)

    # 3. Calculate Unified Threat Level & Risk Probability
    if is_phishing and url_suspicious:
        threat_level = "CRITICAL THREAT: Phishing Content & Link Detected!"
        risk_probability = 98.0
        risk_color = "#ef4444"
    elif is_phishing:
        threat_level = "HIGH RISK: Phishing Email Content Detected"
        risk_probability = max(75.0, phishing_prob * 100)
        risk_color = "#ef4444"
    elif url_suspicious:
        threat_level = "SUSPICIOUS: Dangerous Hyperlink Detected"
        risk_probability = 85.0
        risk_color = "#d97706"
    else:
        threat_level = "SECURE: Clean Workspace Verified"
        risk_probability = max(5.0, phishing_prob * 100)
        risk_color = "#10b981"

    if is_ajax:
        return jsonify({
            "success": True,
            "url_text": url,
            "email_text": email,
            "prediction": int(prediction),
            "probability": round(risk_probability, 1),
            "email_result": email_result,
            "url_result": url_result,
            "threat_level": threat_level,
            "risk_color": risk_color,
            "word_count": len(email.split())
        })

    # Return standard template render for classic forms
    return render_template("index.html",
                           email_result=email_result,
                           url_result=url_result,
                           email_text=email,
                           url_text=url)

if __name__ == "__main__":
    app.run(debug=True)
