"""
Self-Contained Python Web Calculator
-----------------------------------
Run this directly with:
    python app.py

It will automatically launch a responsive web calculator in your default web browser!
All arithmetic operations, input validations, and error handling are executed in Python.
"""

import sys
import webbrowser
import threading
from flask import Flask, request, jsonify, render_template_string

# ==========================================
# 1. Arithmetic Functions (Core Logic)
# ==========================================

def add(a: float, b: float) -> float:
    """Returns the sum of two numbers."""
    return a + b


def subtract(a: float, b: float) -> float:
    """Returns the difference between two numbers."""
    return a - b


def multiply(a: float, b: float) -> float:
    """Returns the product of two numbers."""
    return a * b


def divide(a: float, b: float) -> float:
    """
    Returns the quotient of two numbers.
    Raises ZeroDivisionError if divisor is 0.
    """
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero.")
    return a / b


def compute(num1: float, num2: float, op: str) -> float:
    """Routes the numbers to the appropriate operation function."""
    operations = {
        "+": add,
        "-": subtract,
        "*": multiply,
        "/": divide,
    }
    if op not in operations:
        raise ValueError(f"Unsupported operation: {op}")
    return operations[op](num1, num2)


# ==========================================
# 2. Flask Web Server Setup
# ==========================================

app = Flask(__name__)

