# trilinos-testbed
Unified system for Trilinos testing 

This script is intended to create a standalone build of Trilinos. 
It downloads and builds the following without any other dependencies from the host machine:
- gcc
- MVAPICH2
- LAPACK
- Boost
- Trilinos

During the install process you may have to add "gcc-install/lib64" to the Library Path.

The additional Makefile and make.inc files are modified install files for LAPACK and will
be copied to the build directory. 

For whatever reason, LAPACK's build may fail towards the end. Re-running the build command seems to 
be a workaround. 
