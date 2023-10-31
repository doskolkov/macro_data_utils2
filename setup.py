# Import required functions
from setuptools import setup, find_packages

# Call setup function
setup(
    author="QNX",
    description="ModelManager package: work with excel, sql and models",
    name="ModelManager",
    packages=find_packages(
        include=[
            "ModelManager",
            "ModelManager.*",
        ]
    ),
    version="0.1.0",
    install_requires=[
        'pandas>=1.2.1',
        #'sqlite'
    ],
)
