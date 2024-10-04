import streamlit as st
import pandas as pd
import numpy as np
from styles import inject_css, inject_header  # Importer la fonction depuis styles.py
import random
import seaborn as sns
import matplotlib.pyplot as plt
import math

# vecteur nombre de jour dans chaque mois de 2025
jours_par_mois_2025 = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

# Vecteur depense, chiffre d'affaire et benefice pour chaque jour de l'année
depenses_vecteur = np.zeros(365)  
chiffre_affaire_vecteur = np.zeros(365)  
benefice_vecteur = np.zeros(365)  

#Encodage jour type pannes vecteur : 0 journee normal; 1 panne 1; 2 panne 2 ect
jour_type_pannes_vecteur = np.zeros(365)  



# Données d'entrée utilisateur
st.sidebar.header("Paramètres d'investissement")
nombre_investisseurs = st.sidebar.number_input('Nombre d’investisseurs', value=10)
investissement_moyen_par_personne = st.sidebar.number_input('Investissement moyen par personne', value=6100)
duree_blocage_investissement = st.sidebar.number_input('Durée minimale du blocage de l’investissement de chaque investisseur (mois)', value=6)

st.sidebar.header("Paramètres à l'achat des tractopelles")
prix_unitaire_pelle = st.sidebar.number_input('Prix unitaire du tractopelle + marteau piqueur', value=50000)
nombre_pelle = st.sidebar.number_input('Nombre de tractopelle acheté', value = 1)
prix_douane_pelle = st.sidebar.number_input('Prix douane du tractopelle + marteau piqueur', value=5000)
prix_envoi_pelle = st.sidebar.number_input('Prix d’envoi du tractopelle + marteau piqueur', value=5000)

st.sidebar.header("Paramètres à l'achat des camion benne")
prix_unitaire_camion = st.sidebar.number_input('Prix unitaire du camion benne', value=30000)
nombre_camion = st.sidebar.number_input('Nombre de camion benne acheté', value=0)
prix_douane_camion = st.sidebar.number_input('Prix douane du camion benne', value=5000)
prix_envoi_camion = st.sidebar.number_input('Prix d’envoi du camion benne', value=5000)

st.sidebar.header("Paramètres associés aux salaires")
salaire_chauffeur = st.sidebar.number_input("Salaire mensuel d'un chauffeur", value=1000)
salaire_responsable = st.sidebar.number_input('Salaire mensuel du responsable', value=2000)

st.sidebar.header("Paramètres liés à la location du terrain de stockage des vehicules")
prix_location_terrain = st.sidebar.number_input("Coût de la location du terrain", value=1000)

# Beauté des ongles
inject_header()
inject_css()

st.header("Prix et nombre de jours de travail")
# Créer deux colonnes
col1, col2 = st.columns(2)

# Placer rentabilite_jour_pelle dans la première colonne
with col1:
    rentabilite_jour_pelle = st.number_input("Prix moyen d'une prestation du tractopelle (€)", value=1000, step=50)
    jours_travail_pelle_semaine  = st.number_input("Nombre de jours de travail par semaine du tractopelle", value=5, step=1)
    essence_mois_pelle  = st.number_input('Coût du carburant par mois par tractopelle', value=800)
    huile_mois_pelle  = st.number_input("Coût de l'huile et du lubifiant par mois par tractopelle", value=300)
    
# Placer rentabilite_jour_camion dans la deuxième colonne
with col2:
    rentabilite_jour_camion = st.number_input("Prix moyen d'une prestation d'un camion benne (€)", value=400, step=50)
    jours_travail_camion_semaine = st.number_input("Nombre de jours de travail par semaine d'un camion penne", value=5, step=1)
    essence_mois_camion = st.number_input('Coût du carburant par mois par camion benne', value=800)


# Titre de la page
# Définir les paramètres du modèle
st.header("Définition du modèle operationel prévisonnel")
# Créer un DataFrame initial pour que l'utilisateur puisse modifier les valeurs
data_type_panne_variables = {
    "Type de pannes": [
                 "Crevaison mineure", "Changement de pneu", 
                 "Problème hydraulique", "Accident de chantier"],
    "Jours d'arrêt par panne (jour)": [1, 10, 5, 1],  # Valeurs par défaut
    "Nombre de pannes sur l'année (jour)": [0, 0, 0, 0],  # Valeurs par défaut
}

# Créer un DataFrame
df_data_type_panne = pd.DataFrame(data_type_panne_variables)

# Utilisation de st.data_editor pour permettre à l'utilisateur de modifier les valeurs
editable_df_data_type_panne = st.data_editor(df_data_type_panne)

