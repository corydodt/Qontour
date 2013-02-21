from setuptools import setup

from qontour import version, NAME

setup(
        name=NAME,
        author="Cory Dodt",
        version=version.string,
        install_requires=[
            "distribute", 
            "klein", 
            "pillow", 
            "pymongo", 
            "twisted"],
        packages=["qontour"],
        )
