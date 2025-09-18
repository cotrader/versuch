import streamlit as st
import yfinance as yf
import pandas as pd

# --- Simple Authentication ---
def check_password():
    """Returns `True` if the user entered the correct password."""
    if "password_correct" not in st.session_state:
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        st.error("😕 Password incorrect")
        return False
    else:
        return True

def password_entered():
    """Checks if password is correct and updates session state."""
    if st.session_state["password"] == st.secrets["auth"]["password"]:
        st.session_state["password_correct"] = True
    else:
        st.session_state["password_correct"] = False

# --- Main App ---
if check_password():
    st.set_page_config(layout="wide")
    st.title("AI-Powered Technical Stock Analysis Dashboard1")
    st.sidebar.header("Configuration")

    # Example content
    ticker = st.sidebar.text_input("Enter ticker", "AAPL")
    data = yf.download(ticker, period="1mo")
    st.line_chart(data["Close"])


            
