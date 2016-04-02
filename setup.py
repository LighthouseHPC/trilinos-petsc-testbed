#!/usr/bin/env python
import subprocess
import urllib
import os
import tarfile
import shutil
import errno
try:
    import psutil
    cpuCount = psutil.cpu_count()
except:
    cpuCount = 4
LIBDIR = ''
percentage = 0
download_progress = 0


def dl_progress(block_no, block_size, file_size):
    total = file_size / block_size
    global percentage
    if percentage == int(100 * float(block_no) / float(total)):
        print('Percentage complete: %i' % percentage)
        percentage += 10


def download_gcc():
    global percentage
    percentage = 0
    print('Downloading gcc 5.3.0')
    urllib.urlretrieve('ftp://ftp.gnu.org/gnu/gcc/gcc-5.3.0/gcc-5.3.0.tar.bz2',
                       'gcc-5.3.0.tar.bz2', reporthook=dl_progress)
    print('Downloaded gcc 5.3.0')


def download_openmpi():
    global percentage
    percentage = 0
    print('Downloading openmpi 1.10.2')
    urllib.urlretrieve(
        'http://www.open-mpi.org/software/ompi/v1.10/downloads/openmpi-1.10.2.tar.gz',
        'openmpi-1.10.2.tar.gz', reporthook=dl_progress)
    print('Downloaded openmpi 1.10.2') 


def download_lapack():
    global percentage
    percentage = 0
    print('Downloading LAPACK 3.6.0')
    urllib.urlretrieve('http://www.netlib.org/lapack/lapack-3.6.0.tgz',
                       'lapack-3.6.0.tgz', reporthook=dl_progress)
    print('Downloaded LAPACK 3.6.0')


def download_boost():
    global percentage
    percentage = 0
    print('Downloading Boost 1.60.0')
    urllib.urlretrieve(
        'http://sourceforge.net/projects/boost/files/boost/1.60.0/boost_1_60_0.tar.bz2/download',
        'boost_1_60_0.tar.bz2', reporthook=dl_progress)
    print('Downloaded Boost 1.60.0')


def download_trilinos():
    global percentage
    percentage = 0
    print('Downloading Trilinos 12.4.2')
    urllib.urlretrieve(
        'http://trilinos.csbsju.edu/download/files/trilinos-12.4.2-Source.tar.bz2',
        'trilinos-12.4.2.tar.bz2', reporthook=dl_progress)
    print('Downloaded Trilinos 12.4.2')

def download_petsc():
    global percentage
    percentage = 0
    print('Downloading PETSc 3.6.3')
    urllib.urlretrieve(
        'http://ftp.mcs.anl.gov/pub/petsc/release-snapshots/petsc-3.6.3.tar.gz',
        'petsc-3.6.3.tar.gz', reporthook=dl_progress)
    print('Downloaded PETSc 3.6.3')

def extract_gcc():
    print('Extracting gcc 5.3.0')
    try:
        gcc_tar = tarfile.open('gcc-5.3.0.tar.bz2')
    except:
        print('gcc tar file does not exist')
        exit()
    gcc_tar.extractall()
    gcc_tar.close()
    print('Extracted gcc 5.3.0')


def extract_openmpi():
    print('Extracting openmpi 1.10.2')
    try:
        openmpi_tar = tarfile.open('openmpi-1.10.2.tar.gz')
    except:
        print('openmpi tar file does not exist')
        exit()
    openmpi_tar.extractall()
    openmpi_tar.close()
    print('Extracted openmpi 1.10.2')


def extract_trilinos():
    print('Extracting Trilinos 12.4.2')
    try:
        trilinos_tar = tarfile.open('trilinos-12.4.2.tar.bz2')
    except:
        print('Trilinos tar file does not exist')
        exit()
    trilinos_tar.extractall()
    trilinos_tar.close()
    print('Extracted Trilinos 12.4.2')


def extract_boost():
    print('Extracting Boost 1.60.0')
    try:
        trilinos_tar = tarfile.open('boost_1_60_0.tar.bz2')
    except:
        print('Boost tar file does not exist')
        exit()
    trilinos_tar.extractall()
    trilinos_tar.close()
    print('Extracted Boost 1.60.0')


def extract_lapack():
    print('Extracting LAPACK 3.6.0')
    try:
        trilinos_tar = tarfile.open('lapack-3.6.0.tgz')
    except:
        print('LAPACK tar file does not exist')
        exit()
    trilinos_tar.extractall()
    trilinos_tar.close()
    print('Extracted LAPACK 3.6.0')


def extract_petsc():
    print('Extracting PETSc 3.6.3')
    try:
        trilinos_tar = tarfile.open('petsc-3.6.3.tar.gz')
    except:
        print('PETSc tar file does not exist')
        exit()
    trilinos_tar.extractall()
    trilinos_tar.close()
    print('Extracted PETSc 3.6.3')


