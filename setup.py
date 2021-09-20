from setuptools import setup, find_packages

setup(
    name="pythonbootcamp",
    version='0.0.3',
    long_description='Python Pro Bootcamp 2021 from Udemy',
    packages=find_packages('./src/'),
    package_dir={'': 'src'},
    package_data={'pythonbootcamp.day032': ['data/*.txt', 'data/letter_templates/letter*'],
                  'pythonbootcamp.day033': ['images/*.png'],
                  'pythonbootcamp.day034': ['images/*.png']},
    exclude_package_data={'pythonbootcamp.day032': ['*secret*']},
    author='Jakub Bagiński',
    author_email='jakub.baginski@gmail.com',
    url='https://github.com/jakubbaginski/pythonbootcamp',
    license='GPU',
    license_files=['LICENSE'],
    install_requires=[
        'panda',
        'setuptools'
        'requests',
        'ttkthemes',
        'Pillow',
        'future',
        'twilio'
    ],
    tests_require=[
        'pytest',
        'pytest-runner'
    ]

)

print(f'Packages found: {find_packages("./src/")}')
