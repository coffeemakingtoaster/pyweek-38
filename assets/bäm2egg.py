import os
import subprocess

def convert_egg_to_bam(directory):
    # Walk through all directories and files
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".bam"):
                egg_file = os.path.join(root, file)
                bam_file = egg_file.replace(".bam", ".egg")

                # Prepare the egg2bam command
                command = ["bam2egg","-o", bam_file, egg_file]
                print(f"Converting: {egg_file} -> {bam_file}")

                try:
                    # Execute the command
                    subprocess.run(command, check=True)
                    print(f"Successfully converted: {egg_file}")
                except subprocess.CalledProcessError as e:
                    print(f"Failed to convert {egg_file}. Error: {e}")

if __name__ == "__main__":
    folder_path = input("Enter the path to the folder: ")
    convert_egg_to_bam(folder_path)