# Single-page responsive HTML + CSS + JS embedded directly inside Python
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Python Interactive Web Calculator</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-gradient: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%);
            --card-bg: rgba(30, 41, 59, 0.7);
            --card-border: rgba(255, 255, 255, 0.1);
            --accent: #6366f1;
            --accent-hover: #4f46e5;
            --operator-bg: #4f46e5;
            --operator-hover: #4338ca;
            --action-bg: #334155;
            --action-hover: #475569;
            --equal-bg: #10b981;
            --equal-hover: #059669;
            --danger-bg: #ef4444;
            --danger-hover: #dc2626;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Inter', sans-serif;
            -webkit-tap-highlight-color: transparent;
        }

        body {
            background: var(--bg-gradient);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
            color: var(--text-main);
        }

        .container {
            width: 100%;
            max-width: 440px;
            background: var(--card-bg);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid var(--card-border);
            border-radius: 24px;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5), 0 0 40px rgba(99, 102, 241, 0.15);
            overflow: hidden;
            transition: transform 0.2s ease;
        }

        .header {
            padding: 24px 24px 12px;
            text-align: center;
        }

        .header h1 {
            font-size: 1.4rem;
            font-weight: 700;
            letter-spacing: -0.02em;
            background: linear-gradient(to right, #a5b4fc, #38bdf8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .header p {
            font-size: 0.8rem;
            color: var(--text-muted);
            margin-top: 4px;
        }

        /* Display Screen */
        .screen {
            padding: 16px 24px;
            background: rgba(15, 23, 42, 0.8);
            margin: 0 20px 20px;
            border-radius: 16px;
            border: 1px solid rgba(255, 255, 255, 0.05);
            text-align: right;
            box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.3);
        }

        .screen-history {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.9rem;
            color: var(--text-muted);
            min-height: 22px;
            overflow-x: auto;
            white-space: nowrap;
        }

        .screen-current {
            font-family: 'JetBrains Mono', monospace;
            font-size: 2.2rem;
            font-weight: 700;
            color: #38bdf8;
            margin-top: 4px;
            overflow-x: auto;
            white-space: nowrap;
        }

        /* Keypad Grid */
        .keypad {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 12px;
            padding: 0 20px 24px;
        }

        button {
            height: 60px;
            border: none;
            border-radius: 14px;
            font-size: 1.25rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.15s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            user-select: none;
            color: var(--text-main);
            background: rgba(51, 65, 85, 0.5);
            border: 1px solid rgba(255, 255, 255, 0.06);
        }

        button:hover {
            transform: translateY(-2px);
            background: rgba(71, 85, 105, 0.8);
        }

        button:active {
            transform: translateY(1px);
        }

        button.operator {
            background: var(--operator-bg);
            color: #fff;
        }

        button.operator:hover {
            background: var(--operator-hover);
        }

        button.action {
            background: rgba(239, 68, 68, 0.2);
            color: #f87171;
            border-color: rgba(239, 68, 68, 0.3);
        }

        button.action:hover {
            background: rgba(239, 68, 68, 0.35);
        }

        button.equal {
            background: var(--equal-bg);
            color: #fff;
        }

        button.equal:hover {
            background: var(--equal-hover);
        }

        .zero-btn {
            grid-column: span 2;
        }

        /* History drawer */
        .history-section {
            padding: 16px 20px 20px;
            border-top: 1px solid rgba(255, 255, 255, 0.08);
            background: rgba(15, 23, 42, 0.4);
        }

        .history-title {
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.85rem;
            font-weight: 600;
            color: var(--text-muted);
            margin-bottom: 10px;
        }

        .clear-history-btn {
            background: transparent;
            border: none;
            color: #94a3b8;
            font-size: 0.75rem;
            cursor: pointer;
            padding: 4px 8px;
            border-radius: 6px;
            height: auto;
        }

        .clear-history-btn:hover {
            color: #f87171;
            background: rgba(239, 68, 68, 0.1);
            transform: none;
        }

        .history-list {
            max-height: 110px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 6px;
        }

        .history-item {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.8rem;
            padding: 6px 10px;
            background: rgba(255, 255, 255, 0.03);
            border-radius: 6px;
            display: flex;
            justify-content: space-between;
            color: #cbd5e1;
        }

        .history-item span.res {
            color: #38bdf8;
            font-weight: 600;
        }

        .footer {
            text-align: center;
            padding-bottom: 16px;
            font-size: 0.75rem;
            color: var(--text-muted);
        }

        /* Responsive Mobile Adjustments */
        @media (max-width: 480px) {
            body {
                padding: 10px;
            }
            .container {
                border-radius: 18px;
            }
            button {
                height: 54px;
                font-size: 1.15rem;
            }
            .screen-current {
                font-size: 1.85rem;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Python Web Calculator</h1>
            <p>Responsive • Interactive • Python Backend</p>
        </div>

        <div class="screen">
            <div class="screen-history" id="subDisplay">&nbsp;</div>
            <div class="screen-current" id="mainDisplay">0</div>
        </div>

        <div class="keypad">
            <button class="action" onclick="clearAll()">AC</button>
            <button class="action" onclick="backspace()">⌫</button>
            <button class="action" onclick="toggleSign()">±</button>
            <button class="operator" onclick="chooseOp('/')">÷</button>

            <button onclick="appendNum('7')">7</button>
            <button onclick="appendNum('8')">8</button>
            <button onclick="appendNum('9')">9</button>
            <button class="operator" onclick="chooseOp('*')">×</button>

            <button onclick="appendNum('4')">4</button>
            <button onclick="appendNum('5')">5</button>
            <button onclick="appendNum('6')">6</button>
            <button class="operator" onclick="chooseOp('-')">−</button>

            <button onclick="appendNum('1')">1</button>
            <button onclick="appendNum('2')">2</button>
            <button onclick="appendNum('3')">3</button>
            <button class="operator" onclick="chooseOp('+')">+</button>

            <button class="zero-btn" onclick="appendNum('0')">0</button>
            <button onclick="appendDot()">.</button>
            <button class="equal" onclick="calculateResult()">=</button>
        </div>

        <div class="history-section">
            <div class="history-title">
                <span>Recent Calculations</span>
                <button class="clear-history-btn" onclick="clearHistory()">Clear</button>
            </div>
            <div class="history-list" id="historyList">
                <div style="font-size:0.75rem; color:#64748b; text-align:center; padding: 10px;">No calculations yet</div>
            </div>
        </div>

        <div class="footer">
            Powered by Python • Internship Ready Project
        </div>
    </div>

    <script>
        let currentInput = "0";
        let storedNum = null;
        let pendingOp = null;
        let resetScreen = false;
        let historyRecords = [];

        const mainDisplay = document.getElementById("mainDisplay");
        const subDisplay = document.getElementById("subDisplay");
        const historyList = document.getElementById("historyList");

        function updateDisplay() {
            mainDisplay.textContent = currentInput;
            if (storedNum !== null && pendingOp) {
                const opSymbols = { "+": "+", "-": "−", "*": "×", "/": "÷" };
                subDisplay.textContent = `${storedNum} ${opSymbols[pendingOp] || pendingOp}`;
            } else {
                subDisplay.innerHTML = "&nbsp;";
            }
        }

        function appendNum(num) {
            if (currentInput === "0" || resetScreen) {
                currentInput = num;
                resetScreen = false;
            } else {
                currentInput += num;
            }
            updateDisplay();
        }

        function appendDot() {
            if (resetScreen) {
                currentInput = "0.";
                resetScreen = false;
            } else if (!currentInput.includes(".")) {
                currentInput += ".";
            }
            updateDisplay();
        }

        function toggleSign() {
            if (currentInput !== "0" && currentInput !== "Error") {
                currentInput = currentInput.startsWith("-") ? currentInput.slice(1) : "-" + currentInput;
                updateDisplay();
            }
        }

        function backspace() {
            if (resetScreen || currentInput === "Error") {
                currentInput = "0";
                resetScreen = false;
            } else {
                currentInput = currentInput.length > 1 ? currentInput.slice(0, -1) : "0";
            }
            updateDisplay();
        }

        function clearAll() {
            currentInput = "0";
            storedNum = null;
            pendingOp = null;
            resetScreen = false;
            updateDisplay();
        }

        function chooseOp(op) {
            if (storedNum !== null && pendingOp && !resetScreen) {
                calculateResult(() => {
                    storedNum = parseFloat(currentInput);
                    pendingOp = op;
                    resetScreen = true;
                    updateDisplay();
                });
                return;
            }
            storedNum = parseFloat(currentInput);
            pendingOp = op;
            resetScreen = true;
            updateDisplay();
        }

        async function calculateResult(callback) {
            if (storedNum === null || !pendingOp) return;

            const num1 = storedNum;
            const num2 = parseFloat(currentInput);
            const op = pendingOp;

            try {
                // Call Python Backend via HTTP POST
                const response = await fetch('/api/calculate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ num1: num1, num2: num2, op: op })
                });

                const data = await response.json();

                if (data.status === "success") {
                    const resultStr = String(data.result);
                    const opSymbols = { "+": "+", "-": "−", "*": "×", "/": "÷" };
                    subDisplay.textContent = `${num1} ${opSymbols[op]} ${num2} =`;
                    currentInput = resultStr;

                    addHistory(num1, opSymbols[op], num2, resultStr);

                    storedNum = null;
                    pendingOp = null;
                    resetScreen = true;
                    mainDisplay.textContent = currentInput;

                    if (callback) callback();
                } else {
                    currentInput = data.message || "Error";
                    mainDisplay.textContent = currentInput;
                    storedNum = null;
                    pendingOp = null;
                    resetScreen = true;
                }
            } catch (err) {
                currentInput = "Server Error";
                mainDisplay.textContent = currentInput;
                resetScreen = true;
            }
        }

        function addHistory(n1, sym, n2, res) {
            historyRecords.unshift({ n1, sym, n2, res });
            renderHistory();
        }

        function renderHistory() {
            if (historyRecords.length === 0) {
                historyList.innerHTML = `<div style="font-size:0.75rem; color:#64748b; text-align:center; padding: 10px;">No calculations yet</div>`;
                return;
            }
            historyList.innerHTML = historyRecords.slice(0, 10).map(item => `
                <div class="history-item">
                    <span>${item.n1} ${item.sym} ${item.n2}</span>
                    <span class="res">= ${item.res}</span>
                </div>
            `).join('');
        }

        function clearHistory() {
            historyRecords = [];
            renderHistory();
        }

        // Keyboard Support for responsiveness
        document.addEventListener("keydown", (e) => {
            if (e.key >= "0" && e.key <= "9") appendNum(e.key);
            else if (e.key === ".") appendDot();
            else if (e.key === "+") chooseOp("+");
            else if (e.key === "-") chooseOp("-");
            else if (e.key === "*") chooseOp("*");
            else if (e.key === "/") { e.preventDefault(); chooseOp("/"); }
            else if (e.key === "Enter" || e.key === "=") calculateResult();
            else if (e.key === "Backspace") backspace();
            else if (e.key.toLowerCase() === "c" || e.key === "Escape") clearAll();
        });
    </script>
</body>
</html>
"""

# ==========================================
# 3. HTTP API Endpoints
# ==========================================

@app.route("/")
def home():
    """Renders the single-page interactive web calculator."""
    return render_template_string(HTML_TEMPLATE)


@app.route("/api/calculate", methods=["POST"])
def api_calculate():
    """
    Receives JSON with num1, num2, and op.
    Uses defensive try/except blocks to compute result safely in Python.
    """
    try:
        data = request.get_json(force=True)
        if not data:
            return jsonify({"status": "error", "message": "No data received"}), 400

        # Validate numeric inputs
        try:
            num1 = float(data.get("num1"))
            num2 = float(data.get("num2"))
        except (ValueError, TypeError):
            return jsonify({"status": "error", "message": "Invalid numeric input"}), 400

        op = str(data.get("op", "")).strip()

        # Perform arithmetic computation using python functions
        result = compute(num1, num2, op)

        # Format integer results cleanly without trailing decimals (e.g. 5.0 -> 5)
        clean_result = int(result) if result.is_integer() else round(result, 6)

        return jsonify({
            "status": "success",
            "result": clean_result,
            "expression": f"{num1:g} {op} {num2:g} = {clean_result}"
        })

    except ZeroDivisionError:
        return jsonify({"status": "error", "message": "Cannot divide by 0"}), 200
    except ValueError as err:
        return jsonify({"status": "error", "message": str(err)}), 400
    except Exception as err:
        return jsonify({"status": "error", "message": f"Unexpected error: {str(err)}"}), 500


# ==========================================
# 4. Auto-Browser Launcher & Server Start
# ==========================================

def open_browser():
    """Automatically launches the user's browser once server is running."""
    webbrowser.open_new("http://127.0.0.1:5000")


if __name__ == "__main__":
    print("=" * 55)
    print(" Starting Python Web Calculator...")
    print(" Opening browser at: http://127.0.0.1:5000")
    print(" Press Ctrl+C in this terminal to stop the server.")
    print("=" * 55)

    # Launch browser after 1 second
    threading.Timer(1.0, open_browser).start()

    # Run local Flask web server
    app.run(host="127.0.0.1", port=5000, debug=False)
