import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="QClickEdit",
    version="1.0.0",
    author="Brendan Krueger",
    author_email="hyperdimensionalplants@gmail.com",
    description="Qt widget for text that becomes a Qt input widget when clicked on.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Hyperdimensionals/QClickEdit",
    packages=setuptools.find_packages(),
    license="MIT license",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3',
)
