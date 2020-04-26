
"""A setuptools based setup module.
See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
import setuptools
from setuptools import setup, find_packages
from os import path
# io.open is needed for projects that support Python 2.7
# It ensures open() defaults to text mode with universal newlines,
# and accepts an argument to specify the text encoding
# Python 3 only projects can skip this import
from io import open

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
setup(
name='BillingKivy',
version='1.0.0',
description='A sample Python project',
long_description=long_description,
long_description_content_type='text/x-rst',
url='https://github.com/pypa/sampleproject',
author='Nadeem',
author_email='nadeemsani786@gmail.com',
license='',
classifiers=[
    # How mature is this project? Common values are
    #   3 - Alpha
    #   4 - Beta
    #   5 - Production/Stable
    'Development Status :: 3 - Alpha',

    # Indicate who your project is intended for
    'Intended Audience :: Users',
    'Topic :: Software Development :: Build Tools',

    # Pick your license as you wish (should match "license" above)
     'License :: OSI Approved :: MIT License',

    # Specify the Python versions you support here. In particular, ensure
    # that you indicate whether you support Python 2, Python 3 or both.
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.2',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
],
keywords='POS billing',
project_urls={
    'Documentation': '',
    'Funding': '',
    'Say Thanks!': '',
    'Source': '',
    'Tracker': '',
},
package_dir={'': 'src'},
packages=setuptools.find_packages(),
py_modules=["six"],
install_requires=['peppercorn'],
python_requires='>=3',
package_data={
     "": ["*.txt"],
        # And include any *.dat files found in the "data" subdirectory
        # of the "mypkg" package, also:
        "mypkg": ["data/*.dat"],
},
include_package_data=True
)