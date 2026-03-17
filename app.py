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

DIALECT_OPTIONS = [
    "T-SQL (SQL Server / Azure SQL)",
    "PostgreSQL",
    "BigQuery",
    "Snowflake SQL",
    "Generic SQL",
]

SAMPLE_QUERY = """SELECT
    c.customer_name,
    COUNT(o.order_id) AS order_count,
    SUM(o.total_amount) AS lifetime_value
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE o.created_date >= DATEADD(year, -1, GETDATE())
GROUP BY c.customer_name
HAVING COUNT(o.order_id) > 5
ORDER BY lifetime_value DESC"""

# ── Session state init ────────────────────────────────────────
if "request_count" not in st.session_state:
    st.session_state.request_count = 0
if "sample_loaded" not in st.session_state:
    st.session_state.sample_loaded = False

# ── Password gate ─────────────────────────────────────────────
def check_password() -> bool:
    try:
        app_password = st.secrets.get("APP_PASSWORD", "")
    except Exception:
        app_password = ""
    if not app_password:
        return True
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
    """Returns True if request is allowed. Increments counter."""
    if st.session_state.request_count >= MAX_REQUESTS_PER_SESSION:
        st.error(
            f"Session limit reached ({MAX_REQUESTS_PER_SESSION} requests). "
            "Refresh the page to continue."
        )
        return False
    st.session_state.request_count += 1
    return True

# ── Sidebar ───────────────────────────────────────────────────
with st.sidebar:
    st.header("Settings")
    dialect = st.selectbox(
        label="SQL dialect",
        options=DIALECT_OPTIONS,
        index=0,
        help="Select the SQL dialect for more accurate explanations and optimisations."
    )
    st.divider()
    st.caption(f"Requests this session: {st.session_state.request_count} / {MAX_REQUESTS_PER_SESSION}")
    st.divider()
    st.markdown("**About**")
    st.caption("SQL Explainer uses Azure OpenAI (gpt-4o) to explain and optimise SQL queries.")

# ── Main UI ───────────────────────────────────────────────────
st.title("🗄️ SQL Explainer")
st.caption("Paste a SQL query. Get a plain-English explanation and optimisation suggestions.")

if st.button("Load sample query", type="secondary"):
    st.session_state.sample_loaded = True
    st.rerun()

default_sql = SAMPLE_QUERY if st.session_state.sample_loaded else ""

sql_input = st.text_area(
    label="Paste your SQL query here",
    value=default_sql,
    height=200,
    placeholder=(
        "SELECT c.name, COUNT(o.id) AS order_count\n"
        "FROM customers c\n"
        "JOIN orders o ON c.id = o.customer_id\n"
        "GROUP BY c.name"
    )
)

if sql_input:
    st.caption(
        f"{len(sql_input)} characters | ~{len(sql_input) // 4} tokens estimated"
    )

if sql_input and len(sql_input) > MAX_SQL_CHARS:
    st.warning(f"Query is {len(sql_input)} characters. Very long queries may produce incomplete explanations.")

col1, col2 = st.columns(2)

with col1:
    explain_clicked = st.button("Explain Query", type="primary", use_container_width=True)

with col2:
    optimise_clicked = st.button("Suggest Optimisations", use_container_width=True)

# ── Explain handler ───────────────────────────────────────────
if explain_clicked:
    if not sql_input.strip():
        st.error("Please paste a SQL query first.")
    elif len(sql_input) > MAX_SQL_CHARS:
        st.error(f"Query too long. Maximum {MAX_SQL_CHARS} characters.")
    elif check_rate_limit():
        with st.spinner(f"Explaining your {dialect} query..."):
            result = explain_sql(sql_input, dialect=dialect)
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
        st.error(f"Query too long. Maximum {MAX_SQL_CHARS} characters.")
    elif check_rate_limit():
        with st.spinner(f"Analysing {dialect} query for optimisations..."):
            result = optimise_sql(sql_input, dialect=dialect)
        st.subheader("Optimisation Suggestions")
        st.markdown(result)
        st.divider()
        st.caption("Copy the suggestions:")
        st.code(result, language=None)

# ── Footer ────────────────────────────────────────────────────
st.divider()
st.caption("Built with Python, Azure OpenAI, and Streamlit · [GitHub](https://github.com/Halfloaf82ZA/sql-explainer)")
