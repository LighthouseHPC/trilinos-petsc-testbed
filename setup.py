#!/usr/bin/python
import subprocess
import urllib
import os
import tarfile

###  Download functions
def download_gcc():
	if os.path.isfile('gcc-5.3.0.tar.bz2'): 
		print('gcc 5.3.0 tarball already exists...skipping download')
	else:		
		print('Downloading gcc 5.3.0')
		gcc = urllib.urlretrieve('ftp://gnu.mirrorcatalogs.com/gnu/gcc/gcc-5.3.0/gcc-5.3.0.tar.bz2' , 'gcc-5.3.0.tar.bz2')
		print('Downloaded gcc 5.3.0')

def download_mvapich2():
	if os.path.isfile('mvapich2-2.2b.tar.gz'):
		print('mvapich2 2.2b tarball already exists...skipping download')
	else:
		print('Downloading mvapich2 2.2b')
		mvapich2 = urllib.urlretrieve('http://mvapich.cse.ohio-state.edu/download/mvapich/mv2/mvapich2-2.2b.tar.gz', 'mvapich2-2.2b.tar.gz')
		print('Downloaded mvapich2 2.2b')

def download_lapack():
	if os.path.isfile('lapack-3.6.0.tgz'):
		print('LAPACK 3.6.0 tarball already exists...skipping download')
	else:
		print('Downloading LAPACK 3.6.0')
		lapack = urllib.urlretrieve('http://www.netlib.org/lapack/lapack-3.6.0.tgz', 'lapack-3.6.0.tgz')
		print('Downloaded LAPACK 3.6.0')

def download_trilinos():
	if os.path.isfile('trilinos-12.4.2.tar.bz2'):
		print('Trilinos 12.4.2 already exists...skipping download') 
	else:
		print('Downloading Trilinos 12.4.2')
		trilinos = urllib.urlretrieve('http://trilinos.csbsju.edu/download/files/trilinos-12.4.2-Source.tar.bz2', 'trilinos-12.4.2.tar.bz2')
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

### Install functions
def install_gcc():
	print('Downloading pre-requisite packages')
	os.chdir('gcc-5.3.0')                     
	subprocess.Popen('./contrib/download_prerequisites')                                
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
			' --enable-languages=c,c++,fortran,java'                                        
			' --disable-multilib'                                                         
			' --prefix=' + os.path.abspath('../gcc-install')                                
			)                                                                               
	print(gcc_config)                                                                   
	process = subprocess.Popen(gcc_config.split(), stdout=subprocess.PIPE)              
	output = process.communicate()[0]                                                   
	print('gcc has been configured')                                                    
	gcc_make = 'make -j16'                                                              
	process = subprocess.Popen(gcc_make.split(), stdout=subprocess.PIPE)                
	output = process.communicate()[0]                                                   
	print('gcc has been made')                                                          
	gcc_install = 'make install'                                                        
	process = subprocess.Popen(gcc_install.split(), stdout=subprocess.PIPE)             
	output = process.communicate()[0]                                                   
	print('gcc has been installed')                                                     
	os.chdir('..')                                                                      

### Main function
if __name__ == "__main__":
	answer = raw_input('Want to download things?')
	if answer == 'y' or answer == 'Y':

		answer = raw_input('Want to download gcc?: ')
		if answer == 'y' or answer == 'Y':
			download_gcc()	
		answer = raw_input('Want to download mvapich2?: ')
		if answer == 'y' or answer == 'Y':
			download_mvapich2()
		answer = raw_input('Want to download Trilinos?: ')
		if answer == 'y' or answer == 'Y':
			download_trilinos()

	answer = raw_input('Want to extract things?')
	if answer == 'y' or answer == 'Y':

		answer = raw_input('Want to extract gcc?: ')
		if answer == 'y' or answer == 'Y':
			extract_gcc()	
		answer = raw_input('Want to extract mvapich2?: ')
		if answer == 'y' or answer == 'Y':
			extract_mvapich2()
		answer = raw_input('Want to extract Trilinos?: ')
		if answer == 'y' or answer == 'Y':
			extract_trilinos()

	answer = raw_input('Want to install things?')
	if answer == 'y' or answer == 'Y':
		answer = raw_input('Want to install gcc?: ')
		if answer == 'y' or answer == 'Y':
			install_gcc()

