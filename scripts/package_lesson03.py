"""Package only the lesson's public source; never include local secrets or environments."""
from pathlib import Path
import zipfile

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"files/lesson-03"
FILES=("app.py","core.py","demo.py","requirements.txt","README.md","run-local.txt",
       ".gitignore",".streamlit/config.toml",".streamlit/secrets.toml.example")
target=ROOT/"files/lesson-03.zip"
with zipfile.ZipFile(target,"w",compression=zipfile.ZIP_DEFLATED) as bundle:
    for name in FILES:
        bundle.write(SOURCE/name,arcname="lesson-03/"+name)
with zipfile.ZipFile(target) as bundle:
    assert bundle.namelist()==["lesson-03/"+name for name in FILES]
    assert all(bundle.read("lesson-03/"+name)==(SOURCE/name).read_bytes() for name in FILES)
print(f"{target}: {len(FILES)} files, {target.stat().st_size} bytes")
