"""
Interactive Web Calculator (Pure Python using Streamlit)
-------------------------------------------------------
Run this in terminal with:
    streamlit run streamlit_app.py

Features:
- 100% Python code (no HTML/CSS required)
- Interactive, responsive web layout
- Two modes: Quick Interactive Keypad & Formula / Two-Number Mode
- Full calculation history
- Safe error handling (try/except for ZeroDivisionError and invalid inputs)
"""

import streamlit as st

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


def calculate(a: float, b: float, op: str) -> float:
    """Routes numbers to the appropriate arithmetic function."""
    operations = {
        "+": add,
        "-": subtract,
        "×": multiply,
        "*": multiply,
        "÷": divide,
        "/": divide,
    }
    func = operations.get(op)
    if not func:
        raise ValueError(f"Unknown operation '{op}'")
    return func(a, b)


# ==========================================
# 2. Page Configuration & State
# ==========================================

st.set_page_config(
    page_title="Python Web Calculator",
    page_icon="🧮",
    layout="centered"
)

# Initialize session state for interactive history & display
if "history" not in st.session_state:
    st.session_state.history = []

if "display_value" not in st.session_state:
    st.session_state.display_value = "0"

if "stored_num" not in st.session_state:
    st.session_state.stored_num = None

if "pending_op" not in st.session_state:
    st.session_state.pending_op = None

if "reset_next" not in st.session_state:
    st.session_state.reset_next = False


# ==========================================
# 3. Interactive Web Layout
# ==========================================

st.title("🧮 Python Interactive Calculator")
st.caption("A beginner-friendly responsive web calculator built purely in Python.")

tab_keypad, tab_inputs, tab_history = st.tabs(["📱 Interactive Keypad", "🔢 Standard Input Mode", "📜 History"])

# ------------------------------------------
# TAB 1: Interactive Keypad Layout
# ------------------------------------------
with tab_keypad:
    st.subheader("Keypad Calculator")

    # Display Screen
    display_box = st.empty()
    display_box.markdown(
        f"""
        <div style="
            background: #1e293b;
            color: #38bdf8;
            font-size: 2.2rem;
            font-weight: 700;
            padding: 16px 20px;
            border-radius: 12px;
            text-align: right;
            box-shadow: inset 0 2px 8px rgba(0,0,0,0.4);
            margin-bottom: 15px;
            font-family: monospace;
            overflow-x: auto;
        ">
            {st.session_state.display_value}
        </div>
        """,
        unsafe_allow_html=True
    )

    # Keypad Button Handlers
    def handle_digit(d):
        if st.session_state.reset_next or st.session_state.display_value == "0":
            st.session_state.display_value = str(d)
            st.session_state.reset_next = False
        else:
            st.session_state.display_value += str(d)

    def handle_dot():
        if st.session_state.reset_next:
            st.session_state.display_value = "0."
            st.session_state.reset_next = False
        elif "." not in st.session_state.display_value:
            st.session_state.display_value += "."

    def handle_clear():
        st.session_state.display_value = "0"
        st.session_state.stored_num = None
        st.session_state.pending_op = None
        st.session_state.reset_next = False

    def handle_operator(op):
        try:
            current = float(st.session_state.display_value)
            st.session_state.stored_num = current
            st.session_state.pending_op = op
            st.session_state.reset_next = True
        except ValueError:
            st.session_state.display_value = "Error"

    def handle_equals():
        if st.session_state.stored_num is not None and st.session_state.pending_op:
            try:
                num1 = st.session_state.stored_num
                num2 = float(st.session_state.display_value)
                op = st.session_state.pending_op

                res = calculate(num1, num2, op)
                formatted_res = f"{res:g}"

                # Save record to history
                st.session_state.history.append(f"{num1:g} {op} {num2:g} = {formatted_res}")

                st.session_state.display_value = formatted_res
                st.session_state.stored_num = None
                st.session_state.pending_op = None
                st.session_state.reset_next = True
            except ZeroDivisionError:
                st.session_state.display_value = "Error: Div by 0"
                st.session_state.reset_next = True
            except Exception as e:
                st.session_state.display_value = "Error"
                st.session_state.reset_next = True

    # 4-Column Grid Layout for Calculator Buttons
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("C", use_container_width=True, type="secondary"):
            handle_clear()
            st.rerun()
        if st.button("7", use_container_width=True):
            handle_digit(7)
            st.rerun()
        if st.button("4", use_container_width=True):
            handle_digit(4)
            st.rerun()
        if st.button("1", use_container_width=True):
            handle_digit(1)
            st.rerun()
        if st.button("0", use_container_width=True):
            handle_digit(0)
            st.rerun()

    with col2:
        if st.button("±", use_container_width=True):
            try:
                val = float(st.session_state.display_value)
                st.session_state.display_value = f"{-val:g}"
            except ValueError:
                pass
            st.rerun()
        if st.button("8", use_container_width=True):
            handle_digit(8)
            st.rerun()
        if st.button("5", use_container_width=True):
            handle_digit(5)
            st.rerun()
        if st.button("2", use_container_width=True):
            handle_digit(2)
            st.rerun()
        if st.button(".", use_container_width=True):
            handle_dot()
            st.rerun()

    with col3:
        if st.button("⌫", use_container_width=True):
            val = st.session_state.display_value
            st.session_state.display_value = val[:-1] if len(val) > 1 else "0"
            st.rerun()
        if st.button("9", use_container_width=True):
            handle_digit(9)
            st.rerun()
        if st.button("6", use_container_width=True):
            handle_digit(6)
            st.rerun()
        if st.button("3", use_container_width=True):
            handle_digit(3)
            st.rerun()
        if st.button("=", use_container_width=True, type="primary"):
            handle_equals()
            st.rerun()

    with col4:
        if st.button("÷", use_container_width=True, type="primary"):
            handle_operator("÷")
            st.rerun()
        if st.button("×", use_container_width=True, type="primary"):
            handle_operator("×")
            st.rerun()
        if st.button("-", use_container_width=True, type="primary"):
            handle_operator("-")
            st.rerun()
        if st.button("+", use_container_width=True, type="primary"):
            handle_operator("+")
            st.rerun()


