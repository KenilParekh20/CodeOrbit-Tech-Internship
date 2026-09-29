# 🧮 Interactive Python Web Calculator

A beginner-friendly, responsive calculator application written in Python, complete with clean function modularity, defensive `try/except` error handling, and modern web UI layouts.

---

## 📁 Files in This Project

1. **[`app.py`](calculator/app.py)** ⭐ *(Recommended)*
   - **Self-contained Python Web Application**.
   - Simply run `python app.py` and it **automatically pops up in your web browser**!
   - Modern, responsive glassmorphism UI with keyboard & click support, live display, and calculation history.
   - All arithmetic logic, input validation, and division-by-zero checks run on the Python backend.

2. **[`streamlit_app.py`](calculator/streamlit_app.py)**
   - **100% Pure Python UI** (powered by Streamlit).
   - Features responsive tabs (interactive keypad, standard two-number formula inputs, and history log).
   - Run with: `streamlit run streamlit_app.py`.

3. **[`calculator.py`](calculator/calculator.py)**
   - The original **command-line (CLI)** interactive calculator.
   - Run with: `python calculator.py`.

---

## 🚀 How to Run the Web Calculator

### Option 1: Standalone Web App (One Command)
Open PowerShell or Command Prompt and run:
```powershell
cd "C:\Users\Amit parekh\Desktop\calculator"
python app.py
```
Your browser will automatically open at: **`http://127.0.0.1:5000`**.

### Option 2: Streamlit Pure-Python Web App
```powershell
cd "C:\Users\Amit parekh\Desktop\calculator"
streamlit run streamlit_app.py
```

---

## 💡 Internship Submission Highlights

- **Modular Architecture**: Separate functions for `add()`, `subtract()`, `multiply()`, and `divide()`.
- **Defensive Programming**: `try/except` safeguards against `ZeroDivisionError` and non-numeric entries (`ValueError`).
- **Responsive Web Design**: Adapts cleanly across desktop monitors, tablets, and mobile screens.
