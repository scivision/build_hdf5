# Intel compilers (icc, icpc, ifort) HDF5 build scripts

These scripts use Python for ease and portability.
They automatically download and extract the HDF5 and prereq source code, and compile using GNU Make.


## Prereqs

* C compiler
* Fortran / C++ compiler


### Linux

additional prereqs:

* autoconf
* automake
* libtools


### Windows

HDF5 on Windows currently requires CMake.