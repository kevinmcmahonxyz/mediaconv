from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mediaconv",
    version="0.1.0",
    author="Kevin McMahon",
    description="Convert modern media formats to universal formats",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kevinmcmahonxyz/mediaconv",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Graphics :: Graphics Conversion",
        "Topic :: Multimedia :: Sound/Audio :: Conversion",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.10",
    install_requires=[
        "click>=8.1.0",
        "pillow>=10.0.0",
        "pillow-avif-plugin>=1.4.0",
        "cairosvg>=2.7.0",
        "pydub>=0.25.1",
    ],
    entry_points={
        "console_scripts": [
            "mediaconv=mediaconv.cli:cli",
        ],
    },
)