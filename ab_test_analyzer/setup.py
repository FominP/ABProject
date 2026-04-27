from setuptools import setup, find_packages

setup(
    name="ab_test_analyzer",
    version="0.1.3",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.21.0",
        "scipy>=1.7.0",
    ],
    description="Библиотека для статистического анализа A/B-тестов",
    long_description="Библиотека для A/B-тестов: z-тест, t-тест, хи-квадрат, SRM, MDE",
    long_description_content_type="text/markdown",
    author="Pavel Fomin",
    author_email="fominpavel243@gmail.com",
    url="https://github.com/FominP/ABProject",
    python_requires=">=3.8",
)