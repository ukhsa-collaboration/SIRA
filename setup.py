from setuptools import setup
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

## Get the long description from the README file ##
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description_file = f.read()

## Get the license from the LICENSE file ##
with open('LICENCE.txt') as f:
    license = f.read()
    
requires = [
            'numpy>=1.18.1',
            'scipy>=1.4.1'
            ]

package_data={
   }
  
setup(
    name='sira',
    description='Package containing model which simulates and quantify the \
                 risk of importation for varying diseases, travel times and \
                 exposure mechanisms',
    version='1.1.0',
    long_description=long_description_file,
    author='Declan Bays',
    author_email='declan.bays@phe.gov.uk',
    url='https://gitlab.phe.gov.uk/Declan.Bays/SIRA',
    license=license,
    packages=['sira'],
    install_requires=requires,
    package_data = package_data,
    entry_points={
        'console_scripts': [
            'sira=sira:border_screening',
        ],
    },
)