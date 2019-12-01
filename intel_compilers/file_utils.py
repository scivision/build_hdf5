#!/usr/bin/env python3
"""
Extract tar or zip file using Python from command line
"""
from pathlib import Path
import argparse
import zipfile
import tarfile
import hashlib


def extract_files(infile: Path, outdir: Path):

    infile = Path(infile).expanduser().resolve()

    if infile.suffix.lower() == ".zip":
        extract_zip(infile, outdir)
    elif infile.suffix.lower() in (".tar", ".gz", ".bz2", ".xz"):
        extract_tar(infile, outdir)
    else:
        raise ValueError(f"Not sure how to decompress {infile}")


def file_checksum(fn: Path, mode: str, filehash: str) -> bool:
    h = hashlib.new(mode)
    h.update(fn.read_bytes())
    return h.hexdigest() == filehash


def extract_zip(fn: Path, outpath: Path, overwrite: bool = False):
    outpath = Path(outpath).expanduser().resolve()
    # need .resolve() in case intermediate relative dir doesn't exist
    if outpath.is_dir() and not overwrite:
        return

    fn = Path(fn).expanduser().resolve()
    with zipfile.ZipFile(fn) as z:
        z.extractall(outpath.parent)


def extract_tar(fn: Path, outpath: Path, overwrite: bool = False):
    outpath = Path(outpath).expanduser().resolve()
    # need .resolve() in case intermediate relative dir doesn't exist
    if outpath.is_dir() and not overwrite:
        return

    fn = Path(fn).expanduser().resolve()
    if not fn.is_file():
        raise FileNotFoundError(fn)  # keep this, tarfile gives confusing error
    with tarfile.open(fn) as z:
        z.extractall(outpath.parent)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("infile", help="compressed file to extract")
    p.add_argument("outpath", help="path to extract into")
    P = p.parse_args()

    extract_files(P.infile, P.outpath)
