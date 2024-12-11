from setuptools import setup, find_packages

VERSION = "0.0.1"
DESCRIPTION = "A ciphers package"
LONG_DESCRIPTION = "A package that makes it easy to play around with different ciphering and deciphering algorithms"

setup(
    name="ciphers",
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author="Norbert Acedański",
    author_email="norbert.acedanski@gmail.com",
    license="MIT",
    packages=find_packages(),
    install_requires=[],
    keywords="ciphers",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: tox",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13"
    ]
)
