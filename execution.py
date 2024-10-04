import json
import os

def execut(nom_fichier):
    nom = nom_fichier
    # Ouvrir le notebook Jupyter et lire le contenu
    with open(nom + '.ipynb', 'r', encoding='utf-8') as f:
        notebook_content = json.load(f)

    # Préparer une liste pour stocker le code extrait des cellules
    code_cells = []

    # Parcourir les cellules du notebook pour extraire les cellules de type "code"
    for cell in notebook_content['cells']:
        if cell['cell_type'] == 'code':
            # Extraire le source de la cellule et ajouter à la liste
            code = ''.join(cell['source'])
            code_cells.append(code)

    # Fusionner tous les morceaux de code en une seule chaîne de caractères
    full_code = '\n\n'.join(code_cells)

    # Écrire le code extrait dans le fichier Python
    with open(nom +'.py', 'w', encoding='utf-8') as f:
        f.write(full_code)

    print("Le fichier", nom+'.py', "a été créé avec le contenu de", nom +'.ipynb')

#############################################################################################
#############################################################################################

# Spécifiez le chemin du dossier
dossier = r"C:\Users\laithe\Documents\personal document file\laithe\projet tractopelle\dashboard operationel\pages"

# Lister tous les fichiers .ipynb dans le dossier
fichiers_ipynb = [f for f in os.listdir(dossier) if f.endswith('.ipynb')]

execut("app")
# Afficher les fichiers trouvés
for fichier in fichiers_ipynb:
    execut("pages/" + fichier[:-6])