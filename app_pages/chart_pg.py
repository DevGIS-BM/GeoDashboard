import streamlit as st

# Page Content
st.title("Graphes d'analyses")
st.write("Choisr les données à visualiser")
col1, col2 = st.columns(2)
with col1:
    st.subheader("Contenu 1")
    st.write("bla bla bla bla.")
    st.line_chart({
        'Data A': [10, 20, 30, 40],
        'Data B': [40, 30, 20, 10]
    })
with col2:
    st.subheader("Contenu 2")
    st.write("bla bla bla bla.")
    st.bar_chart({
        'Data A': [10, 20, 30, 40],
        'Data B': [10, 50, 20, 10]
    })
st.write("bla bla bla bla.")
