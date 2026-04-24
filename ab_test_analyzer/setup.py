from setuptools import setup, find_packages

setup(
    name="ab_test_analyzer",
    version="0.1.0",
    author="Pavel Fomin",
    author_email="fominpavel243@gmail.com",
    description="Библиотека для статистического анализа A/B-тестов",
    long_description="",
    long_description_content_type="text/markdown",
    url="https://github.com/FominP/ABProject",
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
    ],
    extras_require={
        "dev": ["pytest>=7.0", "flask>=2.0"],
    },
)