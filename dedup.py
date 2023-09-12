import os
import hashlib

_source_folder = "certificates"
_target_folder = "certificates_clean"

files = {}

def delete_files_in_directory(directory_path):
   try:
     files = os.listdir(directory_path)
     for file in files:
       file_path = os.path.join(directory_path, file)
       if os.path.isfile(file_path):
         os.remove(file_path)
   except OSError:
     print("Error occurred while deleting files.")

delete_files_in_directory(_target_folder)

for path in os.listdir(_source_folder):
    # check if current path is a file
    if os.path.isfile(os.path.join(_source_folder, path)):
        file = open(_source_folder + "/" + path)
        targetFile = open(_target_folder + "/" + path, "w")
        
        if hashlib.sha3_256(file.read().encode("utf-8")).hexdigest() in files :
            print("Find dupe : " + path)
            continue
            
        files[hashlib.sha3_256(file.read().encode("utf-8")).hexdigest()] = path
        
        content = file.read()
        targetFile.write(content)
        
        targetFile.close()
        file.close()
        
print("Operation finished")