from setuptools import setup, find_packages

description = (
    'A Python package that gives you the power to extract '
    'any compressed file using the same simple syntax.')

setup(
    name='kai',
    version='0.0.5',
    description=description,
    long_description=description,
    author='Brian Bates',
    author_email='brian@eccentricprototypes.com',
    url='http://github.com/brian-bates/kai',
    install_requires=['rarfile'],
    packages=find_packages(),
    entry_points={'console_scripts': ['kai = kai.kai:main']}
)
