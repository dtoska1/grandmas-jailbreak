#!/usr/bin/env python3
from pathlib import Path
import hashlib,gzip,bz2,lzma
repo=Path(__file__).resolve().parents[1]
raw=(repo/'Packages').read_bytes()
stanzas=[x for x in raw.decode().strip().split('\n\n') if x.strip()]
assert len(stanzas)==2, f"expected 2 packages, got {len(stanzas)}"
for s in stanzas:
    f={}
    for line in s.splitlines():
        if ': ' in line:
            k,v=line.split(': ',1); f[k]=v
    path=repo/f['Filename']; data=path.read_bytes()
    assert len(data)==int(f['Size'])
    assert hashlib.sha256(data).hexdigest()==f['SHA256']
    for key in ('Icon','Depiction','Homepage'): assert key in f, f"{f['Name']} missing {key}"
    print('OK:',f['Name'],f['Version'])
assert gzip.decompress((repo/'Packages.gz').read_bytes())==raw
assert bz2.decompress((repo/'Packages.bz2').read_bytes())==raw
assert lzma.decompress((repo/'Packages.xz').read_bytes())==raw
print('FINAL PUBLIC REPO CHECK PASSED')
