from setuptools import find_packages
from setuptools import setup

setup(
    name='amr_msgs',
    version='0.1.0',
    packages=find_packages(
        include=('amr_msgs', 'amr_msgs.*')),
)
