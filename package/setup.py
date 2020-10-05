from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name='avitech',
    description="Avitech learning package",
    version='0.1.5',
    author="Nechaev Artem",
    packages=find_packages(),
    long_description="Пакет для обучения Питону",
    python_requires='>=3.6',
    include_package_data=True
)
    #