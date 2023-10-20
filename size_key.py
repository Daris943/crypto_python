from cryptography.hazmat.primitives import serialization

# Chemin vers le fichier contenant la clé publique au format PEM
pem_file_path = 'certificates/cert-751.pem'

# Charger la clé publique depuis le fichier PEM
with open(pem_file_path, 'rb') as file:
    pem_data = file.read()
    public_key = serialization.load_pem_public_key(pem_data)

# Obtenir la longueur de la clé en bits
key_length = public_key.key_size

print("Taille de la clé en bits:", key_length)
