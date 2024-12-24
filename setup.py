from setuptools import setup, find_packages

setup(
    name="arl-cli",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        'requests>=2.25.1',
        'prettytable>=2.0.0',
        'colorama>=0.4.4',
        'pyyaml>=5.4.1',
    ],
    entry_points={
        'console_scripts': [
            'arl=arl.cli:main',
        ],
    },
) 