from imports import subprocess, sys

subprocess.run([
    sys.executable,
    "-m", "PyInstaller",
    "--onedir",
    "--windowed",
    "--add-data", "Textures;Textures",
    "--add-data", "Saves;Saves",
    "--add-data", "audio;audio",
    "main.py"
], check = True)

print("\nBuild Complete")
print("Executable: dist\\main\\main.exe")