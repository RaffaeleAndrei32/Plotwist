from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="plotwist",
    version="0.1.0",
    author="Raffaele",
    description="A web platform for movies logging, scoring and reviewing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/plotwist",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: Django :: 6.0",
        "Environment :: Web Environment",
        "Intended Audience :: End Users/Desktop",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "plotwist-manage=manage:main",
        ],
    },
)
