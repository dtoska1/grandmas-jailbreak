#!/usr/bin/env python3
from pathlib import Path
import subprocess, tarfile, hashlib, io, gzip, bz2, lzma
from email.utils import formatdate

repo = Path(__file__).resolve().parents[1]
debs = sorted((repo / "debs").glob("*.deb"))
if len(debs) != 2:
    raise SystemExit(f"STOP: expected exactly 2 .deb files in {repo/'debs'}, found {len(debs)}")

extra = {
    "com.local.grandmaphonetest": {
        "Icon": "https://dtoska1.github.io/grandmas-jailbreak/assets/grandmaphone-icon.png",
        "Depiction": "https://dtoska1.github.io/grandmas-jailbreak/depictions/grandmaphone.html",
        "Homepage": "https://dtoska1.github.io/grandmas-jailbreak/",
    },
    "com.local.grandmaclock": {
        "Icon": "https://dtoska1.github.io/grandmas-jailbreak/assets/grandmaclock-icon.png",
        "Depiction": "https://dtoska1.github.io/grandmas-jailbreak/depictions/grandmaclock.html",
        "Homepage": "https://dtoska1.github.io/grandmas-jailbreak/",
    },
}

entries=[]
for deb in debs:
    members=subprocess.check_output(["ar","-t",str(deb)], text=True).splitlines()
    cm=next((x for x in members if x.startswith("control.tar")),None)
    if not cm: raise SystemExit(f"STOP: no control.tar in {deb.name}")
    raw=subprocess.check_output(["ar","-p",str(deb),cm])
    with tarfile.open(fileobj=io.BytesIO(raw),mode="r:*") as tf:
        member=next((m for m in tf.getmembers() if m.name in ("control","./control")),None)
        if not member: raise SystemExit(f"STOP: control missing in {deb.name}")
        f=tf.extractfile(member)
        control=f.read().decode().strip()
    fields={}
    ordered=[]
    for line in control.splitlines():
        if ": " in line:
            k,v=line.split(": ",1); fields[k]=v; ordered.append(k)
    pkg=fields.get("Package")
    if pkg not in extra: raise SystemExit(f"STOP: unexpected package id {pkg}")
    for k in ("Icon","Depiction","Homepage"):
        fields.pop(k,None)
        if k in ordered: ordered.remove(k)
    lines=[]
    seen=set()
    for k in ordered:
        if k in seen: continue
        seen.add(k); lines.append(f"{k}: {fields[k]}")
    for k,v in extra[pkg].items(): lines.append(f"{k}: {v}")
    data=deb.read_bytes()
    lines += [
        f"Filename: debs/{deb.name}",
        f"Size: {len(data)}",
        f"MD5sum: {hashlib.md5(data).hexdigest()}",
        f"SHA1: {hashlib.sha1(data).hexdigest()}",
        f"SHA256: {hashlib.sha256(data).hexdigest()}",
    ]
    entries.append("\n".join(lines))

packages=("\n\n".join(entries)+"\n").encode()
(repo/"Packages").write_bytes(packages)
(repo/"Packages.gz").write_bytes(gzip.compress(packages, compresslevel=9, mtime=0))
(repo/"Packages.bz2").write_bytes(bz2.compress(packages, compresslevel=9))
(repo/"Packages.xz").write_bytes(lzma.compress(packages, preset=9))

idx=[repo/"Packages",repo/"Packages.gz",repo/"Packages.bz2",repo/"Packages.xz"]
def dig(p,a):
    h=hashlib.new(a); h.update(p.read_bytes()); return h.hexdigest()
lines=["Origin: Grandma's Jailbreak","Label: Grandma's Jailbreak","Suite: stable","Codename: stable","Version: 1.0","Architectures: iphoneos-arm64","Components: main","Description: GrandmaPhone and GrandmaClock packages by d",f"Date: {formatdate(usegmt=True)}","","MD5Sum:"]
for p in idx: lines.append(f" {dig(p,'md5')} {p.stat().st_size:16d} {p.name}")
lines.append("SHA1:")
for p in idx: lines.append(f" {dig(p,'sha1')} {p.stat().st_size:16d} {p.name}")
lines.append("SHA256:")
for p in idx: lines.append(f" {dig(p,'sha256')} {p.stat().st_size:16d} {p.name}")
(repo/"Release").write_text("\n".join(lines)+"\n")
print("Generated Packages indexes with Icon, Depiction and Homepage metadata for 2 packages.")
