# 🤖 AI Code Review Agent

An intelligent code review and improvement tool that uses **Google Gemini AI** to automatically improve code readability, performance, and quality. It also tests original and improved code for correctness and reports metrics like **Maintainability Index** and **Cyclomatic Complexity**.

---

## 🚀 Features

- ✅ Automatically reviews and improves code (Python, C++, JavaScript, etc.)
- 📊 Analyzes code quality before and after AI improvement
- 🧪 Testing Support: Uses Piston API for basic execution and language-specific frameworks (e.g., Pytest, JUnit, Google Test) for deeper correctness checks
- 📄 Generates a detailed `report.md` with summary of improvements
- 📁 Supports reviewing entire codebases or single files
- 🔁 Modular design for extension (e.g., add performance or security focus)

---

## 📁 Project Structure

```
AI-Code-Review-Agent/
├── main.py                  # CLI entry point
├── ai_agent.py              # Gemini AI integration
├── utils.py                 # File processing & report generation
├── metrics.py               # Code quality analysis (Radon + Lizard)
├── test_runner.py           # Code execution via Piston API
├── requirements.txt         # Dependencies
```

---

## 🛠️ Setup & Installation

1. **Clone the repo:**
   ```bash
   git clone https://github.com/abaiml/AI-Code-Review-Agent.git
   cd AI-Code-Review-Agent
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set your Gemini API key:**
   Create a `.env` file in the root with:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

---

## 📦 Usage

```bash
python main.py --input ./sample --output ./improved_code --focus readability
```

### Arguments:

| Flag       | Description                                           |
|------------|-------------------------------------------------------|
| `--input`  | Folder containing source code to review               |
| `--output` | Folder where improved code and reports will be saved |
| `--focus`  | Review focus area (`readability`, `performance`, etc.) |

📝 **Note:** You can choose any `--input` and `--output` folder paths. The program runs relative to the location of `main.py`.

🧪 **Test Execution Modes:**
- **Basic Check:** Uses [Piston API](https://github.com/engineer-man/piston) to run code and verify it executes without errors
- **Deeper Validation:** Automatically uses appropriate frameworks based on language:
  - Python → Pytest  
  - C++ → Google Test  
  - JavaScript → Jest or Mocha  
  - Java → JUnit  
  - C# → xUnit  
  - Go → GoTest

---

## 📋 Output

After running the tool:

- Improved code is saved in `./improved_code`
- A report is generated at `./improved_code/report.md` summarizing:
  - Summary of AI changes with line references
  - ✅ or ❌ test results (before & after)
  - Maintainability Index & Cyclomatic Complexity metrics

---

## ✅ Example Report Snippet

```markdown
## sample/app.py
**Focus**: readability

```python
def main():
    """
    Sorts a list of numbers in ascending order and prints the sorted list.
    """
    numbers = [10, 32, 5, 1, 6, 16, 4, 6, 100]
    numbers.sort()
    print(numbers)
```

**Summary of Changes:**
- Line 3: Added docstring
- Line 6: Renamed variable `data` to `numbers`

**Test Results**
- Before Improvement: ✅ Passed
- After Improvement: ✅ Passed

**Code Quality Metrics:**
- Maintainability Index: 78.02 ➝ 100.00
- Avg. Cyclomatic Complexity: 1.00 ➝ 1.00
```

---

## 📌 Future Enhancements

- [ ] Add security and performance review focus modes
- [ ] Web UI for uploading files and viewing reports
- [ ] Integrate structured multi-language testing by automatically selecting appropriate frameworks
- [ ] Add more languages support (PHP, TS, Ruby)
- [ ] Generate before/after diffs visually


---

## 📃 License

MIT License