# Install functions
def install_gcc():
    print('Downloading pre-requisite packages')
    try:
        os.chdir('gcc-5.3.0')
    except:
        print('You have not extracted gcc, or it exists in a different ' +
              'directory than gcc-5.3.0')
        exit()
    subprocess.call('./contrib/download_prerequisites')
    os.chdir('..')
    print('Downloaded pre-requisite packages')
    # Creating install directory
    print('Configuring gcc')
    try:
        os.mkdir('gcc-install')
    except:
        pass
    try:
        os.mkdir('gcc-build')
    except:
        pass
    os.chdir('gcc-build')
    gcc_config = ('../gcc-5.3.0/configure'
                  ' --enable-shared'
                  ' --enable-threads=posix'
                  ' --enable-languages=c,c++,fortran'
                  ' --disable-multilib'
                  ' --prefix=' + os.path.abspath('../gcc-install'))
    subprocess.call(gcc_config.split(), stdout=subprocess.PIPE)
    print('gcc has been configured')
    subprocess.call('make -j' + str(cpuCount), shell=True)
    print('gcc has been made')
    subprocess.call('make install', shell=True)
    print('gcc has been installed')
    os.chdir('..')


def install_openmpi():
    try:
        os.mkdir('openmpi-install')
    except:
        pass
    try:
        os.chdir('openmpi-1.10.2')
    except:
        print('openmpi has either not been extracted or the source files' +
              ' are not located in openmpi-1.10.2')
        exit()
    gcc_path = os.path.abspath('../gcc-install')
    install_cmd = ('./configure' +
                   ' CC=' + gcc_path + '/bin/gcc' +
                   ' CXX=' + gcc_path + '/bin/g++' +
                   ' FC=' + gcc_path + '/bin/gfortran' +
                   ' LDFLAGS=-Wl,-rpath,'+ gcc_path + '/lib64' +
                   ' --prefix=' + os.path.abspath('../openmpi-install'))
    subprocess.call(install_cmd, shell=True)
    print('openmpi configured')
    subprocess.call('make -j' + str(cpuCount), shell=True)
    print('openmpi made')
    subprocess.call('make install', shell=True)
    print('openmpi installed')
    os.chdir('..')


def install_lapack():
    gcc_dir = os.path.abspath('./gcc-install/bin')
    try:
        os.chdir('lapack-3.6.0')
    except:
        print('LAPACK has either not been extracted or the files are not' +
              ' located in the lapack-3.6.0 directory')
    try:
        shutil.copy('../extra_files/make.inc', 'make.inc')
        shutil.copy('../extra_files/Makefile', 'Makefile')
    except:
        print('LAPACKs make.inc and/or Makefile could not be found or ' +
              'copied into the LAPACK build directory')
        exit()
    # Adds gcc directory to LAPACK's dumb make.inc file
    with open('make.inc', 'r+') as f:
        first_line = f.readline()
        lines = f.readlines()
        f.seek(0)
        f.write('GCC_DIR=' + gcc_dir + '\n')
        f.write(first_line)
        f.writelines(lines)
    subprocess.call('make clean', shell=True)
    subprocess.call('make all -j12', shell=True)
    subprocess.call('make all -j12', shell=True)
    print('LAPACK has been made\n')
    os.chdir('..')


def install_boost():
    # Create user-config.jam
    with open('./extra_files/user-config.jam', 'w') as boost_file:
        boost_file.write('using gcc : 5.3.0 : ' + os.path.abspath('./gcc-install/bin/gcc ;'))
    try:
        home = os.path.expanduser('~')
        print home
        shutil.copy('./extra_files/user-config.jam', home);
    except:
        print('Cannot copy user-config.jam to $HOME')
    try:
        os.mkdir('boost-install')
    except:
        pass
    try:
        os.chdir('boost_1_60_0')
    except:
        print('Boost has either not been extracted or the files are not in ' +
              'the boost_1_60_0 directory')
        exit()
    subprocess.call(['./bootstrap.sh'], shell=True)
    print('Boost bootstrapping complete\n')
    subprocess.call(
        ['./b2', 'install', '--prefix=' + os.path.abspath('../boost-install')])
    print('Boost has been installed\n')
    os.chdir('..')


