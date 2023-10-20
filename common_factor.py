from sympy import gcd
import os

_source_folder = "certificates"

certs = []
cpt = 0

for index, path in enumerate(os.listdir(_source_folder)):
    # check if current path is a file
    if os.path.isfile(os.path.join(_source_folder, path)):
        full_path = _source_folder + "/" + path

        file = open(full_path)
        cert = file.read()
        certs.append(cert)
    if index % 10000 == 0:
        cpt += 10000
        print("cpt : ", cpt)

for cert in certs:
    common_factor = gcd(cert, [i for i in certs if i != cert])
    print(common_factor)
    break
