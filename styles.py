import streamlit as st
import base64
# Fonction pour injecter du CSS personnalisé
def inject_css():
    css = """
    <style>
     /* Ajuster la largeur du conteneur principal */
    .main .block-container {
        max-width: 1300px;  /* Ajuste cette valeur pour changer la largeur */
        padding-left: 1rem;  /* Réduit la marge à gauche */
        padding-right: 1rem;  /* Réduit la marge à droite */
    }
    
    /* Autres styles personnalisés */
    .custom-button {
        background-color: #545454;
        color: #F6D9A7;
        font-size: 20px;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        font-family: 'Cormorant Garamond', serif !important;
    }

    h2 {
        color: #CC9623;
        font-family: 'Cormorant Garamond', serif !important;
    }

    p {
        color: #F5F5DC;
        font-family: 'Cormorant Garamond', serif !important;
        font-size: 18px;
        display: inline-block;
    }

    .stApp {
        background-color: #545454;
        font-family: 'Cormorant Garamond', serif !important;
 !important;  /* Forcer l'arrière-plan ici /
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


def inject_header():
    image_path = "C:/Users/laithe/Documents/personal document file/laithe/pays musulman/structure investissement musulmane/logo_blackgoldinvestment.jpg"
    with open(image_path, "rb") as image_file:
        image_base64 = base64.b64encode(image_file.read()).decode()
    # Chemin vers l'image locale

    header_html = f"""
        <style>
        .header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px;
            background-color: #545454;
            font-family: 'Cormorant Garamond', serif !important;
        }}
        .header img {{
            display: block;
            max-width: 200px;
            align-items: center;
        }}
        .header h1 {{
             color: #F6D9A7;
            font-family: 'Cormorant Garamond', serif !important;
            text-align: center;
        }}
        </style>

        <div class="header">
            <img src="data:image/jpg;base64,{image_base64}" alt="Logo">
        </div>
    """
    # Injection du code HTML
    st.markdown(header_html, unsafe_allow_html=True)
