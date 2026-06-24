import math

def check_password(password):
    """
    Evaluates the strength of a password using Shannon Entropy, length, and diversity checks.
    Returns a dictionary with score, verdict, entropy, and actionable feedback.
    """
    if not password:
        return {
            "score": 0,
            "verdict": "No password provided",
            "entropy": 0.0,
            "feedback": "Please enter a password to evaluate."
        }
    
    # 1. Common passwords blacklist check
    common_blacklist = [
        "123456", "password", "123456789", "12345", "12345678", "qwerty", "admin", 
        "1234567", "1234567890", "1234", "password123", "admin123", "letmein"
    ]
    if password.lower() in common_blacklist:
        return {
            "score": 10,
            "verdict": "❌ Extremely Weak",
            "entropy": 5.0,
            "feedback": "CRITICAL: This is a highly common password that can be cracked instantly by automated scripts!"
        }
    
    # 2. Compute character pool size (R) and checklist checks
    length = len(password)
    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(not c.isalnum() for c in password)
    
    pool_size = 0
    if has_lower: pool_size += 26
    if has_upper: pool_size += 26
    if has_digit: pool_size += 10
    if has_special: pool_size += 32
    
    if pool_size == 0:
        pool_size = 1
        
    # Calculate Shannon Entropy: E = L * log2(R)
    entropy = length * math.log2(pool_size)
    
    # 3. Formulate custom actionable suggestions
    suggestions = []
    if length < 8:
        suggestions.append("Increase length to at least 8 characters (ideally 12+).")
    if not has_upper:
        suggestions.append("Add uppercase letters.")
    if not has_lower:
        suggestions.append("Add lowercase letters.")
    if not has_digit:
        suggestions.append("Add numbers.")
    if not has_special:
        suggestions.append("Add special symbols (e.g. !, @, #, $).")
        
    # 4. Score out of 100 and map to security verdicts
    if entropy < 35:
        verdict = "❌ Weak"
        score = min(35, max(15, int(entropy * 0.9)))
    elif entropy < 55:
        verdict = "⚠️ Medium"
        score = int(40 + (entropy - 35) * 1.25)
    elif entropy < 80:
        verdict = "✅ Strong"
        score = int(65 + (entropy - 55) * 0.6)
    else:
        verdict = "💎 Excellent"
        score = min(100, int(80 + (entropy - 80) * 0.4))
        
    if not suggestions:
        feedback_str = "Excellent choice! This is a highly complex, secure password."
    else:
        feedback_str = "Suggestions: " + " ".join(suggestions)
        
    return {
        "score": score,
        "verdict": verdict,
        "entropy": round(entropy, 1),
        "feedback": feedback_str
    }
