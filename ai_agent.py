import os
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

# Initialize the Gemini API client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def improve_code_with_ai(code, focus="readability"):
    prompt = f"""You are an AI code reviewer. Your task is to improve the following code with a focus on **{focus}**, while preserving its functionality.

Make the code cleaner, more maintainable, and aligned with best practices for its language. If applicable, also:
- Fix potential performance issues
- Improve naming and documentation (e.g., comments, docstrings)
- Apply consistent formatting and style conventions
- Address any possible security concerns

After rewriting the code, provide only:

1. The final improved code inside a properly formatted markdown code block with the appropriate language tag.
2. Provide a clear and concise summary detailing the exact changes made, with specific references to line numbers or code snippets in proper markdown format.
3. Avoid including the entire before/after code for the full file. Only show minimal relevant code snippets if needed to illustrate a change.

Code to review:
{code}
"""

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )

    if response and response.text:
        full_response = response.text.strip()
        print("AI Response")
        print(full_response)
        

        # Try to extract the FIRST improved code block only
        improved_code = code  # fallback
        parts = full_response.split("```")
        for part in parts:
            if part.strip().startswith("python") or part.strip().startswith("cpp") or part.strip().startswith("js"):
                code_lines = part.strip().splitlines()
                improved_code = "\n".join(code_lines[1:]) if len(code_lines) > 1 else ""
                break

        return improved_code.strip(), full_response.strip()

    return code, "No changes made."



