import os
from cryptography.hazmat.primitives import serialization

# Chemin vers le répertoire contenant les fichiers de clés publiques PEM
directory_path = 'certificates'

# Listez les fichiers dans le répertoire
files = os.listdir(directory_path)

n_values = []
cpt_rsa = 0
cpt_ec = 0
cpt_other = 0

for file_name in files:

    file_path = os.path.join(directory_path, file_name)
    with open(file_path, 'rb') as file:
        pem_data = file.read()
        pem_key = serialization.load_pem_public_key(pem_data)
        try:
            n_value = pem_key.public_numbers().n
            cpt_rsa += 1
        except:
            try:
                n_value = pem_key.public_numbers().y
                cpt_ec += 1
            except:
                cpt_other += 1

print("rsa : ", cpt_rsa)
print("ec : ", cpt_ec)
print("other : ", cpt_other)
