from setuptools import setup, find_namespace_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='contactbook',
    version='1.1.4',
    description='contactbook + notebook + filesort + calculator',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/VadimTrubay/contactbook',
    author='TrubayVadim',
    author_email='vadnetvadnet@ukr.net',
    license='MIT',
    include_package_data=True,
    packages=find_namespace_packages(),
    install_requires=['colorama', 'numexpr'],
    entry_points={'console_scripts': ['contactbook=contactbook.main:main']}
)