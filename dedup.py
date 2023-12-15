import os
import hashlib

_source_folder = "certificates"
_target_folder = "certificates_dedup"

files = {}      # dictionnaire


def delete_files_in_directory(directory_path):
    try:
        files = os.listdir(directory_path)
        for file in files:
            file_path = os.path.join(directory_path, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
    except OSError:
        print("Error occurred while deleting files.")


# delete_files_in_directory(_target_folder)

for path in os.listdir(_source_folder):
    # check if current path is a file
    if os.path.isfile(os.path.join(_source_folder, path)):
        full_path = _source_folder + "/" + path

        file = open(full_path)
        targetFile = open(_target_folder + "/" + path, "w")

        if hashlib.sha3_256(file.read().encode("utf-8")).hexdigest() in files:
            print("Find dupe : " + path + " dup path : " +
                  str(files[hashlib.sha3_256(file.read().encode("utf-8")).hexdigest()][0]))
            continue

        files[hashlib.sha3_256(file.read().encode("utf-8")).hexdigest()] = [
            path,
            os.path.getsize(full_path)
        ]

        print(files)
        print("----------")

        # {
        #     "a7ffc6f8bf1ed76651c14756a061d662f580ff4de43b49fa82d80a4b80f8434a" => [
        #         0 => "/lien",   // path
        #         1 => 256        // taille
        #     ],
        #     "drhfg:hkjbv" => [
        #         0 => "/lien",   // path
        #         1 => 256        // taille
        #     ],
        #     "drhfg:hkjbv" => [
        #         0 => "/lien",   // path
        #         1 => 256        // taille
        #     ],
        # }

        print(hashlib.sha3_256(file.read().encode("utf-8")).hexdigest())

        content = file.read()
        targetFile.write(content)

        targetFile.close()
        file.close()

print("Operation finished")
print(files, type(files))

print("----------")

files_sorted = sorted(files, key=lambda file: file[1])

print(files_sorted, type(files_sorted))

for f in files_sorted:
    print(f, type(f))
