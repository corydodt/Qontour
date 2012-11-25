from setuptools import setup

from qontour import version, name

setup(
        name=name,
        author="Cory Dodt",
        version=version.string,
        install_requires=["distribute", "klein"],
        packages=["qontour"],
        )
