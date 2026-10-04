"""T-014: extract pinned Windows R binary packages into task-owned library.

No installers, registry, environment persistence or compilation. Dependencies
are resolved from CRAN R-4.4 and Bioconductor-3.20 R-4.4 PACKAGES metadata.
"""
import gzip
import hashlib
import json
from pathlib import Path
import re
import urllib.request
import zipfile

ROOT = Path("D:/RCA-ext/work/T-014")
OUT = Path(__file__).resolve().parent
DOWNLOAD = ROOT / "downloads"
LIB = ROOT / "R-library"
DOWNLOAD.mkdir(parents=True, exist_ok=True)
LIB.mkdir(parents=True, exist_ok=True)
records = []
REPOS = [
    "https://cran.r-project.org/bin/windows/contrib/4.4/",
    "https://bioconductor.posit.co/packages/3.20/bioc/bin/windows/contrib/4.4/",
]
base = set("R base boot class cluster codetools compiler datasets foreign graphics grDevices grid KernSmooth lattice MASS Matrix methods mgcv nlme nnet parallel rpart spatial splines stats stats4 survival tcltk tools utils".split())


def save_records():
    (OUT/"r-downloads.json").write_text(json.dumps(records, indent=2), encoding="utf-8")


def fetch(url, dest):
    print("DOWNLOAD_BEGIN", url, flush=True)
    with urllib.request.urlopen(url, timeout=60) as response:
        payload=response.read()
    dest.write_bytes(payload)
    record={"url":url,"path":str(dest),"bytes":len(payload),"sha256":hashlib.sha256(payload).hexdigest(),"md5":hashlib.md5(payload).hexdigest()}
    records.append(record);save_records()
    print("DOWNLOAD_END",len(payload),url,flush=True)
    return payload


def parse_dcf(text):
    result=[]
    for block in text.split("\n\n"):
        fields={};last=None
        for line in block.splitlines():
            if line.startswith((" ","\t")) and last:
                fields[last]+=" "+line.strip()
            elif ":" in line:
                last,value=line.split(":",1);fields[last]=value.strip()
        if "Package" in fields:
            result.append(fields)
    return result


packages={}
for index,repo in enumerate(REPOS):
    payload=fetch(repo+"PACKAGES.gz",DOWNLOAD/f"packages-{index}.gz")
    for fields in parse_dcf(gzip.decompress(payload).decode("utf-8")):
        fields["repo"]=repo
        packages.setdefault(fields["Package"],fields)

planned={}
def require(package):
    if package in base or package in planned:
        return
    if package not in packages:
        raise RuntimeError("No binary dependency: "+package)
    fields=packages[package];planned[package]=fields
    for field in ("Depends","Imports"):
        for item in fields.get(field,"").split(","):
            dependency=re.sub(r"\s*\(.*\)","",item).strip()
            if dependency:
                require(dependency)

require("pcalg")
assert planned["pcalg"]["Version"]=="2.7-12", planned["pcalg"]
(OUT/"r-packages-plan.json").write_text(json.dumps(planned,indent=2),encoding="utf-8")
print("PACKAGES_PLAN",len(planned),sorted(planned),flush=True)
bytes_total=86248441+520705+sum(record["bytes"] for record in records)
for package,fields in sorted(planned.items()):
    filename=f"{package}_{fields['Version']}.zip"
    url=fields["repo"]+filename
    with urllib.request.urlopen(urllib.request.Request(url,method="HEAD"),timeout=60) as response:
        advertised=int(response.headers.get("Content-Length","0"))
    if advertised and bytes_total+advertised>200_000_000:
        raise RuntimeError("Estimated 200 MB setup budget exceeded")
    payload=fetch(url, DOWNLOAD/filename);bytes_total+=len(payload)
    if bytes_total>200_000_000:
        raise RuntimeError("Actual 200 MB setup budget exceeded")
    md5=fields.get("MD5sum")
    if md5 and hashlib.md5(payload).hexdigest()!=md5:
        raise RuntimeError("Package MD5 mismatch: "+package)
    with zipfile.ZipFile(DOWNLOAD/filename) as archive:
        for info in archive.infolist():
            dest=(LIB/info.filename).resolve()
            if LIB.resolve() not in dest.parents and dest!=LIB.resolve():
                raise RuntimeError("Unsafe archive path: "+info.filename)
        archive.extractall(LIB)
    records[-1]["metadata_md5_match"]=(not md5 or hashlib.md5(payload).hexdigest()==md5)
    save_records()
    print("PACKAGE_EXTRACTED",package,fields["Version"],flush=True)
print("DONE",bytes_total,flush=True)
