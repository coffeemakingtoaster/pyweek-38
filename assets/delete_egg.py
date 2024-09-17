import os
import subprocess

def del_egg(directory): 
    # Walk through all directories and files
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".egg"):
                # Construct the full file path
                file_path = os.path.join(root, file)
                try:
                    # Remove the .egg file
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")

if __name__ == "__main__":
    folder_path = input("Enter the path to the folder: ")
    del_egg(folder_path)