import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lightify",
    version="0.0.1",
    author="Finn Harms",
    author_email="lightify@finn-harms.de",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/innif/Spotify-Beat-Detection",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: GNU GPL v3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)