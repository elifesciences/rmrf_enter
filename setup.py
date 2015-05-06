from setuptools import setup

from rmrf_enter import rmrf_enter

with open('README.md') as fp:
    readme = fp.read()

with open('gpl.txt') as fp:
    license = fp.read()

with open('requirements.txt') as f:
    install_requires = f.read().splitlines()

setup(name='rmrf_enter',
    version=rmrf_enter.__version__,
    description=rmrf_enter.__description__,
    long_description=readme,
    packages=['rmrf_enter'],
    license = license,
    install_requires=install_requires
)
