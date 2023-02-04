from setuptools import setup, find_packages


def get_readme():
    with open("README.md") as f:
        return f.read()


setup(
    long_description=get_readme(),
    packages=find_packages(),
)