# Créer un DataFrame avec 1 ligne et 2 colonnes
data_total = {
    "Nombre de jours d'arrêt sur l'année": [editable_df_data_type_panne['Jours d\'arrêt par panne (jour)'].sum()],  # Valeur de la première colonne
    "Nombre de jours de pannes sur l'année": [editable_df_data_type_panne['Nombre de pannes sur l\'année (jour)'].sum()]  # Valeur de la deuxième colonne
}

# Ajouter une ligne "Total"
df_total = pd.DataFrame(data_total, index=["Total"])
# Afficher le tableau avec st.table()
st.dataframe(df_total)
# Récupérer les nouvelles valeurs depuis le tableau

jour_arret_crevaison_mineur = editable_df_data_type_panne.loc[0, "Jours d'arrêt par panne (jour)"]
jour_arret_changement_pneu = editable_df_data_type_panne.loc[1, "Jours d'arrêt par panne (jour)"]
jour_arret_probleme_hydrolique = editable_df_data_type_panne.loc[2, "Jours d'arrêt par panne (jour)"]
jour_arret_accident_chantier = editable_df_data_type_panne.loc[3, "Jours d'arrêt par panne (jour)"]

jour_arret_crevaison_mineur_frequentiel = editable_df_data_type_panne.loc[0, "Nombre de pannes sur l'année (jour)"]
jour_arret_changement_pneu_frequentiel = editable_df_data_type_panne.loc[1, "Nombre de pannes sur l'année (jour)"]
jour_arret_probleme_hydrolique_frequentiel = editable_df_data_type_panne.loc[2, "Nombre de pannes sur l'année (jour)"]
jour_arret_accident_chantier_frequentiel = editable_df_data_type_panne.loc[3, "Nombre de pannes sur l'année (jour)"]

cout_carburant_jour = 0
cout_main_oeuvre = 0
cout_entretien = 0


# Exemple d'emploi du temps (modifiable selon vos besoins)
st.header("Description financière et opérationelle journalières")
planification_tab, ressources_tab, cout_revenu_journalier_tab, accident_tab = \
st.tabs(["Planification des opérations", "Gestion des ressources journalières", "Coûts et revenus journaliers", "Scénarios accidentels"])

with planification_tab:
    data_planification = {
        "Heure": ["07h00-07h30", "07h30-08h00", "08h00-09h00", "09h00-12h00", "12h00-13h00", "13h00-16h00", "16h00-16h30", "16h30-17h00", "17h00-17h30"],
        "Tâche": [
            "Briefing", "Vérification des machines", "Départ vers le chantier", "Travail sur le chantier (matin)",
            "Pause déjeuner", "Travail sur le chantier (après-midi)", "Retour à l'entrepôt", 
            "Inspection et entretien des machines", "Briefing de fin de journée"
        ],
        "Détails/Actions": [
            "Réunion pour assigner les tâches du jour", "Contrôle du matériel, carburant, huile, état des pneus", 
            "Transport de l'équipement au chantier", "Terrassement, excavation, travaux de préparation",
            "Pause pour les employés", "Continuation des travaux sur le chantier", 
            "Retour des machines à l'entrepôt ou stationnement sur place", 
            "Vérification des machines : huile, carburant, maintenance", 
            "Discussion sur l'avancement des travaux, préparation du lendemain"
        ],
        "Personne/Responsable": [
            "Chef d'équipe", "Mécanicien", "Chauffeur", "Chauffeur et ouvriers", "Tous les employés", 
            "Chauffeur et ouvriers", "Chauffeur", "Mécanicien", "Chef d'équipe"
        ]
    }
    df = pd.DataFrame(data_planification)

    # Formater uniquement les colonnes numériques (int et float) sans séparateurs de milliers
    df[df.select_dtypes(include=[np.number]).columns] = df.select_dtypes(include=[np.number]).applymap(lambda x: f'{x:.0f}')

    st.dataframe(df)

with ressources_tab:
    data_ressources = {
    "Type de dépense": ["Carburant", "Huile et lubrifiant"],
    "Coût journalier (€)": [cout_carburant_jour, cout_main_oeuvre],
    "Commentaire": [
        "Varie en fonction de la durée et de l'intensité du travail", 
        "Changement ou ajout régulier"
    ]
}

    df = pd.DataFrame(data_ressources)

    # Formater uniquement les colonnes numériques (int et float) sans séparateurs de milliers
    df[df.select_dtypes(include=[np.number]).columns] = df.select_dtypes(include=[np.number]).applymap(lambda x: f'{x:.0f}')

    st.dataframe(df)