def install_trilinos():
    gcc_dir = os.path.abspath('./gcc-install')
    openmpi_dir = os.path.abspath('./openmpi-install')
    lapack_dir = os.path.abspath('./lapack-3.6.0')
    boost_dir = os.path.abspath('./boost-install')
    try:
        os.mkdir('trilinos-build')
    except:
        pass
    try:
        os.mkdir('trilinos-install')
    except:
        pass
    shutil.copy('extra_files/do-configure', 'trilinos-build/')
    os.chdir('trilinos-build')
    # Adding unique absolute paths to Trilinos' do-configure script
    with open('do-configure', 'r+') as f:
        first_line = f.readline()
        lines = f.readlines()
        f.seek(0)
        f.write(first_line + '\n')
        f.write('GCC=' + gcc_dir + '\n')
        f.write('OPENMPI=' + openmpi_dir + '\n')
        f.write('LAPACK=' + lapack_dir + '\n')
        f.write('BOOST=' + boost_dir + '\n')
        f.writelines(lines)
    subprocess.call('./do-configure', shell=True)
    subprocess.call('make all -j12', shell=True)
    subprocess.call('make install', shell=True)


def install_petsc():
    gcc_dir = os.path.abspath('./gcc-install')        
    openmpi_dir = os.path.abspath('./openmpi-install')
    lapack_dir = os.path.abspath('./lapack-3.6.0')    
    boost_dir = os.path.abspath('./boost-install')    
    try:
        os.mkdir('petsc-install')
    except:
        pass
    try:
        os.chdir('./petsc-3.6.3')
    except:
        print('petsc-3.6.3 does not exist')
        exit()
    install_cmd = ('./configure' +
                   ' --with-mpi-dir=' + openmpi_dir +
                   ' --with-lapack-lib=' + lapack_dir + '/liblapack.a' +
                   ' --with-blas-lib=' + lapack_dir + '/librefblas.a' +
                   ' --prefix=' + os.path.abspath('../petsc-install') +
                   ' --with-shared-libraries=0' +
                   ' --with-debugging=0' +
                   ' COPTFLAGS="-O3"' +
                   ' FOPTFLAGS="-O3"'
                  )
    subprocess.call(install_cmd, shell=True)
    print('Navigate to petsc-3.6.3/ and run the above commands to finish the installation process\n')

if __name__ == '__main__':
    download_choices = []
    extract_choices = []
    install_choices = []
    LIBDIR = os.path.abspath('./gcc-install/lib64')
    GCC_PATH = os.path.abspath('./gcc-install/bin')
    MPI_PATH = os.path.abspath('./openmpi-install/bin')
    if 'LD_LIBRARY_PATH' in os.environ:
        os.environ['LD_LIBRARY_PATH'] = os.environ['LD_LIBRARY_PATH'] + ':' + LIBDIR
    else:
        os.environ['LD_LIBRARY_PATH'] = LIBDIR
    if 'PATH' in os.environ:
        os.environ['PATH'] = GCC_PATH + ':' + MPI_PATH + ':' + os.environ['PATH'] 
    else:
        os.environ['PATH'] = GCC_PATH + ':' + MPI_PATH

    newpid = os.fork()
    if newpid is 0:
        options = ['gcc', 'openmpi', 'LAPACK', 'Boost', 'Trilinos', 'PETSc']
        #  Downloading
        download = raw_input('Want to download things?: ')
        if download == 'y':
            for i in range(len(options)):
                download_choices.append(raw_input('Want to download ' + options[i]  + '?: '))

        # Extraction
        extract = raw_input('Want to extract things?: ')
        if extract == 'y':
            for i in range(len(options)):
                extract_choices.append(raw_input('Want to extract ' + options[i]  + '?: '))

        # Installation
        install = raw_input('Want to install things?: ')
        if install == 'y':
            for i in range(len(options)):
                install_choices.append(raw_input('Want to install ' + options[i]  + '?: '))

        if download == 'y':
            if download_choices[0] == 'y':
                download_gcc()
            if download_choices[1] == 'y':
                download_openmpi()
            if download_choices[2] == 'y':
                download_lapack()
            if download_choices[3] == 'y':
                download_boost()
            if download_choices[4] == 'y':
                download_trilinos()
            if download_choices[5] == 'y':
                download_petsc()

        if extract == 'y':
            if extract_choices[0] == 'y':
                extract_gcc()
            if extract_choices[1] == 'y':
                extract_openmpi()
            if extract_choices[2] == 'y':
                extract_lapack()
            if extract_choices[3] == 'y':
                extract_boost()
            if extract_choices[4] == 'y':
                extract_trilinos()
            if extract_choices[5] == 'y':
                extract_petsc()

        if install == 'y':
            if install_choices[0] == 'y':
                install_gcc()
            if install_choices[1] == 'y':
                install_openmpi()
            if install_choices[2] == 'y':
                install_lapack()
            if install_choices[3] == 'y':
                install_boost()
            if install_choices[4] == 'y':
                install_trilinos()
            if install_choices[5] == 'y':
                install_petsc()
    else:
        os.waitpid(newpid, 0)
