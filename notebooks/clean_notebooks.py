#!/usr/bin/env python
# POC: Guoqing.Ge@noaa.gov
#
import sys
import os
from pathlib import Path
from nbclean import NotebookCleaner

if len(sys.argv) != 2:
    print(f"Usage: {os.path.basename(sys.argv[0])} <filename/directory>")
    exit()
# ~~
tmp = sys.argv[1].rstrip("/")
files = []
if os.path.isdir(tmp):  # or tmp=="." or tmp=="..":
    for file in Path(tmp).glob("*.ipynb"):  # recursively glob: rglob
        if file.is_file():
            files.append(file)
else:
    files.append(tmp)

for filename in files:
    nb = NotebookCleaner(str(filename))
    nb.clear('output')

    for cell in nb.ntbk.cells:
        if 'execution_count' in cell:
            cell['execution_count'] = None

        # Remove UI metadata like jp-MarkdownHeadingCollapsed
        if 'metadata' in cell and isinstance(cell['metadata'], dict):
            cell['metadata'].pop('jp-MarkdownHeadingCollapsed', None)

    # nb.clear('metadata', preserve=["kernelspec", "language_info"])
    nb.save(str(filename))
