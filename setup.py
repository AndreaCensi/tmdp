import os
from setuptools import setup, find_packages

version = "0.1"

description = ('') 
long_description = ('') 
 

setup(name='tmdp',
      author="Andrea Censi",
      author_email="censi@mit.edu",
      url='http://andreacensi.github.com/tmdp/',

      description=description,
      long_description=long_description,
      keywords="",
      license="LGPL",

      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Topic :: Software Development :: Quality Assurance',
        'Topic :: Software Development :: Documentation',
        'Topic :: Software Development :: Testing'
      ],

    version=version,
      download_url='http://github.com/AndreaCensi/tmdp/tarball/%s' % version,

      package_dir={'':'src'},
      packages=find_packages('src'),
      install_requires=['PyContracts'],
      tests_require=['nose'],

      entry_points={
        'console_scripts': [
            'gridworld_test_display = gridworld:gridworld_test_display',
            'tmdp = tmdp.programs:tmpd_main'
       ]
      },
)

