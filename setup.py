from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()
    
with open('LICENSE') as f:
    license = f.read()


setup(
    name='CapivarIA',
    version='0.1.0',
    description='Gen AI powered newsletter',
    long_description=readme,
    license = license,
    url='https://github.com/vitornegromonte/newsletter'
)
