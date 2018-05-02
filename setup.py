from setuptools import setup, find_packages
from io import open
import qtsass


setup(
    name=qtsass.__title__,
    version=qtsass.__version__,
    description=qtsass.__description__,
    long_description=open("README.md", "r", encoding="utf-8").read(),
    author=qtsass.__author__,
    author_email="N/A",
    url=qtsass.__url__,
    license="N/A",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "qtsass = qtsass.qtsass:main"
        ]
    },
    classifiers=(
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        "Topic :: Software Development :: Libraries :: Python Modules",
    ),
    install_requires=[
        'libsass',
        'watchdog'
    ]
)
