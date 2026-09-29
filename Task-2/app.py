"""
Interactive Python Web To-Do Application
----------------------------------------
Run this script with:
    python app.py

It will automatically launch a modern, responsive web application in your default browser.
All task operations (Add, View, Remove, Complete) and file persistence ('tasks.txt')
are handled directly by Python.
"""

import os
import json
import webbrowser
import threading
from flask import Flask, request, jsonify, render_template_string

DATA_FILE = "tasks.txt"

# ==========================================
# 1. File Handling & Task Logic
# ==========================================

def load_tasks_from_file(filename=DATA_FILE):
    """Loads tasks and their completion status from tasks.txt."""
    tasks = []
    if os.path.exists(filename):
        try:
            with open(filename, "r", encoding="utf-8") as file:
                for line in file:
                    line = line.strip()
                    if not line:
                        continue
                    # Check for completed marker "[x] " or "[X] "
                    if line.startswith("[x] ") or line.startswith("[X] "):
                        tasks.append({"text": line[4:], "completed": True})
                    elif line.startswith("[ ] "):
                        tasks.append({"text": line[4:], "completed": False})
                    else:
                        tasks.append({"text": line, "completed": False})
        except Exception as e:
            print(f"[Error loading tasks]: {e}")
    return tasks


def save_tasks_to_file(tasks, filename=DATA_FILE):
    """Saves tasks to tasks.txt with completion markers."""
    try:
        with open(filename, "w", encoding="utf-8") as file:
            for task in tasks:
                prefix = "[x] " if task.get("completed") else "[ ] "
                file.write(f"{prefix}{task['text']}\n")
    except Exception as e:
        print(f"[Error saving tasks]: {e}")


