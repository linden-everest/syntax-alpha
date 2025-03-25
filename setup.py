from setuptools import setup, find_packages

# 正确读取 README.md，指定 utf-8 编码
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="syntax-alpha",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.21.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0",
            "mypy>=0.950",
        ],
    },
    author="Linden",
    author_email="linden.everest@gmail.com",
    description="A flexible factor expression engine for numerical computations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/linden.everest/syntax-alpha",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
