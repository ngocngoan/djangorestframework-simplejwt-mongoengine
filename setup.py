#!/usr/bin/env python
from pathlib import Path

from setuptools import find_packages, setup

requirements = [
    "django>=3.2,<4.3",
    "djangorestframework>=3.12",
    "django-mongoengine>=0.5.4",
    "pyjwt>=1.7.1,<3",
]

extras_require = {
    "test": [
        "cryptography",
        "coverage",
        "freezegun",
        "psutil",
        "python-jose",
        "pytest-cov",
        "pytest-django",
        "pytest-xdist",
        "pytest",
        "tox",
    ],
    "lint": [
        "flake8",
        "pep8",
        "isort",
    ],
    "doc": [
        "Sphinx>=7",
        "sphinx_rtd_theme>=2.0.0",
    ],
    "dev": [
        "pytest-watch",
        "wheel",
        "twine",
        "ipython",
    ],
    "python-jose": [
        "python-jose==3.3.0",
    ],
    "crypto": [
        "cryptography>=3.3.1",
    ],
}

extras_require["dev"] = (
    extras_require["dev"]
    + extras_require["test"]
    + extras_require["lint"]
    + extras_require["doc"]
    + extras_require["python-jose"]
)


setup(
    name="djangorestframework_simplejwt_mongoengine",
    keywords="djangorestframework_simplejwt_mongoengine",
    author="Đỗ Ngọc Ngoạn (aka Ngoan Do)",
    author_email="ngocngoan060288@gmail.com",
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.1",
        "Framework :: Django :: 4.2",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Internet :: WWW/HTTP",
    ],
    description="Simple JWT is a JSON Web Token authentication plugin for the Django REST Framework which to be compatible with MongoEngine.",  # noqa: E501
    long_description=Path("README.rst").read_text(encoding="utf-8"),
    install_requires=requirements,
    extras_require=extras_require,
    license="GNU General Public License v3",
    include_package_data=True,
    zip_safe=False,
    packages=find_packages(
        include=[
            "rest_framework_simplejwt_mongoengine",
            "rest_framework_simplejwt_mongoengine.*",
        ]
    ),
    test_suite="tests",
    url="https://github.com/ngocngoan/djangorestframework-simplejwt-mongoengine",
    version="1.3.0",
)
