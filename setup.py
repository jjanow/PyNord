#!/usr/bin/env python3
"""
Setup script for PyNord - NordVPN Management Application
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="pynord",
    version="1.0.0",
    author="PyNord Team",
    author_email="pynord@example.com",
    description="A desktop application for managing NordVPN on Kubuntu/Linux",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/pynord",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Internet :: Proxy Servers",
        "Topic :: System :: Networking",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    entry_points={
        "console_scripts": [
            "pynord=main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt"],
    },
    keywords="vpn nordvpn desktop gui kubuntu linux",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/pynord/issues",
        "Source": "https://github.com/yourusername/pynord",
        "Documentation": "https://github.com/yourusername/pynord#readme",
    },
) 