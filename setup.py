from setuptools import setup, find_packages

setup(
    name="fuzzbench",
    version="0.1.0",
    description="Fast fuzzy string matching benchmarks",
    package_dir={"": "src"},
    packages=find_packages("src"),
    python_requires=">=3.8",
    install_requires=[
        "pytest==8.3.4",
        "rapidfuzz==3.14.0",
        "psutil==5.9.8",
    ],
)
