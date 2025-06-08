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
        return False, f"Unsupported language for Piston: {language}"

    payload = {
        "language": language,
        "version": version,
        "files": [{"name": "script", "content": code}]
    }

    try:
        response = requests.post(url, json=payload)
        data = response.json()
        run_result = data.get("run", {})
        success = run_result.get("code", -1) == 0
        error_output = run_result.get("stderr") or run_result.get("output") or "Unknown error"
        return success, error_output.strip()
    except Exception as e:
        return False, str(e)
