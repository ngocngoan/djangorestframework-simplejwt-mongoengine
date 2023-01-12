#!/usr/bin/env python

"""The setup script."""

from pathlib import Path

from setuptools import find_packages, setup

requirements = [
    "django>=3.2,<4.1",
    "djangorestframework>=3.11",
    "djangorestframework-simplejwt>=4.7,<5.2",
    "django-mongoengine>=0.5.4",
    "pyjwt>=1.7.1,<3",
]

test_requirements = [
    "pytest>=3",
]

setup(
    author="Đỗ Ngọc Ngoạn (aka Ngoan Do)",
    author_email="ngocngoan060288@gmail.com",
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.0",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Internet :: WWW/HTTP",
    ],
    description="Simple JWT is a JSON Web Token authentication plugin for the Django REST Framework which to be compatible with MongoEngine.",  # noqa: E501
    long_description=Path("README.rst").read_text(encoding="utf-8"),
    install_requires=requirements,
    license="GNU General Public License v3",
    include_package_data=True,
    keywords="djangorestframework_simplejwt_mongoengine",
    name="djangorestframework_simplejwt_mongoengine",
    packages=find_packages(
        include=[
            "rest_framework_simplejwt_mongoengine",
            "rest_framework_simplejwt_mongoengine.*",
        ]
    ),
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/ngocngoan/djangorestframework-simplejwt-mongoengine",
    version="1.2.0",
    zip_safe=False,
)
