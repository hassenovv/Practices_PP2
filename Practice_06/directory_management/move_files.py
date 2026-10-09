# Practice 6 - Move / copy files between directories
import shutil
from pathlib import Path

base = Path(__file__).parent / "move_demo"
src, dst = base / "from", base / "to"
src.mkdir(parents=True, exist_ok=True)
dst.mkdir(parents=True, exist_ok=True)

(src / "a.txt").write_text("A")
(src / "b.txt").write_text("B")

shutil.copy(src / "a.txt", dst / "a.txt")   # copy: stays in both
shutil.move(src / "b.txt", dst / "b.txt")   # move: leaves the old place
print("from:", sorted(p.name for p in src.iterdir()))
print("to:  ", sorted(p.name for p in dst.iterdir()))

shutil.rmtree(base)                          # clean up the whole demo
print("Cleaned up:", not base.exists())
