"""
URL Security Checker Module

This module provides heuristic analysis for URLs to detect potential security
threats such as insecure protocols, user information obfuscation, suspicious
structures (e.g., multiple protocol slash pairs), and URL shortening services
often abused by malicious actors.

Designed to be clean, readable, and production-ready for academic presentation
and technical interviews.
"""

from typing import Final, List

# --- Configuration Constants ---
# Define constants for heuristic checks to avoid magic strings and improve maintainability
INSECURE_PROTOCOL: Final[str] = "https://"
OBFUSCATION_CHARACTER: Final[str] = "@"
PROTOCOL_SEPARATOR: Final[str] = "//"
SUSPICIOUS_SHORTENER_DOMAINS: Final[List[str]] = ["bit.ly", "tinyurl"]

# --- Response Messages ---
# Exact response messages matching existing application flow to preserve exact functionality
MSG_NO_URL: Final[str] = "No URL provided"
MSG_NOT_SECURE: Final[str] = "❌ Not secure (missing https)"
MSG_SUSPICIOUS_AT: Final[str] = "❌ Suspicious URL (@ detected)"
MSG_SUSPICIOUS_STRUCTURE: Final[str] = "❌ Suspicious URL structure"
MSG_SHORTENED_URL: Final[str] = "❌ Shortened suspicious URL"
MSG_SAFE_URL: Final[str] = "✅ URL looks safe"


def check_url(url: str) -> str:
    """
    Analyzes a URL using quick heuristics to identify potential phishing indicators.
    
    This function performs a series of sequential heuristic checks on the provided URL
    to determine if it matches patterns commonly associated with phishing or malicious sites.
    
    Heuristic Checks:
    1. Null/Empty validation
    2. Protocol verification (ensuring HTTPS)
    3. Detection of user-info obfuscation (checking for '@' symbol)
    4. Structural anomaly detection (checking for multiple '//' sequences)
    5. Identification of shortened URLs from common platforms (bit.ly, tinyurl)
    
    Args:
        url (str): The target URL string to analyze.
        
    Returns:
        str: A safety verdict message representing the heuristic audit result.
    """
    # 1. Null or Empty Input Validation
    if not url:
        return MSG_NO_URL

    # 2. Check for Secure Protocol (HTTPS)
    # Phishing sites often run on plain HTTP. Missing HTTPS is a strong baseline indicator
    # of an insecure site.
    if INSECURE_PROTOCOL not in url:
        return MSG_NOT_SECURE

    # 3. Check for User-Info Obfuscation (@ symbol)
    # The '@' symbol in a URL ignores everything before it and redirects to the domain after it.
    # Attackers use this to spoof legitimate domains (e.g., http://google.com@malicious.com).
    if OBFUSCATION_CHARACTER in url:
        return MSG_SUSPICIOUS_AT

    # 4. Check for Structural Anomalies (Multiple Double Slashes)
    # Legitimate URLs contain '//' only once after the protocol (e.g., https://).
    # Multiple occurrences suggest redirection tricks or embedded sub-URLs.
    if url.count(PROTOCOL_SEPARATOR) > 1:
        return MSG_SUSPICIOUS_STRUCTURE

    # 5. Check for Suspicious URL Shorteners
    # Phishing campaigns frequently employ URL shorteners to mask the final malicious destination.
    if any(shortener in url for shortener in SUSPICIOUS_SHORTENER_DOMAINS):
        return MSG_SHORTENED_URL

    # 6. Default Safe Verdict
    # If the URL passes all the above basic heuristic checks, it is considered clean.
    return MSG_SAFE_URL