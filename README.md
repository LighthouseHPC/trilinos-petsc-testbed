# trilinos-petsc-testbed
Unified system for Trilinos and PETSc testing 

This script is intended to create a standalone build of Trilinos and PETSc with minimal effort from the user. 
The only requirements are make, cmake, wget, and python 2.6+. 

The script will download, extract, and install the following libraries and compilers:
- gcc 5.3.0
- OpenMPI 1.10.2
- LAPACK 3.6.0
- Boost 1.60.0
- Trilinos 12.4.2
- PETSc 3.6.3

The `extra_files` directory contains the basic install configuration files for the 
libraries. They will be automatically updated and then moved or copied to the appropriate 
build directories including one, Boost's `user-config.jam`, to your home directory.  

# Instructions
1. Run the `setup.py` script
2. Enter 'y' or 'n' to choose to download, extract, or install the various components
3. (for PETSc only) After PETSc has been configured you will need to follow the onscreen commands to finish the install process
4. Add the appropriate PETSc and Trilinos directories to your `$LD_LIBRARY_PATH`
5. *(Optional)* Add the gcc and OpenMPI compilers to your `$PATH`

# Trilinos Example
After Trilinos has been succesfully installed, you can test the state of the install using the included `trilinos_test.cpp` file. 
```
cd extra_files
./do-configure-trilinos-test
make
mpirun -np 4 ./trilinos_test
```

# Issues
This code has only been tested on a few systems and may have some unknown bugs. 
