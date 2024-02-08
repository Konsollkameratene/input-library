from setuptools import setup


def read_requirements(file):
    with open(file) as f:
        return f.read().splitlines()


def read_file(file):
    with open(file) as f:
        return f.read()


long_description = read_file("README.md")
requirements = read_requirements("requirements.txt")

setup(
    name='kontroller_input',
    version="1.0",
    author='Konsollkameratene',
    author_email='sverreabo@gmail.com',
    description='Input fra kontrollere',
    long_description=long_description,
    license="MIT",
    url="https://github.com/Konsollkameratene/input-library",
    packages=['kontroller_input'],
    install_requires=requirements,
)
