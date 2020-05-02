from setuptools import setup, find_namespace_packages, find_packages

setup(
    name="katie",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=["beautifulsoup4", "requests"],
    extras_require={"dev": ["black", "pytest"]},
    entry_points={
        "console_scripts": ["kt = katie._cli:main", "katie = katie._cli:main"]
    },
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
    ],
    version="0.0.0",
)
