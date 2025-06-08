import requests

# Map language to known stable version names in Piston
STABLE_VERSIONS = {
    "python": "3.10.0",
    "cpp": "10.2.0",
    "c": "10.2.0",
    "javascript": "18.15.0",
    "java": "15.0.2",
    "csharp": "10.0.0",
    "go": "1.20.3",
    "ruby": "3.2.2",
    "rust": "1.70.0"
}

def run_code_with_piston(language, code):
    url = "https://emkc.org/api/v2/piston/execute"
    version = STABLE_VERSIONS.get(language)

    if version is None:
        print(f"Unsupported language for Piston: {language}")
        return False

    payload = {
        "language": language,
        "version": version,
        "files": [{"name": "script", "content": code}]
    }

    try:
        response = requests.post(url, json=payload)
        data = response.json()

        # Debug: Uncomment to inspect actual Piston output
        # print("Piston Response:", data)

        return data.get("run", {}).get("code") == 0

    except Exception as e:
        print(f"Piston error for {language}: {e}")
        return False
