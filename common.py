import os
from cryptography.hazmat.primitives import serialization
from sympy import gcd

# Chemin vers le répertoire contenant les fichiers de clés publiques PEM
directory_path = 'certificates'

# Listez les fichiers dans le répertoire
files = os.listdir(directory_path)

# Initialisez une liste pour stocker les valeurs n (modulos) extraites des clés publiques
n_values = []
cpt = 0
# Parcourez chaque fichier et extrayez la valeur n de la clé publique PEM
for file_name in files:
    file_path = os.path.join(directory_path, file_name)
    with open(file_path, 'rb') as file:
        pem_data = file.read()
        pem_key = serialization.load_pem_public_key(pem_data)
        try:
            n_value = pem_key.public_numbers().n
            cpt += 1
        except:
            pass
        n_values.append([file_name, n_value])

    if cpt == 2000:
        print(cpt)
        break

# Initialisez une liste pour stocker les facteurs communs
common_factors = []

# Effectuez le Batch GCD en comparant chaque combinaison de valeurs n
for i in range(len(n_values)):
    for j in range(i + 1, len(n_values)):
        n1, n2 = n_values[i][1], n_values[j][1]
        common_factor = gcd(n1, n2)
        if common_factor > 1:
            common_factors.append(
                [n_values[i][0], n_values[j][0], common_factor])

# Affichez les facteurs communs trouvés
if common_factors:
    print("Facteurs communs trouvés :")
    for factor in common_factors:
        print(factor)
else:
    print("Aucun facteur commun trouvé.")
