import logging
import certstream
import requests
import base64
import ctl_parser_structures
from OpenSSL import crypto
from cryptography.hazmat.primitives import serialization
import os

certCount = 0
dir_path = "certificates"
# Iterate directory
for path in os.listdir(dir_path):
    # check if current path is a file
    if os.path.isfile(os.path.join(dir_path, path)):
        certCount += 1

def print_callback(message, context):
    
    logging.debug("Message -> {}".format(message))

    if message['message_type'] == "heartbeat":
        return

    if message['message_type'] == "certificate_update":
        all_domains = message['data']['leaf_cert']['all_domains']

        if len(all_domains) == 0:
            return
            
        url = message["data"]["cert_link"]
        
        results = requests.get(url)
        result = results.json()["entries"][0]
        
        cert_data = str(result["leaf_input"])
        cert_data = base64.b64decode(cert_data)
        
        leaf_cert = ctl_parser_structures.MerkleTreeHeader.parse(cert_data)
        
        if leaf_cert.LogEntryType == "X509LogEntryType":
            # We have a normal x509 entry
            cert_data_string = ctl_parser_structures.Certificate.parse(leaf_cert.Entry).CertData
            chain = [crypto.load_certificate(crypto.FILETYPE_ASN1, cert_data_string)]

            # Parse the `extra_data` structure for the rest of the chain
            extra_data = ctl_parser_structures.CertificateChain.parse(base64.b64decode(result['extra_data']))
            for cert in extra_data.Chain:
                saveToFile(crypto.load_certificate(crypto.FILETYPE_ASN1, cert.CertData).get_pubkey().to_cryptography_key().public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo,
                ))
                chain.append(crypto.load_certificate(crypto.FILETYPE_ASN1, cert.CertData))
        else:
            # We have a precert entry
            extra_data = ctl_parser_structures.PreCertEntry.parse(base64.b64decode(result['extra_data']))
            chain = [crypto.load_certificate(crypto.FILETYPE_ASN1, extra_data.LeafCert.CertData)]

            for cert in extra_data.Chain:
                saveToFile(crypto.load_certificate(crypto.FILETYPE_ASN1, cert.CertData).get_pubkey().to_cryptography_key().public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo,
                ))
                chain.append(
                    crypto.load_certificate(crypto.FILETYPE_ASN1, cert.CertData)
                )

        # Chain is now an array of X509 objects, leaf certificate first, ready for extraction!
        
        # print(chain)
        
def saveToFile(p_key) :
    global certCount
    
    if certCount % 100 == 0 :
        print(str(certCount) + " certificats saved to disk")
    
    with open('certificates/cert-' + str(certCount) + ".pem", 'wb') as f:
        f.write(p_key)
        
    certCount += 1
        
logging.basicConfig(format='[%(levelname)s:%(name)s] %(asctime)s - %(message)s', level=logging.INFO)

certstream.listen_for_events(print_callback, url='wss://certstream.calidog.io/')