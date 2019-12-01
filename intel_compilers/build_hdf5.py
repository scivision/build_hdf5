#!/usr/bin/env python3
"""
Build HDF5 for Intel compilers
"""
from pathlib import Path
import os
import sys
import typing
import argparse
import subprocess

from file_utils import extract_files


def compiler_intel() -> typing.Dict[str, str]:
    """
    returns environment variables for Intel compilers, in case not already set
    """

    var = {"FC": "ifort"}
    if os.name == "nt":
        var.update({"CC": "icl", "CXX": "icl"})
    else:
        var.update({"CC": "icc", "CXX": "icpc"})

    return var


def builder(srcdir: Path, prefix: typing.Union[str, Path]):
    """
    do the HDF5 build
    """
    srcdir = Path(srcdir).expanduser().resolve()
    builddir = srcdir / "build"

    if srcdir.is_file():
        archive = srcdir
        if archive.suffix == ".zip":
            srcdir = archive.with_suffix("")
        else:
            srcdir = archive.with_suffix("").with_suffix("")
        extract_files(archive, srcdir)

    if not srcdir.is_dir():
        raise NotADirectoryError(srcdir)

    compenv = compiler_intel()

    if os == "nt":
        print(
            "There are known issues with Intel Fortran and Visual Studio 16.3 that may cause syntax errors to emerge at build.",
            "https://developercommunity.visualstudio.com/content/problem/715817/icl-problem-with-nodiscard-seen-in-visual-studio-1.html",
            file=sys.stderr,
        )

    # cmd = ['ctest', '-S', 'HDF5config.cmake,BUILD_GENERATOR=Ninja', '-C' ,'Release', '-VV', '-O', 'hdf5.log']
    cmd = [
        "cmake",
        "-G",
        "Ninja",
        "-B",
        str(builddir),
        "-DHDF5_BUILD_FORTRAN:BOOL=OFF",
        "-DCMAKE_BUILD_TYPE:STRING=Release",
        "-DHDF5_ENABLE_SZIP_SUPPORT:BOOL=OFF",
        "-DHDF5_ENABLE_Z_LIB_SUPPORT:BOOL=OFF",
        "-DBUILD_SHARED_LIBS:BOOL=OFF",
        "-DBUILD_TESTING:BOOL=OFF",
        "-DHDF5_BUILD_TOOLS:BOOL=OFF",
    ]

    print("\n", " ".join(cmd), "\n")
    subprocess.check_call(cmd, cwd=srcdir, env=os.environ.update(compenv))

    subprocess.check_call(["cmake", "--build", str(builddir)], cwd=srcdir)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("srcdir", help="path of HDF5 source code")
    p.add_argument("prefix", help="path to install HDF5 under")
    P = p.parse_args()

    builder(P.srcdir, P.prefix)
