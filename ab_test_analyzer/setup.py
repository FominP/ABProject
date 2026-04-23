from setuptools import setup, find_packages

setup(
    name="ab_test_analyzer",                # имя для pip install
    version="0.1.0",
    author="Pavel Fomin",
    author_email="fominpavel243@gmail.com",
    description="Библиотека для анализа результатов A/B-тестов",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/FominP/ab_test_analyzer",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.21.0",
        "scipy>=1.7.0",
        "pandas>=1.3.0",
        "matplotlib>=3.4.0",
    ],
)