# ==========================================
# 2. Flask Web Application & Layout
# ==========================================

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Python Web To-Do App</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg: #090d16;
            --surface: rgba(22, 27, 46, 0.7);
            --surface-border: rgba(255, 255, 255, 0.08);
            --accent: #6366f1;
            --accent-glow: rgba(99, 102, 241, 0.25);
            --success: #10b981;
            --danger: #ef4444;
            --text: #f1f5f9;
            --text-secondary: #94a3b8;
            --text-muted: #64748b;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Plus Jakarta Sans', sans-serif;
            -webkit-tap-highlight-color: transparent;
        }

        body {
            background-color: var(--bg);
            background-image: 
                radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.15) 0px, transparent 50%),
                radial-gradient(at 100% 100%, rgba(16, 185, 129, 0.12) 0px, transparent 50%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: flex-start;
            padding: 40px 20px;
            color: var(--text);
        }

        .app-container {
            width: 100%;
            max-width: 580px;
            background: var(--surface);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid var(--surface-border);
            border-radius: 28px;
            padding: 32px 28px;
            box-shadow: 0 25px 60px -15px rgba(0, 0, 0, 0.7);
        }

        .header {
            text-align: center;
            margin-bottom: 28px;
        }

        .header h1 {
            font-size: 1.85rem;
            font-weight: 700;
            letter-spacing: -0.03em;
            background: linear-gradient(135deg, #e0e7ff 0%, #a5b4fc 50%, #38bdf8 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .header p {
            color: var(--text-secondary);
            font-size: 0.9rem;
            margin-top: 6px;
        }

        /* Stats & Progress */
        .stats-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: rgba(15, 23, 42, 0.6);
            padding: 14px 18px;
            border-radius: 16px;
            border: 1px solid rgba(255, 255, 255, 0.04);
            margin-bottom: 24px;
        }

        .stat-item {
            display: flex;
            flex-direction: column;
            gap: 2px;
        }

        .stat-item .num {
            font-size: 1.3rem;
            font-weight: 700;
            color: var(--text);
        }

        .stat-item .label {
            font-size: 0.72rem;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        /* Input Form */
        .task-form {
            display: flex;
            gap: 10px;
            margin-bottom: 24px;
        }

        .task-input {
            flex: 1;
            background: rgba(15, 23, 42, 0.75);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            padding: 14px 18px;
            color: var(--text);
            font-size: 0.95rem;
            outline: none;
            transition: all 0.2s ease;
        }

        .task-input:focus {
            border-color: var(--accent);
            box-shadow: 0 0 0 3px var(--accent-glow);
        }

        .btn-add {
            background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
            color: #fff;
            border: none;
            border-radius: 16px;
            padding: 0 24px;
            font-weight: 600;
            font-size: 0.95rem;
            cursor: pointer;
            transition: all 0.2s ease;
            box-shadow: 0 4px 14px rgba(99, 102, 241, 0.4);
            white-space: nowrap;
        }

        .btn-add:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(99, 102, 241, 0.5);
        }

        /* Filter Tabs */
        .filters {
            display: flex;
            gap: 8px;
            margin-bottom: 18px;
        }

        .filter-btn {
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.05);
            color: var(--text-secondary);
            padding: 7px 14px;
            border-radius: 12px;
            font-size: 0.8rem;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.15s ease;
        }

        .filter-btn.active, .filter-btn:hover {
            background: var(--accent);
            color: #fff;
            border-color: var(--accent);
        }

        /* Task List */
        .task-list {
            display: flex;
            flex-direction: column;
            gap: 10px;
            max-height: 420px;
            overflow-y: auto;
            padding-right: 4px;
        }

        .task-list::-webkit-scrollbar {
            width: 6px;
        }
        .task-list::-webkit-scrollbar-thumb {
            background: rgba(255, 255, 255, 0.15);
            border-radius: 10px;
        }

        .task-card {
            display: flex;
            align-items: center;
            justify-content: space-between;
            background: rgba(15, 23, 42, 0.55);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 16px;
            padding: 14px 16px;
            transition: all 0.2s ease;
            animation: fadeIn 0.25s ease-out;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(6px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .task-card:hover {
            border-color: rgba(255, 255, 255, 0.12);
            background: rgba(20, 30, 55, 0.7);
        }

        .task-left {
            display: flex;
            align-items: center;
            gap: 14px;
            flex: 1;
            overflow: hidden;
        }

        .task-num {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.8rem;
            font-weight: 600;
            color: var(--text-muted);
            min-width: 24px;
        }

        .checkbox-custom {
            width: 22px;
            height: 22px;
            border-radius: 7px;
            border: 2px solid rgba(255, 255, 255, 0.25);
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.2s;
            flex-shrink: 0;
        }

        .checkbox-custom.checked {
            background: var(--success);
            border-color: var(--success);
        }

        .checkbox-custom.checked::after {
            content: "✓";
            color: #fff;
            font-size: 13px;
            font-weight: bold;
        }

        .task-title {
            font-size: 0.95rem;
            color: var(--text);
            word-break: break-word;
            transition: color 0.2s;
        }

        .task-title.completed {
            text-decoration: line-through;
            color: var(--text-muted);
        }

        .btn-delete {
            background: transparent;
            border: none;
            color: var(--text-muted);
            cursor: pointer;
            padding: 8px 10px;
            border-radius: 10px;
            font-size: 1.1rem;
            transition: all 0.2s;
            line-height: 1;
        }

        .btn-delete:hover {
            color: var(--danger);
            background: rgba(239, 68, 68, 0.15);
        }

        .empty-placeholder {
            text-align: center;
            padding: 40px 20px;
            color: var(--text-muted);
            font-size: 0.95rem;
        }

        .footer {
            margin-top: 24px;
            text-align: center;
            font-size: 0.8rem;
            color: var(--text-muted);
            border-top: 1px solid rgba(255, 255, 255, 0.05);
            padding-top: 16px;
        }

        @media (max-width: 480px) {
            body {
                padding: 16px 12px;
            }
            .app-container {
                padding: 24px 18px;
            }
            .task-form {
                flex-direction: column;
            }
            .btn-add {
                padding: 12px;
            }
        }
    </style>
</head>
<body>
    <div class="app-container">
        <div class="header">
            <h1>Python To-Do Manager</h1>
            <p>Responsive Web Application • Saved to tasks.txt</p>
        </div>

        <div class="stats-bar">
            <div class="stat-item">
                <span class="num" id="totalCount">0</span>
                <span class="label">Total Tasks</span>
            </div>
            <div class="stat-item">
                <span class="num" id="activeCount" style="color: #38bdf8;">0</span>
                <span class="label">Pending</span>
            </div>
            <div class="stat-item">
                <span class="num" id="completedCount" style="color: #10b981;">0</span>
                <span class="label">Completed</span>
            </div>
        </div>

        <form class="task-form" onsubmit="handleAddTask(event)">
            <input type="text" id="taskInput" class="task-input" placeholder="What needs to be done?" autocomplete="off" required>
            <button type="submit" class="btn-add">+ Add Task</button>
        </form>

        <div class="filters">
            <button class="filter-btn active" onclick="setFilter('all', this)">All Tasks</button>
            <button class="filter-btn" onclick="setFilter('active', this)">Pending</button>
            <button class="filter-btn" onclick="setFilter('completed', this)">Completed</button>
        </div>

        <div class="task-list" id="taskList">
            <div class="empty-placeholder">Loading your tasks...</div>
        </div>

        <div class="footer">
            Python Backend • Syncs with <code>tasks.txt</code> in real-time
        </div>
    </div>

    <script>
        let tasks = [];
        let currentFilter = 'all';

        async function fetchTasks() {
            try {
                const res = await fetch('/api/tasks');
                const data = await res.json();
                tasks = data.tasks || [];
                render();
            } catch (err) {
                console.error("Failed to load tasks", err);
            }
        }

        async function handleAddTask(e) {
            e.preventDefault();
            const input = document.getElementById("taskInput");
            const text = input.value.trim();
            if (!text) return;

            try {
                const res = await fetch('/api/tasks', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ text })
                });
                const data = await res.json();
                if (data.status === "success") {
                    tasks = data.tasks;
                    input.value = "";
                    render();
                }
            } catch (err) {
                console.error("Failed to add task", err);
            }
        }

        async function toggleTask(index) {
            try {
                const res = await fetch(`/api/tasks/${index}/toggle`, { method: 'POST' });
                const data = await res.json();
                if (data.status === "success") {
                    tasks = data.tasks;
                    render();
                }
            } catch (err) {
                console.error("Failed to toggle task", err);
            }
        }

        async function deleteTask(index) {
            try {
                const res = await fetch(`/api/tasks/${index}`, { method: 'DELETE' });
                const data = await res.json();
                if (data.status === "success") {
                    tasks = data.tasks;
                    render();
                }
            } catch (err) {
                console.error("Failed to delete task", err);
            }
        }

        function setFilter(filter, el) {
            currentFilter = filter;
            document.querySelectorAll(".filter-btn").forEach(btn => btn.classList.remove("active"));
            el.classList.add("active");
            render();
        }

        function render() {
            const listEl = document.getElementById("taskList");
            const totalCountEl = document.getElementById("totalCount");
            const activeCountEl = document.getElementById("activeCount");
            const completedCountEl = document.getElementById("completedCount");

            const completed = tasks.filter(t => t.completed).length;
            const active = tasks.length - completed;

            totalCountEl.textContent = tasks.length;
            activeCountEl.textContent = active;
            completedCountEl.textContent = completed;

            const filteredTasks = tasks.map((t, origIdx) => ({ ...t, origIdx })).filter(t => {
                if (currentFilter === 'active') return !t.completed;
                if (currentFilter === 'completed') return t.completed;
                return true;
            });

            if (filteredTasks.length === 0) {
                const msg = tasks.length === 0 
                    ? "✨ No tasks yet! Type a task above and press Add."
                    : "No tasks found matching this filter.";
                listEl.innerHTML = `<div class="empty-placeholder">${msg}</div>`;
                return;
            }

            listEl.innerHTML = filteredTasks.map(t => `
                <div class="task-card">
                    <div class="task-left">
                        <span class="task-num">#${t.origIdx + 1}</span>
                        <div class="checkbox-custom ${t.completed ? 'checked' : ''}" onclick="toggleTask(${t.origIdx})"></div>
                        <span class="task-title ${t.completed ? 'completed' : ''}" onclick="toggleTask(${t.origIdx})">${escapeHtml(t.text)}</span>
                    </div>
                    <button class="btn-delete" title="Delete Task" onclick="deleteTask(${t.origIdx})">✕</button>
                </div>
            `).join('');
        }

        function escapeHtml(str) {
            return str.replace(/[&<>"']/g, m => ({
                '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;'
            }[m]));
        }

        // Initial fetch on page load
        fetchTasks();
    </script>
