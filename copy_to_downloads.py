import shutil
import os

files_to_copy = [
    "Intelligenz_TalentAssess_360_Executive_Dossier.docx",
    "Intelligenz_TalentAssess_360_CEO.pptx",
]

downloads_dir = r"C:\Users\User\Downloads"

for f in files_to_copy:
    if os.path.exists(f):
        dest = os.path.join(downloads_dir, f)
        shutil.copy2(f, dest)
        print(f"Copied {f} -> {dest}")
    else:
        print(f"File not found: {f}")
