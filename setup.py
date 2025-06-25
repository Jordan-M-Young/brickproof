from setuptools import setup, find_packages
from brickproof.version import VERSION

DESCRIPTION = "brickproof"
LONG_DESCRIPTION = "a library for remote testing of databricks code"


# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="brickproof",
    version=VERSION,
    author="Jordan-M-Young",
    author_email="jordan.m.young0@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=["toml"],  # add any additional packages that
    # needs to be installed along with your package. Eg: 'caer'
    keywords=["python3", "databricks", "unit test", "test", "cidd"],
    classifiers=["Programming Language :: Python :: 3", "Framework :: Pytest"],
)
