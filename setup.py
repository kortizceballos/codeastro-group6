from setuptools import setup, find_packages

# stolen from orbitize, which stole from radvel
def get_requires():
    reqs = []
    for line in open('requirements.txt', 'r').readlines():
        reqs.append(line)
    return reqs

setup(
    name="pyhips",
    version="0.3",
    packages=find_packages(),
    license="BSD",
    install_requires=get_requires(),
    description='PyHiPS: a simple interface to the CDS hips2fits service.',
)
