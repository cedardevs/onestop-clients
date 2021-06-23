import setuptools

setuptools.setup(
    name="onestop-python-client-cedardevs",
    version="0.2.5",
    author="CEDARDEVS",
    author_email="cedar.cires@colorado.edu",
    description="A python package for processing messages from the NOAA OneStop event stream (aka Inventory Manager).",
    long_description="This package provides subject matter experts an API to interact with OneStop via kafka, cloud, and REST.",
    long_description_content_type="text/markdown",
    url="https://github.com/cedardevs/onestop-clients",
    packages=setuptools.find_packages(exclude=("tests",)),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
