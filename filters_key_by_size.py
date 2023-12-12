from cryptography.hazmat.primitives import serialization
import os
import shutil

directory_path = 'certificates'
directory_path_sorted = 'sorted_certificates'

files = os.listdir(directory_path)
certs = []

cpt = 0
# retrieve certificates
for file_name in files:
    file_path = os.path.join(directory_path, file_name)
    with open(file_path, 'rb') as file:
        pem_data = file.read()
        public_key = serialization.load_pem_public_key(pem_data)
        key_length = public_key.key_size
        certs.append([file_name, key_length])
        cpt += 1

        if cpt % 20000 == 0:
            print("cpt = ", cpt)

print("--------------")
print("finish to load certificates")

# apply a bubble sort algo
n = len(certs)
for i in range(n):
    for j in range(0, n - i - 1):
        if certs[j][1] > certs[j + 1][1]:
            certs[j], certs[j + 1] = certs[j + 1], certs[j]
    if i % 1000 == 0:
        print("tri : ", i)
print("end of the bubble sort")

# apply a quick sort
if len(certs) <= 1:
    pass
else:
    pivot = certs[0]
    less = [cert for cert in certs[1:] if cert[1] <= pivot[1]]
    greater = [cert for cert in certs[1:] if cert[1] > pivot[1]]
    sorted_certs = less + [pivot] + greater
print("quick sort finish")

# copy order in a txt
f = open("sorted_order_v2.txt", 'w')

cpt_copy = 0

# copy certificates in a new dir after sort
for filename, key_length in sorted_certs:  # certs:
    # source_path = os.path.join(directory_path, filename)
    # dest_path = os.path.join(directory_path_sorted, filename)
    # shutil.copyfile(source_path, dest_path)
    f.write(filename + ", " + str(key_length) + "\n")

    cpt_copy += 1
