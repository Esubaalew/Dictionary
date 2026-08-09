from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="dictionary",
    version="0.1.2",
    author="Dictionary Package",
    description="A Python package for querying both the Britannica and Abyssinica dictionaries",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/Dictionary",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "beautifulsoup4>=4.12.3",
        "requests>=2.31.0",
        "bs4>=0.0.2",
    ],
)