</body>
</html>
"""

# ==========================================
# 3. HTTP API Routes
# ==========================================

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)


@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    tasks = load_tasks_from_file()
    return jsonify({"tasks": tasks})


@app.route("/api/tasks", methods=["POST"])
def add_task_api():
    data = request.get_json(force=True) or {}
    text = data.get("text", "").strip()
    if not text:
        return jsonify({"status": "error", "message": "Task cannot be empty"}), 400

    tasks = load_tasks_from_file()
    tasks.append({"text": text, "completed": False})
    save_tasks_to_file(tasks)
    return jsonify({"status": "success", "tasks": tasks})


@app.route("/api/tasks/<int:index>/toggle", methods=["POST"])
def toggle_task_api(index):
    tasks = load_tasks_from_file()
    if 0 <= index < len(tasks):
        tasks[index]["completed"] = not tasks[index].get("completed", False)
        save_tasks_to_file(tasks)
        return jsonify({"status": "success", "tasks": tasks})
    return jsonify({"status": "error", "message": "Index out of range"}), 404


@app.route("/api/tasks/<int:index>", methods=["DELETE"])
def delete_task_api(index):
    tasks = load_tasks_from_file()
    if 0 <= index < len(tasks):
        tasks.pop(index)
        save_tasks_to_file(tasks)
        return jsonify({"status": "success", "tasks": tasks})
    return jsonify({"status": "error", "message": "Index out of range"}), 404


def open_browser():
    webbrowser.open_new("http://127.0.0.1:5001")


if __name__ == "__main__":
    print("=" * 55)
    print(" Starting Python Web To-Do App...")
    print(" Opening browser at: http://127.0.0.1:5001")
    print(" Press Ctrl+C in this terminal to stop.")
    print("=" * 55)
    threading.Timer(1.0, open_browser).start()
    app.run(host="127.0.0.1", port=5001, debug=False)
