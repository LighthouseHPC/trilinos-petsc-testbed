#!/usr/bin/python
import subprocess
import urllib
import os
import tarfile

# Check for local tar files
## Check for gcc 5.3.0
if os.path.isfile('gcc-5.3.0.tar.bz2'): 
	print('gcc 5.3.0 tarball already exists...skipping download')
else:		
	print('Downloading gcc 5.3.0')
	gcc = urllib.urlretrieve('ftp://gnu.mirrorcatalogs.com/gnu/gcc/gcc-5.3.0/gcc-5.3.0.tar.bz2' , 'gcc-5.3.0.tar.bz2')
	print('Downloaded gcc 5.3.0')

## Check for Trilinos 12.4.2
if os.path.isfile('trilinos-12.4.2.tar.bz2'):
	print('Trilinos 12.4.2 already exists...skipping download') 
else:
	print('Downloading Trilinos 12.4.2')
	trilinos = urllib.urlretrieve('http://trilinos.csbsju.edu/download/files/trilinos-12.4.2-Source.tar.bz2', 'trilinos-12.4.2.tar.bz2')
	print('Downloaded Trilinos 12.4.2')

# Check for installed libraries
install = raw_input('Would you like to untar the downloaded files? This might take a while: ')
if install == 'y' or install == 'Y' or install == 'yes' or install == 'YES':
	# Install gcc if path DNE
	if os.path.isdir('gcc-5.3.0'):
		print('gcc 5.3.0 seems to be already installed locally')
	else:
		print('Extracting gcc 5.3.0')
		gcc_tar = tarfile.open('gcc-5.3.0.tar.bz2')
		gcc_tar.extractall()
		gcc_tar.close()
		print('Extracted gcc 5.3.0')
		print('Downloading pre-requisite packages')
		os.chdir('gcc-5.3.0')
		subprocess.Popen('./contrib/download_prerequisites')
		os.chdir('..')
		print('Downloaded pre-requisite packages')
	
	# Install Trilinos if path DNE
	if os.path.isdir('trilinos-12.4.2-Source'):
		print('Trilinos 12.4.2 seems to be already installed locally')
	else:
		print('Extracting Trilinos 12.4.2')
		trilinos_tar = tarfile.open('trilinos-12.4.2.tar.bz2')
		trilinos_tar.extractall()
		trilinos_tar.close()
		print('Extracted Trilinos 12.4.2')

