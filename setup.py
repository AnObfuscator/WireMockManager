#!/usr/bin/env python
import setuptools

with open('README.md', 'rb') as r_file:
    LDINFO = r_file.read()

# TODO remove pip install dependency on mock
required = [
    "psutil",
    "argh",
    "tabulate",
    "mock",
    "pyyaml"
]

dependency_links = [
]

# TODO remove tests from pip installed files
setuptools.setup(
    name="WireMock Manager",
    version="2.11.0.dev-1",
    author="AnObfuscator",
    author_email="anobfuscator@gmail.com",
    description="A tool for managing WireMock instances and files.",
    long_description=LDINFO,
    packages=setuptools.find_packages(),
    # package_dir={'':'wiremockmanager'},
    # packages=setuptools.find_packages("wiremockmanager", exclude=["test"]),
    url="https://github.com/AnObfuscator/WireMockManager",
    dependency_links=dependency_links,
    install_requires=required,
    classifiers=[
        'Intended Audience :: Information Technology',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Topic :: Utilities',
        'Topic :: Software Development :: Libraries :: Python Modules'],
    entry_points={
        "console_scripts": ["wmm = wiremockmanager.wmm:main"]}
)