# 🛡️ SENTINEL.AI // Phishing Email & Threat Detector

![Phishing Email Detection Model Architecture](architecture_diagram.png)

SENTINEL.AI is an advanced, high-fidelity **Phishing Email Classifier and URL Threat Analyzer** dashboard. It combines Natural Language Processing (NLP) Machine Learning (Multinomial Naive Bayes trained via TF-IDF Vectorization) with rule-based heuristics to inspect incoming email bodies and embedded hyperlinks, providing real-time threat scores, diagnostic logs, and interactive mock email sandboxing.

---

## 🚀 Key Features

*   **🧠 Machine Learning NLP Engine**: Analyzes email content using TF-IDF vectorization and a trained Multinomial Naive Bayes model to detect urgent cues, brand spoofing, and social engineering patterns.
*   **🔗 Heuristic Link Auditor**: Automatically inspects embedded URLs for suspicious patterns including IP address hosting, credential masking (`@` symbol), double-slash redirect attempts, insecure protocols (HTTP), sub-domain stuffing, and known URL shorteners.
*   **🎯 Interactive Threat Gauge**: Features a dynamic, glowing SVG circular risk meter that visualizes threat probabilities from 0% (Secure) to 100% (Critical Risk) with real-time color transitions.
*   **📬 Live Sandbox Email Simulator**: A simulated email client preloaded with realistic safe and phishing emails, allowing users to test the ML core's capabilities with a single click in an isolated sandbox.
*   **📟 Live Audit Terminal Logger**: A retro-modern shell interface that prints granular execution steps (e.g., tokenization metrics, vector matrix evaluations, threat calculations) with color-coded severity.
*   **💎 Premium Glassmorphism UI**: Beautiful, dark-themed responsive interface utilizing high-end CSS transitions, glowing neon borders, backdrop filters, and Lucide icons.

---

## 📁 Project Directory Structure

```text
phishing-email-detector/
│
├── app.py                  # Flask Web Server Backend (hybrid Form/AJAX)
├── model_train.py          # ML pipeline (generates dataset, trains, saves PKL models)
├── url_checker.py          # Heuristic rule-based URL validation logic
│
├── model.pkl               # Trained Multinomial Naive Bayes model (serialized)
├── vectorizer.pkl          # Fitted TF-IDF Vectorizer (serialized)
│
├── dataset/
│   └── emails.csv          # Balanced dataset of 80+ realistic emails (phishing & safe)
│
├── templates/
│   └── index.html          # HTML5 dashboard layout (tabbed view + shell + sandbox)
│
├── static/
│   ├── style.css           # Custom glassmorphic styling, animations & gauge layout
│   └── script.js            # Tab routing, AJAX handlers, SVG math & inbox simulator
│
├── requirements.txt        # Python dependency list
└── README.md               # Professional documentation & project guide (this file)
```

---

## 🛠️ Installation & Setup

### Prerequisites
*   Python 3.8 or higher installed on your system.
*   `pip` package manager.

### Step 1: Clone or Open the Directory
Navigate to the root directory where the project is located:
```bash
cd phishing-email-detector
```

### Step 2: Install Dependencies
Install the required libraries (Flask, scikit-learn, pandas, numpy, and joblib) from the requirements list:
```bash
pip install -r requirements.txt
```

### Step 3: Train the Machine Learning Model
Run the model training script. This will load the balanced dataset from `dataset/emails.csv`, convert the email texts to numerical vectors, split the data, train the Multinomial Naive Bayes model, and export `model.pkl` and `vectorizer.pkl`:
```bash
python model_train.py
```
*Expected output:*
```text
Loading dataset...
Vectorizing email text using TF-IDF...
Splitting dataset into train/test sets...
Training Multinomial Naive Bayes model...
Model Training Complete!
Accuracy on test set: 100.00%
Saving model.pkl and vectorizer.pkl...
Files saved successfully!
```

### Step 4: Launch the Web Application
Start the Flask development server:
```bash
python app.py
```
*Expected output:*
```text
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

Open your web browser and navigate to **`http://127.0.0.1:5000`** to access the SENTINEL.AI dashboard!

---

## 🧠 Technical Deep-Dive

### 1. The Machine Learning Pipeline
*   **TF-IDF Vectorization**: Raw text cannot be processed directly by Machine Learning algorithms. We use a **Term Frequency-Inverse Document Frequency (TF-IDF)** vectorizer. TF-IDF calculates how important a word is to an email relative to the entire corpus, penalizing common words like "the" and "is" while highlighting critical words like "urgent", "suspended", "verify", "lottery", or brand names.
*   **Multinomial Naive Bayes (MNB)**: MNB is the industry standard classifier for text classification and spam/phishing filtering. It applies Bayes' Theorem of conditional probability, calculating the likelihood of an email being phishing given the presence of specific vectorized terms. It is fast, highly accurate on text, and provides excellent probability outputs (`predict_proba`) which we use to power our interactive threat gauge.

### 2. Heuristic URL Rules (`url_checker.py`)
While ML is highly effective at language patterns, URLs follow strict structures that can be audited instantly using precise rule checks:
1.  **Protocol Check**: Flags links using insecure `http://` or lacking a specified secure protocol.
2.  **Credential Masking (`@`)**: Flags instances of the `@` symbol in URLs, which malicious actors use to mask the real destination domain (e.g., `http://chase.com@attacker-site.ru`).
3.  **Redirection (`//`)**: Flags path sections containing secondary double slashes, indicating forwarding tricks.
4.  **IP Hosting**: Detects raw IP addresses used as domains (e.g., `http://192.168.1.1/login`), which bypass DNS registrars and indicate phishing.
5.  **Shorteners**: Flags URLs masked behind shortening services like `bit.ly` or `tinyurl` that conceal the destination.

---

## 📊 Sample Test Scenarios

### Test Scenario A: Urgent Account Suspension (Phishing)
*   **Email Body**: "URGENT: Your account has been suspended due to suspicious activity. Click here to verify now: http://paypal-identity-check.com"
*   **URL**: "http://paypal-identity-check.com"
*   **Expected Verdict**: **CRITICAL THREAT (Risk Score: 95%+)**
    *   *NLP Engine*: Flags urgent language ("URGENT", "suspended", "verify now").
    *   *URL Engine*: Flags insecure `http://` and potential brand spoofing keywords.

### Test Scenario B: Team Meeting invitation (Safe)
*   **Email Body**: "Hi Team, let's meet tomorrow at 10 AM to discuss the project roadmap and milestones. Thanks!"
*   **URL**: "https://slack.com/meetings"
*   **Expected Verdict**: **SECURE / SAFE (Risk Score: 5% - 15%)**
    *   *NLP Engine*: Classifies text as safe business communication.
    *   *URL Engine*: Resolves URL as secure `https` with a clean reputation.

---

## 🛡️ Sentinel-Shield Security Core v1.0.0
*Developed as a full-stack educational demonstrator to showcase natural language understanding (NLU) combined with client-side security heuristics.*
