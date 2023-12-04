from setuptools import setup, find_namespace_packages

setup(
    name='contactbook',
    version='1.0.0',
    description='contactbook + notebook + filesort + calculator',
    url='https://github.com/VadimTrubay/contactbook',
    author='TrubayVadim',
    author_email='vadnetvadnet@ukr.net',
    license='MIT',
    include_package_data=True,
    packages=find_namespace_packages(),
    install_requires=['colorama', 'numexpr'],
    entry_points={'console_scripts': ['contactbook=contactbook.main:main']}
)