import setuptools.config
from setuptools import setup, find_packages

setup(
    name="pythonbootcamp",
    version='0.0.2',
    packages=find_packages('./src/'),
    package_dir={
        'pythonbootcamp': 'src/pythonbootcamp/',
        'pythonbootcamp.day032': 'src/pythonbootcamp/day032/'
    },
    package_data={'pythonbootcamp.day032': ['data/*.txt']},

    author='Jakub Bagiński',
    author_email='jakub.baginski@gmail.com',
    url='https://github.com/jakubbaginski/pythonbootcamp',
    license=''
)

print(f'Packages found: {find_packages("./src/")}')

