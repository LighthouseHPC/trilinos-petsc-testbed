#!/usr/bin/python
import urllib
import os.path

if os.path.isfile('gcc-5.3.0.tar.bz2'): 
	print('gcc 5.3.0 already exists...skipping')
else:		
	print('Downloading gcc 5.3.0')
	gcc = urllib.urlretrieve('ftp://gnu.mirrorcatalogs.com/gnu/gcc/gcc-5.3.0/gcc-5.3.0.tar.bz2' , 'gcc-5.3.0.tar.bz2')
	print('Downloaded gcc 5.3.0')

