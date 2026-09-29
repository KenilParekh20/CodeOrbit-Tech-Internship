# 📋 Python To-Do List Application (CLI & Web)

A beginner-friendly to-do list manager created in Python, supporting persistent storage (`tasks.txt`), safe input validation, and modern responsive web layouts.

---

## 📁 Files Included

1. **[`todo.py`](todo.py)** - The **Command-Line (CLI)** App
   - Menu options: Add Task, View Tasks, Remove Task, Save & Exit
   - Clean numbered list display
   - Try/Except input validation
   - Individual functions for every action

2. **[`app.py`](app.py)** ⭐ - **Standalone Responsive Web App**
   - Automatically opens in your browser at `http://127.0.0.1:5001`
   - Real-time checkboxes, add/delete, filters (All, Pending, Completed), live stats
   - Synchronizes with `tasks.txt`

3. **[`streamlit_app.py`](streamlit_app.py)** - **100% Pure Python Web App**
   - Built with Streamlit widgets (progress bar, metrics, form inputs)
   - Run with: `streamlit run streamlit_app.py`

4. **[`tasks.txt`](tasks.txt)**
   - Plain text file where your tasks are saved automatically.

---

## 🚀 How to Run

### Run the Command-Line Version:
```powershell
cd "C:\Users\Amit parekh\Desktop\todo-app"
python todo.py
```

### Run the Interactive Web Version:
```powershell
cd "C:\Users\Amit parekh\Desktop\todo-app"
python app.py
```
*(Automatically launches your web browser!)*

### Run the Streamlit Version:
```powershell
cd "C:\Users\Amit parekh\Desktop\todo-app"
streamlit run streamlit_app.py
```
