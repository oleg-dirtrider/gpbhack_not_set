import os
from importlib.util import spec_from_file_location

from pkg_resources import parse_requirements
from setuptools import setup, find_packages


module_name = 'rtdm_analyze'

module = spec_from_file_location(
    module_name, os.path.join('rtdm_analyze', '__init__.py')
).loader.load_module(module_name)


def load_requirements(file_name: str) -> list:
    requirements = []
    with open(file_name, 'r') as file:
        for req in parse_requirements(file.read()):
            requirements.append(f'{req.name}{req.specifier}')
    return requirements


setup(
    name=module_name,
    version=module.__version__,
    author=module.__author__,
    author_email=module.__email__,
    description=module.__doc__,
    long_description=open('README.md').read(),
    url='https://github.com/vasyanch/gpbhack_not_set',
    platforms='all',
    python_requires='>=3.9',
    packages=find_packages(),
    include_package_data=True,
    install_requires=load_requirements('requirements.txt'),
)
