# main.py
import os
import argparse
from utils import process_file



def process_codebase(input_dir, output_dir, focus="readability"):
    os.makedirs(output_dir, exist_ok=True)
    report_path = os.path.join(output_dir, "report.md")

    # Initialize report with a header once per run
    if not os.path.exists(report_path):
        with open(report_path, "w", encoding="utf-8") as report:
            report.write("# Code Review Report\n\n")

    for root, _, files in os.walk(input_dir):
        for file in files:
            supported_extensions = [".py", ".js", ".cpp", ".c", ".h", ".java", ".ts", ".html"]
            if any(file.endswith(ext) for ext in supported_extensions):

                input_path = os.path.join(root, file)
                relative_path = os.path.relpath(input_path, input_dir)
                output_path = os.path.join(output_dir, relative_path)
                process_file(input_path, output_path, report_path, focus)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI Code Review Agent")
    parser.add_argument("--input", required=True, help="Path to input codebase folder")
    parser.add_argument("--output", required=True, help="Path to output folder for improved code")
    parser.add_argument("--focus", default="readability", help="Focus area: readability, performance, security, etc.")
    args = parser.parse_args()

    process_codebase(args.input, args.output, args.focus)
