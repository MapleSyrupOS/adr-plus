#!/usr/bin/env python3
"""make-manifest.py -- write and check MANIFEST.sha256, the list of files a follower copies.

ADR+ is released as numbered versions (SPEC.md S7). A project that follows a version
copies its payload and records which version it follows; a check in that project
fails when its copy differs from the release. MANIFEST.sha256 is what that check
compares against: one line per payload file, `<sha256>  <path>` (the format
`sha256sum -c` reads), sorted by path.

The payload is VERSION, the schema, the two tools (adrplus.py and adr-yaml.py) and
the converter's fixtures. This tool, the spec and the repository's own files are not
in it.

  python3 tools/make-manifest.py            write MANIFEST.sha256
  python3 tools/make-manifest.py --check    exit 1 if MANIFEST.sha256 is missing or does not
                                            match the payload, naming each file that differs
  python3 tools/make-manifest.py --self-test

Run it again whenever a payload file changes; CI runs --check. Standard library only;
Python 3.8 or later.
"""
from __future__ import annotations

import argparse
import hashlib
import pathlib
import shutil
import sys
import tempfile
from typing import Dict, List

ROOT = pathlib.Path(__file__).resolve().parent.parent
MANIFEST = "MANIFEST.sha256"
PAYLOAD_FILES = ("VERSION", "schema/adr-plus.schema.json", "tools/adrplus.py", "tools/adr-yaml.py")
PAYLOAD_DIRS = ("tools/fixtures",)


def payload(root: pathlib.Path) -> List[str]:
    """The payload's paths relative to `root`, sorted, with forward slashes."""
    found = [f for f in PAYLOAD_FILES if (root / f).is_file()]
    for d in PAYLOAD_DIRS:
        found.extend(p.relative_to(root).as_posix() for p in (root / d).rglob("*") if p.is_file())
    return sorted(found)


def digest(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def render(root: pathlib.Path) -> str:
    return "".join(f"{digest(root / rel)}  {rel}\n" for rel in payload(root))


def read_manifest(root: pathlib.Path) -> Dict[str, str]:
    out: Dict[str, str] = {}
    for line in (root / MANIFEST).read_text(encoding="utf-8").splitlines():
        sha, _, rel = line.partition("  ")
        if rel:
            out[rel] = sha
    return out


def problems(root: pathlib.Path) -> List[str]:
    """Every way MANIFEST.sha256 disagrees with the payload, one line each."""
    if not (root / MANIFEST).is_file():
        return [f"{MANIFEST}: missing"]
    listed = read_manifest(root)
    out: List[str] = []
    present = payload(root)
    for rel in present:
        if rel not in listed:
            out.append(f"{rel}: payload file not listed in {MANIFEST}")
        elif listed[rel] != digest(root / rel):
            out.append(f"{rel}: content differs from {MANIFEST}")
    for rel in listed:
        if rel not in present:
            out.append(f"{rel}: listed in {MANIFEST} but missing")
    return out


def check(root: pathlib.Path) -> int:
    bad = problems(root)
    for line in bad:
        print(f"DRIFT {line}")
    if bad:
        print(f"make-manifest: FAIL -- {len(bad)} file(s) disagree with {MANIFEST}; run make-manifest.py")
        return 1
    print(f"make-manifest: PASS -- {len(payload(root))} payload files match {MANIFEST}")
    return 0


def self_test() -> int:
    failed = 0

    def arm(name: str, ok: bool, why: str = "") -> None:
        nonlocal failed
        failed += 0 if ok else 1
        print(f"  {'ok  ' if ok else 'FAIL'} {name}{'' if ok else ' -- ' + why}")

    print("make-manifest --self-test")
    with tempfile.TemporaryDirectory(prefix="make-manifest-") as td:
        tree = pathlib.Path(td) / "tree"
        for rel in payload(ROOT):
            (tree / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(ROOT / rel, tree / rel)
        (tree / MANIFEST).write_text(render(tree), encoding="utf-8")
        arm("a fresh manifest matches its payload", problems(tree) == [], str(problems(tree)))
        arm("the manifest lists the payload and nothing else",
            sorted(read_manifest(tree)) == payload(tree) and MANIFEST not in read_manifest(tree))
        target = tree / "tools" / "adrplus.py"
        original = target.read_bytes()
        target.write_bytes(original[:-1] + bytes([original[-1] ^ 1]))
        bad = problems(tree)
        arm("red arm: one changed byte fails naming the file",
            bad == ["tools/adrplus.py: content differs from MANIFEST.sha256"], str(bad))
        target.write_bytes(original)
        extra = tree / "tools" / "fixtures" / "adr-yaml" / "extra.md"
        extra.write_text("x\n", encoding="utf-8")
        bad = problems(tree)
        arm("red arm: a payload file not in the manifest fails naming it",
            bad == ["tools/fixtures/adr-yaml/extra.md: payload file not listed in MANIFEST.sha256"], str(bad))
        extra.unlink()
        (tree / "VERSION").unlink()
        bad = problems(tree)
        arm("red arm: a listed file that is gone fails naming it",
            bad == ["VERSION: listed in MANIFEST.sha256 but missing"], str(bad))
        shutil.copy(ROOT / "VERSION", tree / "VERSION")
        (tree / MANIFEST).unlink()
        arm("red arm: a missing manifest fails", problems(tree) == ["MANIFEST.sha256: missing"], str(problems(tree)))
    print(f"make-manifest --self-test: {'FAIL' if failed else 'PASS'} ({failed} failed)")
    return 1 if failed else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--root", default=str(ROOT))
    args = ap.parse_args()
    root = pathlib.Path(args.root)
    if args.self_test:
        return self_test()
    if args.check:
        return check(root)
    (root / MANIFEST).write_text(render(root), encoding="utf-8")
    print(f"make-manifest: wrote {MANIFEST} ({len(payload(root))} files)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