# ------------------------------------------
# TAB 2: Standard Two-Number Input Mode
# ------------------------------------------
with tab_inputs:
    st.subheader("Two-Number Operation Mode")
    st.write("Enter two numbers and select the arithmetic operation:")

    input_col1, input_col2 = st.columns(2)
    with input_col1:
        first_num = st.number_input("First Number", value=0.0, format="%f")
    with input_col2:
        second_num = st.number_input("Second Number", value=0.0, format="%f")

    selected_op = st.selectbox(
        "Select Operation",
        options=["Addition (+)", "Subtraction (-)", "Multiplication (*)", "Division (/)"]
    )

    op_symbol_map = {
        "Addition (+)": "+",
        "Subtraction (-)": "-",
        "Multiplication (*)": "*",
        "Division (/)": "/"
    }
    symbol = op_symbol_map[selected_op]

    if st.button("Calculate Result", type="primary", use_container_width=True):
        try:
            res = calculate(first_num, second_num, symbol)
            result_text = f"{first_num:g} {symbol} {second_num:g} = {res:g}"
            st.success(f"### 🎉 Result: **{result_text}**")
            st.session_state.history.append(result_text)
        except ZeroDivisionError as err:
            st.error(f"⚠️ **Math Error**: {err}")
        except Exception as err:
            st.error(f"❌ **Unexpected Error**: {err}")


# ------------------------------------------
# TAB 3: History & Reset
# ------------------------------------------
with tab_history:
    st.subheader("Calculation History")
    if st.session_state.history:
        for idx, item in enumerate(reversed(st.session_state.history), 1):
            st.write(f"**{idx}.** `{item}`")

        if st.button("🗑️ Clear History", use_container_width=True):
            st.session_state.history = []
            st.rerun()
    else:
        st.info("No calculations performed yet. Try calculating something!")

st.divider()
st.caption("Internship Submission • Python Web Application")
