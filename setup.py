from setuptools import setup, find_packages

setup(
    name="hotel_reservation",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "pytest>=7.4.0",
        "pytest-cov>=4.1.0",
    ],
    entry_points={
        'console_scripts': [
            'myapp=src.cli:main',
        ],
    },
    author="Aleksandar Filic",
    author_email="alex.tech93@outlook.com",
    description="A hotel room availability checking system",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/moontech69/hotel-reservation-system",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
