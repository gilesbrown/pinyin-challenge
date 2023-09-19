import csv
import requests
import tempfile
import shutil
from functools import cache
from pathlib import Path


from gzip import GzipFile
from importlib import resources


url = "https://www.mdbg.net/chinese/export/cedict/cedict_1_0_ts_utf-8_mdbg.txt.gz"

tempdir = tempfile.TemporaryDirectory()

# we only need to download once
@cache
def download_to_tempdir():
    tempfile = Path(tempdir.name).joinpath(url.split('/')[-1])
    # NOTE the stream=True parameter below
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(str(tempfile), 'wb') as f:
            shutil.copyfileobj(GzipFile(fileobj=r.raw), f)
    return tempfile
