// ==========================================================================
// PHISHSHIELD AI - Frontend SaaS Controller & Scanner Logic
// ==========================================================================

document.addEventListener("DOMContentLoaded", () => {
    // Hook Form Submission for AJAX
    const form = document.getElementById("analyzer-form");
    if (form) {
        form.addEventListener("submit", handleFormSubmit);
    }
});

// ==========================================================================
// Threat Analyzer Form Submission (AJAX Mode)
// ==========================================================================
async function handleFormSubmit(event) {
    event.preventDefault();
    
    const urlInput = document.getElementById("url-input").value.trim();
    const emailInput = document.getElementById("email-input").value.trim();
    
    if (!urlInput || !emailInput) return;
    
    // Hide idle/result views, show loading
    document.getElementById("idle-state").classList.add("hidden");
    document.getElementById("result-state").classList.add("hidden");
    document.getElementById("loading-state").classList.remove("hidden");
    document.getElementById("dynamic-results").classList.remove("hidden");
    
    // Reset Progress Bar
    const progressFill = document.getElementById("progress-fill");
    progressFill.style.width = "0%";
    
    // Dynamic loading sequence simulation
    updateLoadingStatus("Auditing hyperlink protocol structures...", 20);
    await sleep(350);
    
    updateLoadingStatus("Running Naive Bayes classification vectors...", 55);
    await sleep(350);
    
    updateLoadingStatus("Executing TF-IDF vector mapping...", 85);
    await sleep(250);
    
    updateLoadingStatus("Assembling diagnostics report...", 95);
    await sleep(150);

    try {
        const response = await fetch("/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                url: urlInput,
                email: emailInput
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            progressFill.style.width = "100%";
            await sleep(100);
            
            // Render results
            renderScanResults(data);
        } else {
            throw new Error("API responded with an internal threat auditing error.");
        }
        
    } catch (error) {
        document.getElementById("loading-state").classList.add("hidden");
        document.getElementById("idle-state").classList.remove("hidden");
        alert("Scan aborted. Please ensure your Python Flask backend is running on port 5000.");
    }
}

function updateLoadingStatus(text, pct) {
    const statusText = document.getElementById("loading-status-text");
    const progressFill = document.getElementById("progress-fill");
    if (statusText) statusText.innerText = text;
    if (progressFill) progressFill.style.width = `${pct}%`;
}

// ==========================================================================
// Result Rendering & Progress Bar Animations
// ==========================================================================
function renderScanResults(data) {
    // Switch states
    document.getElementById("loading-state").classList.add("hidden");
    document.getElementById("result-state").classList.remove("hidden");
    
    const probability = data.probability; // unified threat risk percentage
    const isUrlSuspicious = data.url_result.includes("❌");
    const isMlPhishing = data.prediction === 1;
    
    // 1. Animate Unified Threat Progress Bar
    const confidenceBar = document.getElementById("confidence-bar");
    const percentText = document.getElementById("confidence-percent");
    
    confidenceBar.className = "progress-bar";
    
    let currentScore = 0;
    const duration = 400; // ms
    const stepTime = 15;
    const steps = duration / stepTime;
    const increment = probability / steps;
    
    const interval = setInterval(() => {
        currentScore += increment;
        if (currentScore >= probability) {
            currentScore = probability;
            clearInterval(interval);
        }
        
        const rounded = Math.round(currentScore);
        percentText.innerText = `${rounded}%`;
        confidenceBar.style.width = `${rounded}%`;
        
        // Dynamic color formatting depending on risk
        if (rounded < 35) {
            confidenceBar.classList.add("safe");
            percentText.style.color = "var(--accent-green)";
        } else if (rounded < 75) {
            confidenceBar.classList.add("suspicious");
            percentText.style.color = "#d97706";
        } else {
            confidenceBar.classList.add("phish");
            percentText.style.color = "var(--accent-red)";
        }
    }, stepTime);
    
    // 2. Dynamic Verdict Banner
    const banner = document.getElementById("verdict-banner");
    const bannerText = document.getElementById("verdict-text");
    const iconContainer = document.getElementById("verdict-icon-container");
    
    banner.className = "verdict-banner";
    
    if (isMlPhishing && isUrlSuspicious) {
        banner.classList.add("phish");
        bannerText.innerText = "⚠️ Critical: Phishing Email & Link Detected!";
        iconContainer.innerHTML = '<i data-lucide="shield-alert"></i>';
    } else if (isMlPhishing) {
        banner.classList.add("phish");
        bannerText.innerText = "⚠️ High Risk: Phishing Content Detected";
        iconContainer.innerHTML = '<i data-lucide="shield-alert"></i>';
    } else if (isUrlSuspicious) {
        banner.classList.add("suspicious");
        bannerText.innerText = "⚠️ Warning: Suspicious Hyperlink Detected";
        iconContainer.innerHTML = '<i data-lucide="alert-triangle"></i>';
    } else {
        banner.classList.add("safe");
        bannerText.innerText = "✅ Secure: Clean Link & Safe Email";
        iconContainer.innerHTML = '<i data-lucide="shield-check"></i>';
    }
    
    // 3. Hyperlink Safety Status Card
    const urlTextElement = document.getElementById("url-status-text");
    const urlIconElement = document.getElementById("url-status-icon");
    
    urlIconElement.className = "stat-icon";
    urlTextElement.className = "stat-value";
    
    if (isUrlSuspicious) {
        urlIconElement.classList.add("red");
        urlTextElement.classList.add("red");
        urlTextElement.innerText = "Phishing Link";
    } else {
        urlIconElement.classList.add("green");
        urlTextElement.classList.add("green");
        urlTextElement.innerText = "Safe Link";
    }
    
    // 4. Linguistic Threat Score Card (ML classifier result)
    const keywordTextElement = document.getElementById("keyword-score-text");
    const keywordIconElement = document.getElementById("keyword-status-icon");
    
    keywordIconElement.className = "stat-icon";
    keywordTextElement.className = "stat-value";
    
    if (isMlPhishing) {
        keywordIconElement.classList.add("red");
        keywordTextElement.classList.add("red");
        keywordTextElement.innerText = "Phishing Content";
    } else {
        keywordIconElement.classList.add("green");
        keywordTextElement.classList.add("green");
        keywordTextElement.innerText = "Safe Content";
    }
    
    if (window.lucide) {
        lucide.createIcons();
    }
}

// ==========================================================================
// General Utilities
// ==========================================================================
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}
