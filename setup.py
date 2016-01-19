#!/usr/bin/python
import subprocess
import urllib
import os
import tarfile
import shutil

download_progress = 0
percentage = 0

def dlProgress(block_no, block_size, file_size):
	total = file_size/block_size
	global percentage
	if (int(100*float(block_no)/float(total)) == percentage):
		print("Percentage complete: %i" % (percentage))
		percentage += 10

###  Download functions
def download_gcc():
	global percentage
	percentage = 0
	print('Downloading gcc 5.3.0')
	urllib.urlretrieve('ftp://ftp.gnu.org/gnu/gcc/gcc-5.3.0/gcc-5.3.0.tar.bz2', 'gcc-5.3.0.tar.bz2', reporthook=dlProgress)
	print('Downloaded gcc 5.3.0')

def download_mvapich2():
	global percentage
	percentage = 0
	print('Downloading mvapich2 2.2b')
	urllib.urlretrieve('http://mvapich.cse.ohio-state.edu/download/mvapich/mv2/mvapich2-2.2b.tar.gz', 'mvapich2-2.2b.tar.gz', reporthook=dlProgress)
	print('Downloaded mvapich2 2.2b')

def download_lapack():
	global percentage
	percentage = 0
	print('Downloading LAPACK 3.6.0')
	urllib.urlretrieve('http://www.netlib.org/lapack/lapack-3.6.0.tgz', 'lapack-3.6.0.tgz', reporthook=dlProgress)
	print('Downloaded LAPACK 3.6.0')

def download_boost():
	global percentage
	percentage = 0
	print('Downloading Boost 1.60.0')
	urllib.urlretrieve('http://sourceforge.net/projects/boost/files/boost/1.60.0/boost_1_60_0.tar.bz2/download', 'boost_1_60_0.tar.bz2', reporthook=dlProgress)
	print('Downloaded Boost 1.60.0')

def download_trilinos():
	global percentage
	percentage = 0
	print('Downloading Trilinos 12.4.2')
	urllib.urlretrieve('http://trilinos.csbsju.edu/download/files/trilinos-12.4.2-Source.tar.bz2', 'trilinos-12.4.2.tar.bz2', reporthook=dlProgress)
	print('Downloaded Trilinos 12.4.2')

###  Extraction functions
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

### Install functions
def install_gcc():
	print('Downloading pre-requisite packages')
	os.chdir('gcc-5.3.0')                     
	subprocess.check_call('./contrib/download_prerequisites')                                
	os.chdir('..')                                                                      
	print('Downloaded pre-requisite packages')                                          
	# Creating install directory                                                        
	print('Configuring gcc')                                                            
	os.mkdir('gcc-install')                                                             
	os.mkdir('gcc-build')                                                               
	os.chdir('gcc-build')                                                               
	gcc_config = ('../gcc-5.3.0/configure'                                              
		' --enable-shared'                                                              
		' --enable-threads=posix'                                                       
		' --enable-languages=c,c++,fortran'
		' --disable-multilib'                                                         
		' --prefix=' + os.path.abspath('../gcc-install')                                
		)                                                                               
	print(gcc_config)                                                                   
	process = subprocess.check_call(gcc_config.split(), stdout=subprocess.PIPE)              
	print('gcc has been configured')                                                    
	os.chdir('gcc-build')
	process = subprocess.check_call("make -j24", shell=True)
	print('gcc has been made')                                              
	process = subprocess.check_call("make install", shell=True)
	print('gcc has been installed')                                          
	os.chdir('..')

def install_mvapich2():
	os.mkdir('mvapich2-install')
	os.chdir('mvapich2-2.2b')
	gcc_path = os.path.abspath('../gcc-install/bin')
	install_cmd = ('./configure'
		' CC=' + gcc_path + '/gcc'
		' CXX=' + gcc_path + '/g++'
		' FC=' + gcc_path + '/gfortran'
		' --prefix=' + os.path.abspath('../mvapich2-install')
	)
	subprocess.check_call(install_cmd, shell=True)
	print("mvapich2 configured")
	subprocess.check_call("make -j24", shell=True)
	print("mvapich2 made")
	subprocess.check_call("make install", shell=True)
	print("mvapich2 installed")
	os.chdir('..')

def install_lapack():
	answer = raw_input("Have you added gcc-install/lib64 to the library path?")
	if answer == 'y' or answer == 'Y':
		gcc_dir = os.path.abspath('gcc-install/bin')
		with open("make.inc", "r+") as f:
			first_line = f.readline()
			lines = f.readlines()
			f.seek(0)
			f.write("GCC_DIR=" + gcc_dir + "\n")
			f.write(first_line)
			f.writelines(lines)
		shutil.copy("make.inc","lapack-3.6.0/make.inc")
		shutil.copy("Makefile","lapack-3.6.0/Makefile")
		os.chdir("lapack-3.6.0")
		subprocess.call("make all -j24", shell=True)
		subprocess.call("make all -j24", shell=True)
		print("LAPACK has been made\n")
		os.chdir("..")


### Main function
if __name__ == "__main__":

#  Downloading 
	download = raw_input('Want to download things?: ')
	if download == 'y' or download == 'Y':
		gcc_download = raw_input('Want to download gcc?: ')
		mvapich2_download = raw_input('Want to download mvapich2?: ')
		lapack_download = raw_input('Want to download LAPACK?: ')
		boost_download = raw_input('Want to download Boost?: ')
		trilinos_download = raw_input('Want to download Trilinos?: ')

#  Extraction
	extract = raw_input('Want to extract things?: ')
	if extract == 'y' or extract == 'Y':
		gcc_extract = raw_input('Want to extract gcc?: ')
		mvapich2_extract = raw_input('Want to extract mvapich2?: ')
		lapack_extract = raw_input('Want to extract LAPACK?: ')
		boost_extract = raw_input('Want to extract Boost?: ')
		trilinos_extract = raw_input('Want to extract Trilinos?: ')

#  Installation
	install = raw_input('Want to install things?: ')
	if install == 'y' or install == 'Y': 
		gcc_install = raw_input('Want to install gcc?: ')
		mvapich2_install = raw_input('Want to install mvapich2?: ')
		lapack_install = raw_input('Want to install LAPACK?: ')

	if download == 'y' or download == 'Y':
		if gcc_download == 'y' or gcc_download == 'Y':
			download_gcc()	
		if mvapich2_download == 'y' or mvapich2_download == 'Y':
			download_mvapich2()
		if lapack_download == 'y' or lapack_download == 'Y':
			download_lapack()
		if boost_download == 'y' or boost_download == 'Y':
			download_boost()
		if trilinos_download == 'y' or trilinos_download == 'Y':
			download_trilinos()
	
	if extract == 'y' or extract == 'Y':
		if gcc_extract == 'y' or gcc_extract == 'Y':
			extract_gcc()	
		if mvapich2_extract == 'y' or mvapich2_extract == 'Y':
			extract_mvapich2()	
		if lapack_extract == 'y' or lapack_extract == 'Y':
			extract_lapack()	
		if boost_extract == 'y' or boost_extract == 'Y':
			extract_boost()	
		if trilinos_extract == 'y' or trilinos_extract == 'Y':
			extract_trilinos()

	if install == 'y' or install == 'Y':
		if gcc_install == 'y' or gcc_install == 'Y':
			install_gcc()
		if mvapich2_install == 'y' or mvapich2_install == 'Y':
			install_mvapich2()
		if lapack_install == 'y' or lapack_install == 'Y':
			install_lapack()
