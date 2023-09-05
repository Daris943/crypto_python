from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives.asymmetric import padding
from datetime import datetime

# Création de l'authorité d'enregistrement
subject = issuer = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, u"FR"),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"Ile de France"),
    x509.NameAttribute(NameOID.LOCALITY_NAME, u"Paris"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"ESIEA"),
    x509.NameAttribute(NameOID.COMMON_NAME, u"esiea.fr"),
])

# read file
with open('certificate_store/cert.pem', 'rb') as cert_file:
    cert_data = cert_file.read()
    cert = x509.load_pem_x509_certificate(cert_data, default_backend())

# Durée de vie
print(cert.not_valid_after, type(cert.not_valid_after))

# validation de la structure du certificat (ignore la signature)
try:
    cert.public_key().verify(
        cert.signature,
        cert.tbs_certificate_bytes,
        padding.PKCS1v15(),
        cert.signature_hash_algorithm,
    )
    print("La signature du certificat est valide.")
except Exception as e:
    print("Erreur de vérification de la signature :", e)
    
if cert.issuer == subject and cert.not_valid_after >= datetime.now():
    print("Certificate is valid")
else :
    print("Certificate isn't valid...")