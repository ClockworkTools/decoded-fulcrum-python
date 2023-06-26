__author__ = 'Keith Hannon'
__datecreated__ = '10/07/2015'
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

#requires = ['requests>=2.1.0']
requires = ['fulcrum']

setup(
    name='decodedfulcrum',
    version='1.1.2',
    description='A python wrapper for the Fulcrum API',
    author='Keith Hannon',
    author_email='keith@clockwork.co.nz',
    url='https://github.com/ClockworkTools/decoded-fulcrum-python',
    packages= ['decodedFulcrum', 'decodedFulcrum.api'],
    install_requires=requires,
    license='Apache License',
)
