from setuptools import find_packages, setup

with open("./README.md", "r") as f:
    long_description = f.read()

meta_package = {}
with open("./minall/__version__.py") as f:
    exec(f.read(), meta_package)

setup(
    name="minall",
    version=meta_package["__version__"],
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://github.com/medialab/minall",
    author="Kelly Christensen",
    keywords="webmining",
    license="GPL-3.0",
    python_requires=">=3.11",
    packages=find_packages(exclude=["tests"]),
    install_requires=[
        "minet==1.4.0",
        "ural==1.3.0",
        "babel==2.14.0",
        "click==8.1.7",
        "colorama==0.4.6",
        "ghp-import==2.1.0",
        "griffe==0.38.1",
        "markdown==3.5.1",
        "mergedeep==1.3.4",
        "mkdocs==1.5.3",
        "mkdocs-autorefs==0.5.0",
        "mkdocs-material==9.5.3",
        "mkdocs-material-extensions==1.3.1",
        "mkdocstrings==0.24.0",
        "mkdocstrings-python==1.7.5",
        "packaging==23.2",
        "paginate==0.5.6",
        "pathspec==0.12.1",
        "platformdirs==4.1.0",
        "pymdown-extensions==10.7",
        "pyyaml-env-tag==0.1",
        "watchdog==3.0.0",
    ],
    extra_require={
        ":python_version<'3.11'": ["typing_extensions>=4.3"],
    },
    entry_points={
        "console_scripts": ["minall=minall.cli.run:cli"],
    },
    zip_safe=True,
)
