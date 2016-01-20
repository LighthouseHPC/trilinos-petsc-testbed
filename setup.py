#!/usr/bin/env python
import subprocess
import urllib
import os
import tarfile
import shutil
import errno

download_progress = 0
percentage = 0


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


def download_mvapich2():
    global percentage
    percentage = 0
    print('Downloading mvapich2 2.2b')
    urllib.urlretrieve(
        'http://mvapich.cse.ohio-state.edu/download/mvapich/mv2/mvapich2-2.2b.tar.gz',
        'mvapich2-2.2b.tar.gz', reporthook=dl_progress)
    print('Downloaded mvapich2 2.2b')


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


def extract_gcc():
    print('Extracting gcc 5.3.0')
    gcc_tar = tarfile.open('gcc-5.3.0.tar.bz2')
    gcc_tar.extractall()
    gcc_tar.close()
    print('Extracted gcc 5.3.0')


def extract_mvapich2():
    print('Extracting mvapich2 2.2b')
    mvapich2_tar = tarfile.open('mvapich2-2.2b.tar.gz')
    mvapich2_tar.extractall()
    mvapich2_tar.close()
    print('Extracted mvapich2 2.2b')


def extract_trilinos():
    print('Extracting Trilinos 12.4.2')
    trilinos_tar = tarfile.open('trilinos-12.4.2.tar.bz2')
    trilinos_tar.extractall()
    trilinos_tar.close()
    print('Extracted Trilinos 12.4.2')


def extract_boost():
    print('Extracting Boost 1.60.0')
    trilinos_tar = tarfile.open('boost_1_60_0.tar.bz2')
    trilinos_tar.extractall()
    trilinos_tar.close()
    print('Extracted Boost 1.60.0')


def extract_lapack():
    print('Extracting LAPACK 3.6.0')
    trilinos_tar = tarfile.open('lapack-3.6.0.tgz')
    trilinos_tar.extractall()
    trilinos_tar.close()
    print('Extracted LAPACK 3.6.0')


# Install functions
def install_gcc():
    print('Downloading pre-requisite packages')
    try:
        os.chdir('gcc-5.3.0')
    except:
        print('You have not extracted gcc, or it exists in a different' +
              ' directory than gcc-5.3.0')
    exit()
    subprocess.check_call('./contrib/download_prerequisites')
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
    print(gcc_config)
    subprocess.check_call(gcc_config.split(), stdout=subprocess.PIPE)
    print('gcc has been configured')
    subprocess.check_call('make -j12', shell=True)
    print('gcc has been made')
    subprocess.check_call('make install', shell=True)
    print('gcc has been installed')
    os.chdir('..')


def install_mvapich2():
    try:
        os.mkdir('mvapich2-install')
    except:
        pass
    os.chdir('mvapich2-2.2b')
    gcc_path = os.path.abspath('../gcc-install/bin')
    install_cmd = ('./configure' +
                   ' CC=' + gcc_path + '/gcc' +
                   ' CXX=' + gcc_path + '/g++' +
                   ' FC=' + gcc_path + '/gfortran ' +
                   '../mvapich2-install')
    subprocess.check_call(install_cmd, shell=True)
    print('mvapich2 configured')
    subprocess.check_call('make -j12', shell=True)
    print('mvapich2 made')
    subprocess.check_call('make install', shell=True)
    print('mvapich2 installed')
    os.chdir('..')


def install_lapack():
    answer = raw_input(
        'Have you added gcc-install/lib64 to the library path?: ')
    if answer == 'y' or answer == 'Y':
        gcc_dir = os.path.abspath('./gcc-install/bin')
        shutil.copy('make.inc', 'lapack-3.6.0/make.inc')
        shutil.copy('Makefile', 'lapack-3.6.0/Makefile')
        os.chdir('lapack-3.6.0')
        with open('make.inc', 'r+') as f:
            first_line = f.readline()
            lines = f.readlines()
            f.seek(0)
            f.write('GCC_DIR=' + gcc_dir + '\n')
            f.write(first_line)
            f.writelines(lines)
        subprocess.call('make all -j12', shell=True)
        subprocess.call('make all -j12', shell=True)
        print('LAPACK has been made\n')
        os.chdir('..')


