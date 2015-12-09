#!/usr/bin/python
import urllib
import os.path
import tarfile

if os.path.isfile('gcc-5.3.0.tar.bz2'): 
	print('gcc 5.3.0 tarball already exists...skipping download')
else:		
	print('Downloading gcc 5.3.0')
	gcc = urllib.urlretrieve('ftp://gnu.mirrorcatalogs.com/gnu/gcc/gcc-5.3.0/gcc-5.3.0.tar.bz2' , 'gcc-5.3.0.tar.bz2')
	print('Downloaded gcc 5.3.0')

if os.path.isfile('trilinos-12.4.2.tar.bz2'):
	print('Trilinos 12.4.2 already exists...skipping download') 
else:
	print('Downloading Trilinos 12.4.2')
	trilinos = urllib.urlretrieve('http://trilinos.csbsju.edu/download/files/trilinos-12.4.2-Source.tar.bz2', 'trilinos-12.4.2.tar.bz2')
	print('Downloaded Trilinos 12.4.2')

install = raw_input('Would you like to untar the downloaded files? This might take a while')
if install == 'y' or install == 'Y' or install == 'yes' or install == 'YES':
	if os.path.isdir('gcc-5.3.0'):
		print('gcc 5.3.0 is already installed locally')
	else:
		print('Extracting gcc 5.3.0')
		gcc_tar = tarfile.open('gcc-5.3.0.tar.bz2')
		gcc_tar.extractall()
		gcc_tar.close()
		print('Extracted gcc 5.3.0')
	
	if os.path.isdir('trilinos-12.4.2-Source'):
		print('Trilinos is already installed locally')
	else:
		print('Extracting Trilinos 12.4.2')
		trilinos_tar = tarfile.open('trilinos-12.4.2.tar.bz2')
		trilinos_tar.extractall()
		trilinos_tar.close()
		print('Extracted Trilinos 12.4.2')

