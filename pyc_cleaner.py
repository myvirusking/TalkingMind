import os

input("press any key to delete all .pyc files -")

deleted_files = []
for subdir, dirs, files in os.walk(os.getcwd()):
    for file in files:
        if file[-3:] == "pyc":
            deleted_files.append(os.path.join(subdir,file))


for pyc_file in deleted_files:
    os.remove(pyc_file)
    print(" "+ pyc_file + " successfully deleted")

print(f"\n Total = {(len(deleted_files))} files deleted successfully.\n")

input("press any key for exit -")
    
