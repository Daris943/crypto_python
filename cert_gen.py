import datetime
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
import uuid
import os
import time

# environ 5sec / 100 cert
nb_certificates = 1_000_000

def delete_files_in_directory(directory_path):
   try:
     files = os.listdir(directory_path)
     for file in files:
       file_path = os.path.join(directory_path, file)
       if os.path.isfile(file_path):
         os.remove(file_path)
   except OSError:
     print("Error occurred while deleting files.")

# suppression des certificats précédents
delete_files_in_directory("certificate_store")
delete_files_in_directory("key_store/private")
delete_files_in_directory("key_store/public")

start = time.time()

# Création de l'authorité d'enregistrement
subject = issuer = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, u"FR"),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"Ile de France"),
    x509.NameAttribute(NameOID.LOCALITY_NAME, u"Paris"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"ESIEA"),
    x509.NameAttribute(NameOID.COMMON_NAME, u"esiea.fr"),
])

for i in range(0, nb_certificates):
    
    if i % 100 == 0:
        print("Starting generating cert nb " + str(i) + ". Time elapsed: " + str(time.time() - start))
    
    # Création de la clé privée
    key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    uuid_value = uuid.uuid4();
    id = uuid_value.hex

    with open("key_store/private/private_key_" + id + ".key", "wb") as f:
        f.write(key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.BestAvailableEncryption(b"passphrase"),
        ))

    cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.datetime.now(datetime.timezone.utc)
    ).not_valid_after(
        # Our certificate will be valid for 10 days
        datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=10)
    ).add_extension(
        x509.SubjectAlternativeName([x509.DNSName(u"localhost")]),
        critical=False,
    # Sign our certificate with our private key
    ).sign(key, hashes.SHA256())
    # Write our certificate out to disk.

    with open("key_store/public/public_key_" + id + ".key", "wb") as f:
        f.write(key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))

    with open("certificate_store/cert_" + id + ".pem", "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))
        
print("completed in: " + time.time() - start)