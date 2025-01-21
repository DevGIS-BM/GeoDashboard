import streamlit as st


st.title("Paramètres")
st.write("Vous pouvez personaliser les paramêtres suivantes.")
theme = st.radio("Selectioner le thème:", ["Light", "Dark"])
st.checkbox("Activez les notifications", value=True)
st.button("Enregistrer")
