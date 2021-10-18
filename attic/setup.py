import pathlib
from setuptools import find_packages, setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="publicinterest",
    version="1.0.0",
    description="Read the latest Real Python tutorials",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/marinabeshai/publicinterest",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=["pandas", "plotly", "datetime", "csv", "matplotlib",
                      'pikepdf', "slate3k", "os", "urllib", "xml.etree.ElementTree"],
    entry_points={
        "console_scripts": [
            "realpython=publicinterest.__main__:main",
        ]
    },
)
