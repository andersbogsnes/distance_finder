from setuptools import setup, find_packages

INSTALL_REQUIRES = [
    'googlemaps',
    'pandas',
    'sqlalchemy',
]

TEST_REQUIRES = [
    'pytest',
    'pytest-cov'
]

setup(
    name="distances",
    version="0.1.0",
    author="Anders Bogsnes",
    author_email="andersbogsnes@gmail.com",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=INSTALL_REQUIRES,
    tests_requires=TEST_REQUIRES,
    license='MIT',

)
