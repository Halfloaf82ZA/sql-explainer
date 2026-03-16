import streamlit as st
from llm_client import explain_sql, optimise_sql

st.set_page_config(
    page_title="SQL Explainer",
    page_icon="🗄️",
    layout="wide"
)

MAX_SQL_CHARS = 4000

st.title("🗄️ SQL Explainer")
st.caption("Paste a SQL query. Get a plain-English explanation and optimisation suggestions.")

sql_input = st.text_area(
    label="Paste your SQL query here",
    height=200,
    placeholder="SELECT c.name, COUNT(o.id) FROM customers c JOIN orders o ON c.id = o.customer_id GROUP BY c.name"
)

if sql_input:
    st.caption(f"{len(sql_input)} characters | ~{len(sql_input) // 4} tokens estimated")

if sql_input and len(sql_input) > MAX_SQL_CHARS:
    st.warning(f"Query is {len(sql_input)} characters. Very long queries may produce incomplete explanations.")

col1, col2 = st.columns(2)

with col1:
    explain_clicked = st.button("Explain Query", type="primary", use_container_width=True)

with col2:
    optimise_clicked = st.button("Suggest Optimisations", use_container_width=True)

if explain_clicked:
    if not sql_input.strip():
        st.error("Please paste a SQL query first.")
    else:
        with st.spinner("Explaining your query..."):
            result = explain_sql(sql_input)
        st.subheader("Explanation")
        st.markdown(result)
        st.divider()
        st.caption("Copy the explanation:")
        st.code(result, language=None)

if optimise_clicked:
    if not sql_input.strip():
        st.error("Please paste a SQL query first.")
    else:
        with st.spinner("Analysing for optimisations..."):
            result = optimise_sql(sql_input)
        st.subheader("Optimisation Suggestions")
        st.markdown(result)
        st.divider()
        st.caption("Copy the suggestions:")
        st.code(result, language=None)