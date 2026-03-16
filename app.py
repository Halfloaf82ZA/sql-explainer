import streamlit as st
from llm_client import explain_sql, optimise_sql

st.set_page_config(
    page_title="SQL Explainer",
    page_icon="🗄️",
    layout="wide"
)

st.title("🗄️ SQL Explainer")
st.caption("Paste a SQL query. Get a plain-English explanation and optimisation suggestions.")

sql_input = st.text_area(
    label="Paste your SQL query here",
    height=200,
    placeholder="SELECT c.name, COUNT(o.id) FROM customers c JOIN orders o ON c.id = o.customer_id GROUP BY c.name"
)

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

if optimise_clicked:
    if not sql_input.strip():
        st.error("Please paste a SQL query first.")
    else:
        with st.spinner("Analysing for optimisations..."):
            result = optimise_sql(sql_input)
        st.subheader("Optimisation Suggestions")
        st.markdown(result)