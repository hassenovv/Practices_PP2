# Practice 6 - Copy, back up and safely delete files
import os
import shutil
from pathlib import Path

folder = Path(__file__).parent
src = folder / "original.txt"
src.write_text("Important data\n")

# Copy and back up with shutil
shutil.copy(src, folder / "copy.txt")
shutil.copy2(src, folder / "original_backup.txt")  # also copies date info
print("Copied:", (folder / "copy.txt").read_text().strip())

# Delete safely: check first, then remove
for name in ["copy.txt", "original_backup.txt", "original.txt", "ghost.txt"]:
    p = folder / name
    if p.exists() and os.access(p, os.W_OK):
        p.unlink()
        print("Deleted", name)
    else:
        print("Skipped", name, "(missing or no permission)")
