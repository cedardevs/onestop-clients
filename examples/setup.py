import setuptools

# with open("README.md", "r") as fh:
#     long_description = fh.read()

setuptools.setup(
    name="examples",
    version="1.0.0",
    author="",
    author_email="cedar.cires@colorado.edu",
    description="A python package for processing messages from the NOAA OneStop event stream (aka Inventory Manager).",
    long_description="This package provides subject matter experts an API to interact with the kafka topics backing OneStop.",
    long_description_content_type="text/markdown",
    url="https://github.com/cedardevs/onestop-clients",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