def install_boost():
    try:
        os.mkdir('boost-install')
    except:
        pass
    os.chdir('boost_1_60_0')
    subprocess.call(['./bootstrap.sh', '--with-toolset=gcc'], shell=True)
    print('Boost bootstrapping complete\n')
    subprocess.call(
        ['./b2', 'install', '--prefix=' + os.path.abspath('../boost-install')])
    print('Boost has been installed\n')
    os.chdir('..')


def install_trilinos():
    gcc_dir = os.path.abspath('./gcc-install')
    mvapich2_dir = os.path.abspath('./mvapich2-install')
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
    shutil.copy('./do-configure', 'trilinos-build/')
    os.chdir('trilinos-build')
    with open('do-configure', 'r+') as f:
        first_line = f.readline()
        lines = f.readlines()
        f.seek(0)
        f.write(first_line + '\n')
        f.write('GCC=' + gcc_dir + '\n')
        f.write('MVAPICH=' + mvapich2_dir + '\n')
        f.write('LAPACK=' + lapack_dir + '\n')
        f.write('BOOST=' + boost_dir + '\n')
        f.writelines(lines)
    subprocess.call('./do-configure', shell=True)
    subprocess.call('make all -j12', shell=True)
    subprocess.call('make install', shell=True)


if __name__ == '__main__':
    download_choices = ['n'] * 6
    extract_choices = ['n'] * 6
    install_choices = ['n'] * 6
    #  Downloading
    download_choices[0] = raw_input('Want to download things?: ')
    if download_choices[0] == 'y':
        download_choices[1] = raw_input('Want to download gcc?: ')
        download_choices[2] = raw_input('Want to download mvapich2?: ')
        download_choices[3] = raw_input('Want to download LAPACK?: ')
        download_choices[4] = raw_input('Want to download Boost?: ')
        download_choices[5] = raw_input('Want to download Trilinos?: ')

    # Extraction
    extract_choices[0] = raw_input('Want to extract things?: ')
    if extract_choices[0] == 'y':
        extract_choices[1] = raw_input('Want to extract gcc?: ')
        extract_choices[2] = raw_input('Want to extract mvapich2?: ')
        extract_choices[3] = raw_input('Want to extract LAPACK?: ')
        extract_choices[4] = raw_input('Want to extract Boost?: ')
        extract_choices[5] = raw_input('Want to extract Trilinos?: ')

    # Installation
    install_choices[0] = raw_input('Want to install things?: ')
    if install_choices[0] == 'y':
        install_choices[1] = raw_input('Want to install gcc?: ')
        install_choices[2] = raw_input('Want to install mvapich2?: ')
        install_choices[3] = raw_input('Want to install LAPACK?: ')
        install_choices[4] = raw_input('Want to install Boost?: ')
        install_choices[5] = raw_input('Want to install Trilinos?: ')

    if download_choices[0] == 'y':
        if download_choices[1] == 'y':
            download_gcc()
        if download_choices[2] == 'y':
            download_mvapich2()
        if download_choices[3] == 'y':
            download_lapack()
        if download_choices[4] == 'y':
            download_boost()
        if download_choices[5] == 'y':
            download_trilinos()

    if extract_choices[0] == 'y':
        if extract_choices[1] == 'y':
            extract_gcc()
        if extract_choices[2] == 'y':
            extract_mvapich2()
        if extract_choices[3] == 'y':
            extract_lapack()
        if extract_choices[4] == 'y':
            extract_boost()
        if extract_choices[5] == 'y':
            extract_trilinos()

    if install_choices[0] == 'y':
        if install_choices[1] == 'y':
            install_gcc()
        if install_choices[2] == 'y':
            install_mvapich2()
        if install_choices[3] == 'y':
            install_lapack()
        if install_choices[4] == 'y':
            install_boost()
        if install_choices[5] == 'y':
            install_trilinos()
