from setuptools import setup

__about__: dict[str, str] = {}

with open("urbanairship/__about__.py") as fp:
    exec(fp.read(), None, __about__)

# Read long description from README
with open("README.rst", encoding="utf-8") as f:
    long_description = f.read()

# Define test requirements
test_requirements = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "mock>=5.0.0",
]

setup(
    name="urbanairship",
    version=__about__["__version__"],
    author="Airship Tools",
    author_email="tools@airship.com",
    url="https://airship.com/",
    description="Python package for using the Airship API",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    packages=[
        "urbanairship",
        "urbanairship.push",
        "urbanairship.devices",
        "urbanairship.reports",
        "urbanairship.automation",
        "urbanairship.experiments",
        "urbanairship.custom_events",
    ],
    license="BSD License",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Software Development :: Libraries",
    ],
    python_requires=">=3.10",
    install_requires=["requests>=2.32", "six", "backoff>=2.2.1", "pyjwt>=2.8.0"],
    tests_require=test_requirements,
    extras_require={
        "test": test_requirements,
        "dev": test_requirements + ["black", "isort", "flake8"],
    },
    package_data={
        "urbanairship": ["py.typed"],
    },
    project_urls={
        "Documentation": "https://docs.airship.com/",
        "Source": "https://github.com/urbanairship/python-library",
        "Tracker": "https://github.com/urbanairship/python-library/issues",
    },
    test_suite="tests",
)
