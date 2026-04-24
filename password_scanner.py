import re
import math
import hashlib
import requests

# 1. ENTROPY CALCULATION
def calculate_entropy(password):
    pool = 0
    if re.search(r"[a-z]", password): pool += 26
    if re.search(r"[A-Z]", password): pool += 26
    if re.search(r"[0-9]", password): pool += 10
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password): pool += 32

    if pool == 0:
        return 0

    entropy = len(password) * math.log2(pool)
    return round(entropy, 2)


# 2. PATTERN DETECTION
def detect_patterns(password):
    issues = []

    common_patterns = ["123", "abc", "qwerty", "password"]
    for pattern in common_patterns:
        if pattern in password.lower():
            issues.append(f"Contains common pattern: {pattern}")

    if re.search(r"(.)\1{2,}", password):
        issues.append("Repeated characters detected")

    if re.search(r"(012|123|234|345|456|567|678|789)", password):
        issues.append("Sequential numbers detected")

    return issues


# 3. BREACH CHECK (HIBP API)
def check_breach(password):
    sha1 = hashlib.sha1(password.encode()).hexdigest().upper()
    prefix = sha1[:5]
    suffix = sha1[5:]

    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    response = requests.get(url)

    if response.status_code != 200:
        return "Error checking breach"

    hashes = response.text.splitlines()

    for h in hashes:
        hash_suffix, count = h.split(":")
        if hash_suffix == suffix:
            return int(count)  # number of times found

    return 0


# 4. ATTACK TIME ESTIMATION
def estimate_crack_time(entropy):
    guesses = 2 ** entropy

    # guesses per second (approx)
    online = 1e3
    offline = 1e9

    online_time = guesses / online
    offline_time = guesses / offline

    return format_time(online_time), format_time(offline_time)


def format_time(seconds):
    if seconds < 60:
        return f"{int(seconds)} seconds"
    elif seconds < 3600:
        return f"{int(seconds/60)} minutes"
    elif seconds < 86400:
        return f"{int(seconds/3600)} hours"
    elif seconds < 31536000:
        return f"{int(seconds/86400)} days"
    else:
        return f"{int(seconds/31536000)} years"


# 5. SUGGESTIONS ENGINE
def generate_suggestions(password, issues):
    suggestions = []

    if len(password) < 12:
        suggestions.append("Use at least 12 characters")

    if not re.search(r"[A-Z]", password):
        suggestions.append("Add uppercase letters")

    if not re.search(r"[a-z]", password):
        suggestions.append("Add lowercase letters")

    if not re.search(r"[0-9]", password):
        suggestions.append("Include numbers")

    if not re.search(r"[!@#$%^&*]", password):
        suggestions.append("Add special characters")

    if any("pattern" in i.lower() for i in issues):
        suggestions.append("Avoid predictable patterns like 123 or abc")

    return suggestions


# 6. PASSWORD MUTATION GENERATOR
def generate_strong_password(password):
    replacements = {
        "a": "@", "s": "$", "i": "!", "o": "0", "e": "3"
    }

    new_pass = ""
    for char in password:
        if char.lower() in replacements:
            new_pass += replacements[char.lower()]
        else:
            new_pass += char

    new_pass += "#92X$"  # add randomness
    return new_pass


# 7. MAIN ANALYZER
def analyze_password(password):
    print("\n🔐 PASSWORD SECURITY ANALYSIS\n")

    entropy = calculate_entropy(password)
    print(f"Entropy Score: {entropy}")

    if entropy < 40:
        strength = "Weak"
    elif entropy < 70:
        strength = "Moderate"
    else:
        strength = "Strong"

    print(f"Strength Level: {strength}")

    # Pattern Issues
    issues = detect_patterns(password)
    if issues:
        print("\n⚠️ Issues Found:")
        for i in issues:
            print(f"- {i}")

    # Breach Check
    print("\n🔎 Checking breach database...")
    breach_count = check_breach(password)

    if breach_count == "Error checking breach":
        print("Could not check breach database.")
    elif breach_count > 0:
        print(f"❌ Password found in breaches {breach_count} times!")
    else:
        print("✅ Password NOT found in known breaches")

    # Attack Time
    online, offline = estimate_crack_time(entropy)
    print("\n⏳ Estimated Crack Time:")
    print(f"- Online Attack: {online}")
    print(f"- Offline Attack (GPU): {offline}")

    # Suggestions
    suggestions = generate_suggestions(password, issues)
    print("\n💡 Suggestions:")
    for s in suggestions:
        print(f"- {s}")

    # Improved Password
    print("\n🔁 Suggested Strong Password:")
    print(generate_strong_password(password))


# RUN PROGRAM
if __name__ == "__main__":
    user_password = input("Enter password to analyze: ")
    analyze_password(user_password)