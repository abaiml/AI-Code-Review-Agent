import os
import lizard  # pip install lizard
from ai_agent import improve_code_with_ai
from metrics import analyze_metrics
from test_runner import run_code_with_piston

def save_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def append_to_report(report_path, file_name, focus, summary):
    with open(report_path, "a", encoding="utf-8") as report:
        report.write(f"## {file_name}\n")
        report.write(f"**Focus**: {focus}\n\n")
        report.write(f"{summary.strip()}\n")
        report.write("\n---\n\n")

def safe_metric_str(value):
    if value is None:
        return "N/A"
    try:
        return f"{value:.2f}"
    except:
        return str(value)

def analyze_metrics_multilang(file_path, code):
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext == ".py":
        return analyze_metrics(code)
    
    elif ext in {".cpp", ".c", ".h", ".hpp", ".java"}:
        # Use Lizard for fully supported languages
        try:
            results = lizard.analyze_file.analyze_source_code(file_path, code)
            funcs = results.function_list
            if not funcs:
                return {"average_cyclomatic_complexity": None, "maintainability_index": None}
            avg_cc = sum(f.cyclomatic_complexity for f in funcs) / len(funcs)
            return {"average_cyclomatic_complexity": round(avg_cc, 2), "maintainability_index": None}
        except Exception as e:
            raise RuntimeError(f"Lizard analysis failed: {e}")
    
    elif ext == ".js":
        # Manual fallback for JavaScript
        return estimate_js_metrics(code)
    
    else:
        return {"average_cyclomatic_complexity": None, "maintainability_index": None}

def estimate_js_metrics(code):
    lines = code.splitlines()
    complexity = 1
    for line in lines:
        line = line.strip()
        if any(kw in line for kw in ['if', 'else if', 'for', 'while', 'case', 'catch', '&&', '||']):
            complexity += 1
    return {
        "average_cyclomatic_complexity": round(complexity, 2),
        "maintainability_index": None  # Optional: implement later
    }


def get_language_from_extension(ext):
    return {
        ".py": "python",
        ".js": "javascript",
        ".ts": "typescript",
        ".cpp": "cpp",
        ".c": "c",
        ".java": "java",
        ".cs": "csharp",
        ".rb": "ruby",
        ".go": "go",
        ".rs": "rust",
        ".sh": "bash",
        ".php": "php",
    }.get(ext, None)


def process_file(input_file, output_file, report_path, focus):
    print(f"Processing file: {input_file}")
    with open(input_file, "r", encoding="utf-8") as f:
        original_code = f.read()

    ext = os.path.splitext(input_file)[1].lower()
    lang = get_language_from_extension(ext)

    # Step 1: Check if original code runs successfully using Piston
    success, error_message = run_code_with_piston(lang, original_code)
    if not success:
        error_report = (
            "### ❌ Test Failed – Original Code Did Not Compile\n\n"
            "**Test Results**\n"
            "- Before Improvement: ❌ Failed\n"
            "- After Improvement: ⏭️ Skipped\n\n"
            "**Reason:**\n"
            "```text\n"
            f"{error_message.strip()[:500]}\n"
            "```\n"
            "⏭️ Skipped AI improvement due to code failure.\n"
        )

        append_to_report(report_path, input_file, focus, error_report)
        print("Original code failed to run. Skipping improvement.")
        return


    # Step 2: Analyze metrics for original code
    try:
        original_metrics = analyze_metrics_multilang(input_file, original_code)
        print("Original Metrics:", original_metrics)  # <-- Print original metrics here
    except Exception as e:
        err = f"Syntax or analysis error in original code: {e}"
        append_to_report(report_path, input_file, focus, err)
        print(err)
        return

    # Step 3: Get improved code from AI
    improved_code, review_summary = improve_code_with_ai(original_code, focus)

    # Step 4: Analyze metrics for improved code
    try:
        improved_metrics = analyze_metrics_multilang(input_file, improved_code)
        print("Improved Metrics:", improved_metrics)  # <-- Print improved metrics here
    except Exception as e:
        err = f"Syntax or analysis error in improved code: {e}"
        append_to_report(report_path, input_file, focus, review_summary + "\n" + err)
        print(err)
        save_file(output_file, improved_code)
        return

    # Step 5: Save improved code
    save_file(output_file, improved_code)

    # Step 6: Run improved code
    after_success = run_code_with_piston(lang, improved_code)

    # Step 7: Test Result
    test_result = f"""
**Test Results**
- Before Improvement: ✅ Passed
- After Improvement: {"✅ Passed" if after_success else "❌ Failed"}
"""

    # Step 8: Metrics Comparison
    metrics_block = "\n**Code Quality Metrics:**\n"
    if original_metrics.get('maintainability_index') is not None:
        metrics_block += f"- Maintainability Index: {safe_metric_str(original_metrics['maintainability_index'])} ➝ {safe_metric_str(improved_metrics['maintainability_index'])}\n"
    if original_metrics.get('average_cyclomatic_complexity') is not None:
        metrics_block += f"- Avg. Cyclomatic Complexity: {safe_metric_str(original_metrics['average_cyclomatic_complexity'])} ➝ {safe_metric_str(improved_metrics['average_cyclomatic_complexity'])}\n"

    # Step 9: Final Report
    full_report = review_summary + "\n" + test_result + metrics_block
    append_to_report(report_path, input_file, focus, full_report)
