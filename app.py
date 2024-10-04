import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from styles import inject_css, inject_header  # Importer la fonction depuis styles.py


# Beauté des ongles
inject_header()
inject_css()

# Titre de la page
st.markdown("<h2>Bienvenue cher investisseurs</h2>", unsafe_allow_html=True)

# Texte de bienvenue
st.markdown("""
<p>Ce tableau de bord a été conçu pour vous, futurs actionnaires, afin de vous offrir une vue d'ensemble claire et prospective de notre entreprise de travaux publics spécialisée dans l'utilisation de tractopelles. 
Il vous permettra de mieux comprendre les liens entre notre gestion opérationnelle, les dépenses, et notre chiffre d'affaires, tout en mettant en lumière les opportunités de rentabilité à long terme. Explorez les sections pour plus de détails et passez à la page suivante pour voir les prévisions financières.
</p>


""", unsafe_allow_html=True)

# Logique du bouton
if st.button("Commencez"):
    switch_page("operation schedule")