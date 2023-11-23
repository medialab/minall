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
    packages=find_packages(exclude=["test"]),
    install_requires=["minet==1.1.8"],
    extra_require={
        ":python_version<'3.11'": ["typing_extensions>=4.3"],
    },
    entry_points={
        "console_scripts": ["minall=minall.cli.run:cli"],
    },
    zip_safe=True,
)