with cout_revenu_journalier_tab:
    depense_euro = 400
    benefice_euro = 1500
    gain_euro = benefice_euro - depense_euro
    data_cout_revenu_journalier = {
        "Variable financière et comptable journalière": ["Dépense", "Bénéfice", "Gain ou chiffre d'affaire"],
        "Valeur (€)": [depense_euro, benefice_euro, gain_euro ]
    }
    df = pd.DataFrame(data_cout_revenu_journalier)

    # Formater uniquement les colonnes numériques (int et float) sans séparateurs de milliers
    df[df.select_dtypes(include=[np.number]).columns] = df.select_dtypes(include=[np.number]).applymap(lambda x: f'{x:.0f}')

    st.dataframe(df)

with accident_tab:
    data_accident = {
        "Type d'accident": [
            "Crevaison mineure", 
            "Crevaison nécessitant un changement de pneu", 
            "Défaillance du système hydraulique", 
            "Accident sur le chantier"
        ],
        "Arrêt des opérations du à la panne (jour)": [
             str(jour_arret_crevaison_mineur), 
             str(jour_arret_changement_pneu), 
             str(jour_arret_probleme_hydrolique), 
             str(jour_arret_accident_chantier) 
        ],
        "Coût estimé (€)": [
            "100 ", 
            "5000 ", 
            "500 ", 
            "200 "
        ],
        "Commentaire": [
            "Petite réparation rapide sur place", 
            "Nécessite un changement de pneu", 
            "Réparation coûteuse nécessitant un expert", 
            "Assurance prend en charge une partie"
        ]
    }
    
    # Créer le DataFrame
    df_accident = pd.DataFrame(data_accident)

    # Formater uniquement les colonnes numériques (int et float) sans séparateurs de milliers
    df_accident[df_accident.select_dtypes(include=[np.number]).columns] = df_accident.select_dtypes(include=[np.number]).applymap(lambda x: f'{x:.0f}')

    # Afficher le tableau avec Streamlit
    st.dataframe(df_accident)

total_jour_panne_list = []
for i in range(editable_df_data_type_panne.shape[0]):
    total_jour_panne_list.append(editable_df_data_type_panne.loc[i, "Jours d'arrêt par panne (jour)"] * editable_df_data_type_panne.loc[i, "Nombre de pannes sur l'année (jour)"]) 


# Initialiser la liste pour stocker les nombres tirés A_i
n_eme_jours_pannes_vecteur = []

# Fonction pour vérifier si le nouveau Ai respecte les contraintes
def is_valid_Ai(Ai, i, A_list, total_jour_panne_list):
    # Vérification que Ai + total_jour_panne_list[i] <= 364
    if Ai + total_jour_panne_list[i] > 364:
        return False
    
    # Vérification que Ai n'appartient pas aux intervalles précédents
    for p in range(i):
        Ap = A_list[p]
        if Ai < Ap + total_jour_panne_list[p] and Ai + total_jour_panne_list[i] > Ap:
            return False
    
    return True
    
# Fixer une graine aléatoire pour la reproductibilité des résultats
#np.random.seed(42)
# Boucle pour tirer les nombres A_i
for i in range(editable_df_data_type_panne.shape[0]):
    while True:
        # Tirer un nombre aléatoire entre 0 et 364
        Ai = np.random.randint(0, 365)
        
        # Vérifier si Ai respecte les contraintes
        if is_valid_Ai(Ai, i, n_eme_jours_pannes_vecteur, total_jour_panne_list):
            n_eme_jours_pannes_vecteur.append(Ai)
            break

for i_indice , total_jour_type_panne in enumerate(n_eme_jours_pannes_vecteur):
    for nombre_type_panne in range(total_jour_panne_list[i_indice]):
        jour_type_pannes_vecteur[total_jour_type_panne + nombre_type_panne] = i_indice + 1        

# Creation des vecteurs dépenses, chiffre d'affaire et benefice pour chaque jours de l'année    

# Bouton pour revenir à la page d'accueil
if st.button("Retour à la page d'accueil"):
    switch_page("app")

# Calculs basés sur les formules fournies
capital_depart = nombre_investisseurs * investissement_moyen_par_personne
fond_depart_necessaire = (nombre_pelle * (prix_unitaire_pelle + prix_douane_pelle + prix_envoi_pelle) +
                          nombre_camion * (prix_unitaire_camion + prix_douane_camion + prix_envoi_camion))
caisse_depart = capital_depart - fond_depart_necessaire

essence_jour_pelle = essence_mois_pelle * 12 / 365
essence_jour_camion = essence_mois_camion * 12 / 365
huile_jour_pelle = huile_mois_pelle * 12 / 365
salaire_chauffeur_jour = salaire_chauffeur * 12 / 365
salaire_responsable_jour = salaire_responsable * 12 / 365


