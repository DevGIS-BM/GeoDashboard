import streamlit as st


st.title("Recherche")
st.write("Utiser ce menuy pour rechercher des jeux de données.")
query = st.text_input("Entrer votre requète:")
if query:
    st.success(f"Chercher '{query}':")
    st.write("- Result 1\n- Result 2\n- Result 3")
