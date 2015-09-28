"""This is a module for PiPlus from SunFounder.

See:
https://www.sunfounder.com
"""

from setuptools import setup, find_packages
from codecs import open
from os import path
import os

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='PiPlus',
    version='1.0.0',
    description='PiPlus python module for Raspberry Pi',
    long_description=long_description,

    url='https://www.sunfounder.com',

    author='Cavon Lee',
    author_email='lijiarong@sunfounder.com',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',

        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',

        'Programming Language :: Python :: 2.7',
    ],

    keywords='Raspberry Pi',

    packages=find_packages(exclude=['example', 'docs', 'tests*']),

    install_requires=['RPi.GPIO'],
    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },

    package_data={
        'PiPlus': ['package_data.dat'],
    },
    data_files=[('data', ['data/data_file'])],

    entry_points={
        'console_scripts': [
            'PiPlus=PiPlus:main',
        ],
    },
)
	
monthname = {'01':'Jan', '02':'Feb', '03':'Mar', '04':'Apr', '05':'May', '06':'Jun',
			 '07':'Jul', '08':'Aug', '09':'Sep', '10':'Oct', '11':'Nov', '12':'Dec'}
monthfullname = {'01':'January', '02':'February', '03':'March', '04':'April', '05':'May', '06':'June',
				 '07':'July', '08':'August', '09':'September', '10':'October', '11':'November', '12':'December'}
os.system('echo ds1307 0x68 > /sys/class/i2c-adapter/i2c-1/new_device')
print '\nNow the DS1307 is:'
os.system('hwclock -r')
flag = 1
while flag == 1 :
	check = raw_input('Is it right? Do you need to set the clock? ')
	if check == 'y' or check == 'Y':
		flag = 0
	elif check == 'n' or check == 'N':
		print 'OK, we are done here. Install finished.'
		quit()
	else:
		print 'Sorry, you should type in "Y" or "y" for a yes, or "N" or "n", for a no, please Try again.'


print "\nBrillient! Let's set the date first!"
flag = 1
count = 0
while flag == 1:
	date = raw_input('\nType in year, month and date in types "YYYY/MM/DD:" ')
	year = date.split('/')[0]
	month = date.split('/')[1]
	dateofmonth = date.split('/')[2]
	print ''
	if int(month) in [1, 3, 5, 7, 8, 10, 12]:
		if 0 < int(dateofmonth) < 32:
			flag = 0
		else:
			print '%s has only 31 days. Made a mistake? Try again.' % monthfullname[month]
	elif int(month) in [4, 6, 9, 11]:
		if 0 < int(dateofmonth) < 31:
			flag = 0
		else:
			print '%s has only 30 days. Made a mistake? Try again.' % monthfullname[month]
	elif int(month) == 2:
		if int(year)%4 == 0:
			if 0 < int(dateofmonth) < 30:
				flag = 0
			else:
				print '%s in %s has only 29 days. Fabruary has less than 29 days even in a leap year! Made a mistake? Try again.' % (monthfullname[month], year)
		else:
			if 0 < int(dateofmonth) < 29:
				flag = 0
			elif int(dateofmonth) == 29: 
				print 'Year %s is a leap year, February has only 28 days. Made a mistake? Try again.' % year
			else:
				print "%s in %s has only 28 days. Even a leap year don't have that much days. Made a mistake? Try again." % (monthfullname[month], year)
	else:
		print 'How can it be month %s?! There are only 12 months in year %s. Maybe you made a mistake. Remenber, first year, then month, and finally date. and seprated by "/". Try again.' % (month, year)
	
	count += 1

if count > 3:
	print 'Finally, we did the date.you set the date to:'
	print monthname(month), dateofmonth
time = raw_input('set time to (e.g.: 14:59:23): ')

