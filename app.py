import os
import streamlit as st
from llm_client import explain_sql, optimise_sql

# ── Page config ───────────────────────────────────────────────
st.set_page_config(
    page_title="SQL Explainer",
    page_icon="🗄️",
    layout="wide"
)

# ── Constants ─────────────────────────────────────────────────
MAX_SQL_CHARS = 4000
MAX_REQUESTS_PER_SESSION = 10

# ── Session state init ────────────────────────────────────────
if "request_count" not in st.session_state:
    st.session_state.request_count = 0

# ── Password gate (optional — remove if not needed) ───────────
def check_password() -> bool:
    app_password = st.secrets.get("APP_PASSWORD", "")
    if not app_password:
        return True  # No password set — open access
    if st.session_state.get("authenticated"):
        return True
    st.title("🗄️ SQL Explainer")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if password == app_password:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Incorrect password.")
    st.stop()

check_password()

# ── Rate limit helper ─────────────────────────────────────────
def check_rate_limit() -> bool:
    """Returns True if request is allowed. False if session limit exceeded."""
    if st.session_state.request_count >= MAX_REQUESTS_PER_SESSION:
        st.error(
            f"Session limit reached ({MAX_REQUESTS_PER_SESSION} requests). "
            "Refresh the page to continue."
        )
        return False
    st.session_state.request_count += 1
    return True

# ── UI ────────────────────────────────────────────────────────
st.title("🗄️ SQL Explainer")
st.caption("Paste a SQL query. Get a plain-English explanation and optimisation suggestions.")

sql_input = st.text_area(
    label="Paste your SQL query here",
    height=200,
    placeholder=(
        "SELECT c.name, COUNT(o.id) AS order_count\n"
        "FROM customers c\n"
        "JOIN orders o ON c.id = o.customer_id\n"
        "GROUP BY c.name"
    )
)

# Character count + token estimate
if sql_input:
    st.caption(
        f"{len(sql_input)} characters | "
        f"~{len(sql_input) // 4} tokens estimated | "
        f"{st.session_state.request_count}/{MAX_REQUESTS_PER_SESSION} session requests used"
    )

col1, col2 = st.columns(2)

with col1:
    explain_clicked = st.button(
        "Explain Query", type="primary", use_container_width=True
    )

with col2:
    optimise_clicked = st.button(
        "Suggest Optimisations", use_container_width=True
    )

# ── Explain handler ───────────────────────────────────────────
if explain_clicked:
    if not sql_input.strip():
        st.error("Please paste a SQL query first.")
    elif len(sql_input) > MAX_SQL_CHARS:
        st.error(
            f"Query too long ({len(sql_input)} characters). "
            f"Maximum is {MAX_SQL_CHARS} characters."
        )
    elif check_rate_limit():
        with st.spinner("Explaining your query..."):
            result = explain_sql(sql_input)
        st.subheader("Explanation")
        st.markdown(result)
        st.divider()
        st.caption("Copy the explanation:")
        st.code(result, language=None)

# ── Optimise handler ──────────────────────────────────────────
if optimise_clicked:
    if not sql_input.strip():
        st.error("Please paste a SQL query first.")
    elif len(sql_input) > MAX_SQL_CHARS:
        st.error(
            f"Query too long ({len(sql_input)} characters). "
            f"Maximum is {MAX_SQL_CHARS} characters."
        )
    elif check_rate_limit():
        with st.spinner("Analysing for optimisations..."):
            result = optimise_sql(sql_input)
        st.subheader("Optimisation Suggestions")
        st.markdown(result)
        st.divider()
        st.caption("Copy the suggestions:")
        st.code(result, language=None)