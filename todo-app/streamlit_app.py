"""
Interactive To-Do List Application (100% Pure Python with Streamlit)
--------------------------------------------------------------------
Run with:
    streamlit run streamlit_app.py

Features:
- Pure Python web components (no HTML/CSS needed)
- Add, complete, and delete tasks
- Progress bar and live completion metrics
- Automatic sync with 'tasks.txt'
"""

import os
import streamlit as st

DATA_FILE = "tasks.txt"


# ==========================================
# 1. File Persistence Helper Functions
# ==========================================

def load_tasks(filename=DATA_FILE):
    """Loads tasks and completion status from tasks.txt."""
    tasks = []
    if os.path.exists(filename):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    if line.startswith("[x] ") or line.startswith("[X] "):
                        tasks.append({"text": line[4:], "completed": True})
                    elif line.startswith("[ ] "):
                        tasks.append({"text": line[4:], "completed": False})
                    else:
                        tasks.append({"text": line, "completed": False})
        except Exception as e:
            st.error(f"Error loading tasks: {e}")
    return tasks


def save_tasks(tasks, filename=DATA_FILE):
    """Saves tasks and completion status to tasks.txt."""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            for task in tasks:
                prefix = "[x] " if task["completed"] else "[ ] "
                f.write(f"{prefix}{task['text']}\n")
    except Exception as e:
        st.error(f"Error saving tasks: {e}")


# ==========================================
# 2. Page Configuration & State
# ==========================================

st.set_page_config(
    page_title="Python To-Do Web App",
    page_icon="📋",
    layout="centered"
)

if "tasks" not in st.session_state:
    st.session_state.tasks = load_tasks()


# ==========================================
# 3. Streamlit Interactive Web Layout
# ==========================================

st.title("📋 Interactive Python To-Do List")
st.caption("A beginner-friendly responsive web app built purely in Python.")

# Calculate Metrics
total = len(st.session_state.tasks)
completed = sum(1 for t in st.session_state.tasks if t["completed"])
pending = total - completed
progress = (completed / total) if total > 0 else 0.0

# Metric Cards
m_col1, m_col2, m_col3 = st.columns(3)
m_col1.metric("Total Tasks", total)
m_col2.metric("Pending", pending)
m_col3.metric("Completed", completed)

# Visual Progress Bar
st.progress(progress, text=f"Completion Progress: {int(progress * 100)}%")

st.divider()

# Add Task Form
st.subheader("➕ Add a New Task")
with st.form("new_task_form", clear_on_submit=True):
    new_task_input = st.text_input("Task Description", placeholder="e.g. Finish internship Python report")
    submitted = st.form_submit_button("Add Task", use_container_width=True, type="primary")

    if submitted:
        clean_text = new_task_input.strip()
        if clean_text:
            st.session_state.tasks.append({"text": clean_text, "completed": False})
            save_tasks(st.session_state.tasks)
            st.toast(f"Added: {clean_text}", icon="✅")
            st.rerun()
        else:
            st.warning("Task description cannot be empty!")

st.divider()

# Tasks Display
st.subheader("📝 Your Tasks")

if not st.session_state.tasks:
    st.info("Your to-do list is empty. Add a task above to get started!")
else:
    for idx, task in enumerate(st.session_state.tasks):
        col_check, col_title, col_del = st.columns([1, 8, 1])

        with col_check:
            is_done = st.checkbox("", value=task["completed"], key=f"check_{idx}", label_visibility="collapsed")
            if is_done != task["completed"]:
                st.session_state.tasks[idx]["completed"] = is_done
                save_tasks(st.session_state.tasks)
                st.rerun()

        with col_title:
            if task["completed"]:
                st.markdown(f"~~**#{idx + 1}** {task['text']}~~")
            else:
                st.markdown(f"**#{idx + 1}** {task['text']}")

        with col_del:
            if st.button("🗑️", key=f"del_{idx}", help="Delete this task"):
                st.session_state.tasks.pop(idx)
                save_tasks(st.session_state.tasks)
                st.rerun()

    st.divider()
    if st.button("Clear All Completed Tasks", use_container_width=True):
        st.session_state.tasks = [t for t in st.session_state.tasks if not t["completed"]]
        save_tasks(st.session_state.tasks)
        st.rerun()
