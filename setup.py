from setuptools import setup, find_packages

setup(
    name="pythonbootcamp",
    version='0.0.3',
    long_description='Python Pro Bootcamp 2021 from Udemy',
    packages=find_packages('./src/'),
    package_dir={'': 'src'},
    package_data={'pythonbootcamp.day032': ['data/*.txt']},
    exclude_package_data={'pythonbootcamp.day032': ['*secret*']},
    author='Jakub Bagiński',
    author_email='jakub.baginski@gmail.com',
    url='https://github.com/jakubbaginski/pythonbootcamp',
    license='GPU',
    license_files=['LICENSE']
)

print(f'Packages found: {find_packages("./src/")}')

