import os
from cryptography.hazmat.primitives import serialization
from sympy import gcd

directory_path = 'certificates'

files = os.listdir(directory_path)

n_values = []
cpt = 0
# retrieve certificates
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

    # if cpt == 20:
    #     print(cpt)
    #     break

# create a list to keep result of batch gcd
common_factors = []
common_factors.append(["cert_1", "cert_2", "n_value"])

# execute batch gcd to find common factors
for i in range(len(n_values)):
    for j in range(i + 1, len(n_values)):
        n1, n2 = n_values[i][1], n_values[j][1]
        common_factor = gcd(n1, n2)
        if common_factor > 1:
            common_factors.append(
                [n_values[i][0], n_values[j][0], common_factor])

# save results in a file
with open("common_factor.txt", 'w') as f:
    for line in common_factors:
        i = ",".join(map(str, line))
        f.write(i + "\n")
