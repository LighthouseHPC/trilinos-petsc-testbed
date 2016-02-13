# trilinos-petsc-testbed
Unified system for Trilinos and PETSc testing 

This script is intended to create a standalone build of Trilinos and PETSc with minimal effort from the user. 
The only requirements are make, cmake, wget, and python 2.6+. 

The script will download, extract, and install the following libraries and compilers via a simple command line interface:
- gcc 5.3.0
- OpenMPI 1.10.2
- LAPACK 3.6.0
- Boost 1.60.0
- Trilinos 12.4.2
- PETSc 3.6.3

The additional files that are included in the repo are modified install files for some of the 
libraries. They will be automatically moved or copied to the appropriate build directories 
including one (Boost) to your home directory.  

# Trilinos Example
After Trilinos has been succesfully installed, you can test the state of the install using the included trilinos_test.cpp file. 
```
./do-configure-trilinos-test
make
mpirun -np 4 ./trilinos_test
```