type_panne_chiffre_affaire_benefice_jour_dict = {}
for cle in range(editable_df_data_type_panne.shape[0]+1):
    if cle == 0:
        
        
        charge_variable_par_jour = (essence_jour_pelle + huile_jour_pelle) * nombre_pelle  + essence_jour_camion * nombre_camion  
        charge_fixe_par_jour = prix_location_terrain + salaire_responsable_jour + ( nombre_pelle + nombre_camion) * salaire_chauffeur_jour
        
        chiffre_affaire_jour_normal = rentabilite_jour_pelle + rentabilite_jour_camion
        depense_jour_normal = charge_variable_par_jour + charge_fixe_par_jour
    else:
        for i in range(1,editable_df_data_type_panne.shape[0]+1):
            if cle == i:        
                chiffre_affaire_jour_normal = 0
                depense_jour_normal = charge_fixe_par_jour + float(df_accident.iloc[i-1,2]) /float( editable_df_data_type_panne.loc[i-1, "Jours d'arrêt par panne (jour)"])
    type_panne_chiffre_affaire_benefice_jour_dict[int(cle)] = [depense_jour_normal,chiffre_affaire_jour_normal]
    

for indice, type_journee in enumerate(jour_type_pannes_vecteur):
    depenses_vecteur[indice] = type_panne_chiffre_affaire_benefice_jour_dict[int(type_journee)][0]
    chiffre_affaire_vecteur[indice] = type_panne_chiffre_affaire_benefice_jour_dict[int(type_journee)][1] 

benefice_vecteur = chiffre_affaire_vecteur - depenses_vecteur

data_benefice_total = {
"Bénéfice de l'année (€)" : np.sum(benefice_vecteur),
    "Gain net moyen par investisseur (€)" : np.sum(benefice_vecteur) / nombre_investisseurs
}
# Créer le DataFrame
df = pd.DataFrame(data_benefice_total, index=[0])

# Formater uniquement les colonnes numériques (int et float) sans séparateurs de milliers
df[df.select_dtypes(include=[np.number]).columns] = df.select_dtypes(include=[np.number]).applymap(lambda x: f'{x:.0f}')
# Afficher le tableau avec Streamlit
st.dataframe(df)

# Calculs basés sur les formules fournies
capital_depart = nombre_investisseurs * investissement_moyen_par_personne
fond_depart_necessaire = (nombre_pelle * (prix_unitaire_pelle + prix_douane_pelle + prix_envoi_pelle) +
                          nombre_camion * (prix_unitaire_camion + prix_douane_camion + prix_envoi_camion))
caisse_depart = capital_depart - fond_depart_necessaire


# Données pour le graphique
temps = ['Départ', 'Achats', 'Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Aout', 'Septembre', 'Octobre', 'Novembre', 'Décembre']
caisse_entreprise_vecteur = [round(capital_depart, 2), round(caisse_depart, 2)]  # Instants initiaux


start = 0
duree_rentabilisation = 0
# Calcul de l'évolution de la caisse
nouvelle_valeur = round(caisse_depart, 2)
for i in range(1, 13):  # Ajout des données pour chaque mois
    if round(caisse_depart, 2) >= 0:
         benefice_par_mois = np.sum(benefice_vecteur[start:start + jours_par_mois_2025[i-1]])  # Somme des bénéfices pour le mois
         start += jours_par_mois_2025[i-1]  # Mettre à jour le début du prochain mois
        
         nouvelle_valeur = nouvelle_valeur + benefice_par_mois
         caisse_entreprise_vecteur.append(nouvelle_valeur)
    else:
        caisse_entreprise_vecteur.append(round(caisse_depart, 2))

duree_rentabilisation = math.ceil( investissement_moyen_par_personne / (np.sum(benefice_vecteur) / (nombre_investisseurs*12) ) )

# Création du graphique en barres avec Seaborn
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x=temps, y=caisse_entreprise_vecteur, color='skyblue', ax=ax)

# Définir le titre et les labels
ax.set_title(f"Évolution de l'argent de la société\nGain net par mois moyen = $\mathbf{{{int(np.sum(benefice_vecteur) / (nombre_investisseurs*12) )}}}$ €\nDurée de rentabilité moyen par investisseur par rapport au gain net: $\mathbf{{{int(duree_rentabilisation)}}}$ mois", fontsize=14)
ax.set_xlabel("Temps", fontsize=12)
ax.set_ylabel("Montant en caisse (€)", fontsize=12)

# Ajuster la taille et la rotation des étiquettes de l'axe des abscisses
ax.tick_params(axis='x', labelsize=8)  # Taille de police des labels de l'axe des abscisses
plt.xticks(rotation=45)

# Afficher le graphique dans Streamlit ou dans un notebook
st.pyplot(fig)  # Si vous êtes dans Streamlit

